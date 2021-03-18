import jwt
import os
from django.shortcuts import redirect, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, views, status, response, decorators
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.renderers import JSONRenderer
from django.utils.encoding import force_bytes, force_text, smart_bytes, DjangoUnicodeDecodeError, smart_str
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponsePermanentRedirect
from drf_yasg import openapi
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import (RetrieveAPIView, ListAPIView, 
                                    CreateAPIView, RetrieveUpdateDestroyAPIView,
                                    UpdateAPIView, DestroyAPIView
                                    )


from main.models import *
from .utils import Util
from .service import EngineFilter
from .permissions import IsCommentOwner
from .renderers import UserRenderer
from .token import account_activation_token
from .serializers import (CategorySerializer, EnginesSerializer, DisplaysSerializer,
                            WheelsSerializer, UserListSerializer,UserRegisterSerializer,
                            ResetPasswordSerializer, SetNewPasswordSerializer, 
                            CommentSerializer
                            )


@decorators.api_view(['POST'])
@decorators.renderer_classes([JSONRenderer])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    user.is_active = False
    user.save()
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    to_email = user.email
    message = render_to_string('confirmation.html', {'user': user,
                                                     'domain': current_site.domain,
                                                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                     'token': account_activation_token.make_token(user)
                                                     })
    email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
    email.content_subtype = 'html'
    email.send(fail_silently=True)
    return response.Response('Email was send for confirmation',
                             status.HTTP_201_CREATED)


@decorators.api_view(['POST', 'GET'])
@decorators.renderer_classes([JSONRenderer])
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return response.Response(tokens)
    else:
        return response.Response('Invalid')


class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid'})
            
            return Response({'success': True, 'message': 'Credentails is valid', 'uidb64': uidb64, 'token': token})


        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class UsersListApiView(ListAPIView):

    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class ProductsPagination(PageNumberPagination):

    page_size = 2
    page_size_query_params = 'page_size'
    max_page_size = 10


class CategoryCreateApiView(CreateAPIView):
    
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class CategoryListApiView(ListAPIView):
    
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = ProductsPagination
    filter_backends = [SearchFilter]
    search_fields = ['name_category']


class CategoryApiView(RetrieveUpdateDestroyAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'


class EnginesListApiView(ListAPIView):

    serializer_class = EnginesSerializer
    queryset = Engine.objects.all()
    pagination_class = ProductsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EngineFilter


class EngineDetailApiView(RetrieveAPIView):

    serializer_class = EnginesSerializer
    queryset = Engine.objects.all()
    lookup_field = 'id'


class EngineCreateApiView(CreateAPIView):

    serializer_class = EnginesSerializer
    queryset = Engine.objects.all()
    permission_classes = [IsAdminUser]


class EngineUpdateApiView(UpdateAPIView):

    serializer_class = EnginesSerializer
    queryset = Engine.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'


class EngineDestroyApiView(DestroyAPIView):

    serializer_class = EnginesSerializer
    queryset = Engine.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'



class CommentListApiView(ListAPIView):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
   

class CommentCreateApiView(CreateAPIView):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]


class CommentDestroyApiView(DestroyAPIView):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'



class DisplayListApiView(ListAPIView):

    serializer_class = DisplaysSerializer
    queryset = Display.objects.all()
    pagination_class = ProductsPagination
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class DisplayDetailApiView(RetrieveAPIView):

    serializer_class = DisplaysSerializer
    queryset = Display.objects.all()
    lookup_field = 'id'


class WheelListApiView(ListAPIView):

    serializer_class = WheelsSerializer
    queryset = Wheel.objects.all()
    pagination_class = ProductsPagination
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class WheelDetailApiView(RetrieveAPIView):

    serializer_class = WheelsSerializer
    queryset = Wheel.objects.all()
    lookup_field = 'id'

