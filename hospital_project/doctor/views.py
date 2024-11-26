from django.template import loader
from django.http import HttpResponse

def doctor(request):
    #return HttpResponse("welcome!")
    template = loader.get_template('doctorshome.html')
    return HttpResponse(template.render())
