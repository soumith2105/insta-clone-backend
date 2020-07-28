from django.shortcuts import render


def home_page(request):
    template_name = "home.html"
    return render(request, template_name)


def about_page(request):
    template_name = "about.html"
    return render(request, template_name)
