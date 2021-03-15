# from django.shortcuts import render, redirect
# from .models import *
# from django.views.generic import CreateView, View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import UserProfileForm, SignUpForm
# from django.contrib.auth import login as auth_login


# def signup(request):
#     print(request.user)
#     if request.method == "POST":
#         form = SignUpForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             print(user)
#             return redirect('create_profile')
#     else:
#         form = SignUpForm()
#     return render(request, 'login.html', locals())


# class NewProfileView(CreateView, LoginRequiredMixin):

#     model = User
#     template_name = 'create_profile.html'
#     form_class = UserProfileForm
#     context_object_name = 'new_profile'

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.user = self.request.user
#         user.save()
#         return redirect('profile')


# class MyProfileView(View, LoginRequiredMixin):

#     def get(self, request):
#         p = request.user.profile
#         return render(request, "my_account.html", locals())