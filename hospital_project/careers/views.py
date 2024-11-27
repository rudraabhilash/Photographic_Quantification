from django.template import loader
from django.http import HttpResponse
from .models import positions

def careers(request):
    #return HttpResponse("welcome!")
    template = loader.get_template('careershome.html')
    return HttpResponse(template.render())

def careersdata(request):
    cdata = positions.objects.all().values() #using ORM rather than using sql 
    template = loader.get_template('careersdata.html')
    context = {
        'cdata': cdata,
    }
    return HttpResponse(template.render(context, request))
