from django.template import loader
from django.http import HttpResponse
from .models import payments

def payment(request):
    #return HttpResponse("welcome!")
    template = loader.get_template('paymentshome.html')
    return HttpResponse(template.render())



#Read operation
def paymentsdata(request):
    pdata = payments.objects.all().values() #using ORM rather than using sql 
    template = loader.get_template('paymentsdata.html')
    context = {
        'pdata': pdata,
    }
    return HttpResponse(template.render(context, request))
