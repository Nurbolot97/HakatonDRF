from django.shortcuts import render
from django.views.generic import TemplateView, ListView


class MainPageView(TemplateView):

    def get(self, request):
        return render(request, 'index.html')


class AboutUsView(TemplateView):

    def get(self, request):
        return render(request, 'about-us.html')


class BlogView(TemplateView):

    def get(self, request):
        return render(request, 'blog.html')


class ContactView(TemplateView):

    def get(self, request):
        return render(request, 'contact.html')


class CategoryListView(ListView):

    def get(self, request):
        return  render(request, 'shop.html')



