from django.template import loader
from django.http import HttpResponse

def event1(request):
    template = loader.get_template('home_page.html')
    return HttpResponse(template.render())

