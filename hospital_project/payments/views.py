from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from .models import payments
from django.views.decorators.csrf import csrf_exempt

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

#write page
def paymentsdata(request):   
    template = loader.get_template('paymentsdatawrite.html')
    return HttpResponse(template.render())

#Write operation
@csrf_exempt
def paymentsdatawrite(request):
    if request.method == 'POST':
        Name = request.POST.get('Name')
        Remarks = request.POST.get('Remarks')
        contact = request.POST.get('contact')
        emailID = request.POST.get('emailID')
        consulatationFee = request.POST.get('consulatationFee')

        temp = payments(
            Name=Name,
            Remarks=Remarks,
            contact=contact,
            emailID=emailID,
            consulatationFee=consulatationFee,
        )
        temp.save() #this line is important for saving form data in the database
        return redirect("/")  # this page after saving data in database
    else:
        return HttpResponse("Invalid request method..")
