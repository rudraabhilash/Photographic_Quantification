from django.template import loader
from django.http import HttpResponse

def careers(request):
    #return HttpResponse("welcome!")
    template = loader.get_template('careershome.html')
    return HttpResponse(template.render())
