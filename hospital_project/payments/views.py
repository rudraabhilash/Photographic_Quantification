from django.template import loader
from django.http import HttpResponse

def payments(request):
    #return HttpResponse("welcome!")
    template = loader.get_template('paymentshome.html')
    return HttpResponse(template.render())
