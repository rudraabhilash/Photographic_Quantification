from django.template import loader
from django.http import HttpResponse
from .models import doctorinfo

def doctor(request):
    #return HttpResponse("welcome!")
    template = loader.get_template('doctorshome.html')
    return HttpResponse(template.render())

#Read operation
def doctordata(request):
    ddata = doctorinfo.objects.all().values() #using ORM rather than using sql 
    template = loader.get_template('doctordata.html')
    context = {
        'ddata': ddata,
    }
    return HttpResponse(template.render(context, request))

