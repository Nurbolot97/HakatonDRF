from user_accounts.models import User
from main.models import *
from user_accounts.models import *
from django.shortcuts import redirect, render
from .serializers import (UserRegisterSerializer, CategorySerializer, 
                            EnginesSerializer, DisplaysSerializer,
                            WheelsSerializer, UserListSerializer
                            )
from rest_framework import status, response, decorators
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.renderers import JSONRenderer
from .token import account_activation_token
from django.utils.encoding import force_bytes, force_text
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter



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
        return render(request, 'conf_next.html')
    else:
        return response.Response('Invalid')


class UsersListApiView(ListAPIView):

    serializer_class = UserListSerializer
    queryset = User.objects.all()


class CategoryListApiView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name_category']


class EnginesListApiView(ListAPIView):

    serializer_class = EnginesSerializer
    queryset = Engine.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class EngineDetailApiView(RetrieveAPIView):

    serializer_class = EnginesSerializer
    queryset = Engine.objects.all()
    lookup_field = 'id'



class DisplayListApiView(ListAPIView):

    serializer_class = DisplaysSerializer
    queryset = Display.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class DisplayDetailApiView(RetrieveAPIView):

    serializer_class = DisplaysSerializer
    queryset = Display.objects.all()
    lookup_field = 'id'


class WheelListApiView(ListAPIView):

    serializer_class = WheelsSerializer
    queryset = Wheel.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class WheelDetailApiView(RetrieveAPIView):

    serializer_class = WheelsSerializer
    queryset = Wheel.objects.all()
    lookup_field = 'id'

