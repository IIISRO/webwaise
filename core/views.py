from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404,HttpResponse
from .forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from .helpers import send_activate_link,send_contact,send_order_request,send_pay_success
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.utils.encoding import force_str    
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.signals import user_logged_in
from .models import Contact, OrderRequest, Product, Order
import stripe





User = get_user_model()
    



# Create your views here.


def home(request):
    if request.method == 'POST':    
        if request.user.is_authenticated:
            OrderRequest.objects.create(costumer = request.user, requirements = request.POST.getlist('req'), desc = request.POST['desc'])
            send_order_request(request.user.email,request.POST.getlist('req'), request.POST['desc'])
            messages.error(request, f"Your request was received! We will contact with you through this email ({request.user.email}) to inform you about custom package pricing as soon as possible!")

        else:
            messages.success(request, "Please signin first.")
            return redirect(reverse_lazy('core:home'))

    return render(request, 'home.html')


def notfound(request, exception):
    return render(request, '404.html')

def contact(request):

    if request.method == 'POST':
        Contact.objects.create(name = request.POST['name'], email = request.POST['email'], reason = request.POST['Reason'], message = request.POST['field'])
        send_contact(request.POST['name'], request.POST['email'], request.POST['Reason'], request.POST['field'])
        messages.success(request, """
        Thank you for reaching out to us!

This is the confirmation that we received your email. We will respond to your email as soon as possible!
""")
        return redirect(reverse_lazy('core:home'))
    return render(request, 'contact.html')

def info(request):
    return render(request, 'info.html')

def signin(request):

    form = RegistrationForm()
    if request.user.is_authenticated:            
            return redirect(reverse_lazy('core:home'))
    if request.method == "POST":
        if 'signup' in request.POST:
            if User.objects.filter(email=request.POST['email']):
                messages.error(request, 'This email alerdy registered!')
            else:
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.is_active = False
                    user.username = user.email
                    user.save()
                    current_site = get_current_site(request)
                    send_activate_link(user,current_site.domain,urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(user))
                    messages.success(request, 'Activation mail sended!')
                    return redirect(reverse_lazy('core:home'))
        if 'signin' in request.POST:
            email = request.POST['email']
            
            if User.objects.filter(email=email):
                password = request.POST['password']
                username = User.objects.get(username=email).username
                user_act = User.objects.get(username=email)
                user = authenticate(request, username = username, password = password)
                if user is not None and user_act.is_active:
                    login(request,user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect(reverse_lazy("core:home"))
                elif check_password(password, user_act.password) and not user_act.is_active:
                    current_site = get_current_site(request)
                    send_activate_link(user_act,current_site.domain,urlsafe_base64_encode(force_bytes(user_act.pk)), account_activation_token.make_token(user_act))
                    messages.error(request, 'Your account not activated, activation mail sended!')
                        
                else:  messages.success(request, 'Password or Email wrong!')

            else:  messages.success(request, 'Password or Email wrong!')
        
            


    return render(request,'signin.html', context={'form':form})


def logged_in_message(sender, user, request, **kwargs):

    messages.success(request, 'You are loged in!')


user_logged_in.connect(logged_in_message)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and not user.is_active and account_activation_token.check_token(user, token)  :
        user.is_active = True   
        user.save()
        messages.success(request, 'Your account activated!')
        return redirect(reverse_lazy('core:signin'))
    else:
        raise Http404
    
@login_required()
def logout_user(request):
    logout(request)
    messages.success(request, 'Your are loged out!')
    return redirect(reverse_lazy('core:home'))


    
def service(request, category):
    
    products = Product.objects.filter(category = category, type = 'standart')
    context = {
        'products' : products,
        'category' : category
    }
    if products:
        pass
    else: raise Http404
    return render(request, 'service.html',context)

stripe.api_key = "sk_test_51MT1tpIpI2DRrDde4li8UJBGaNS73zugCRBzco8SHT71xKHy2byY41Aogmnt33dEbAJDWqTAfPs5d5MVTNsCBTcH00Xfdxda1D"

def payment(request, prodid):
    product = get_object_or_404(Product, id = prodid)
    if product.type == 'standart' and request.user.is_authenticated:
        if request.method == "POST":
            amount = int(product.price) 
            #Create customer
            try:
                customer = stripe.Customer.create(
                            email=request.user.email,
                            name=request.user.get_full_name(),
                            description=f"{product.name} payment",
                            source=request.POST['stripeToken']
                            )

            except stripe.error.CardError as e:
                return render(request, 'unseccess.html',context={'head':'CardError', 'message':'There was an error charging your card'})            
                   

            except stripe.error.RateLimitError as e:
                return render(request, 'unseccess.html',context={'head':'RateLimitError', 'message':'Rate error!'})            
            

            except stripe.error.InvalidRequestError as e:
                return render(request, 'unseccess.html',context={'head':'InvalidRequestError', 'message':'Invalid Requestor'})            


            except stripe.error.AuthenticationError as e:  
                return render(request, 'unseccess.html',context={'head':'AuthenticationError', 'message':'Invalid API auth!'})            

            except stripe.error.StripeError as e:  
                return render(request, 'unseccess.html',context={'head':'StripeError', 'message':'Stripe error!'})            


            except Exception as e:  
                return render(request, 'unseccess.html',context={'head':'Payment unsuccess', 'message':e}) 
            #Stripe charge 
            charge = stripe.Charge.create(
                    customer=customer,
                        amount=int(amount)*100,
                        currency='usd',
                        description=f"{product.name}-{product.category} sell"
                    ) 
            transRetrive = stripe.Charge.retrieve(
                        charge["id"],
                        api_key="sk_test_51MT1tpIpI2DRrDde4li8UJBGaNS73zugCRBzco8SHT71xKHy2byY41Aogmnt33dEbAJDWqTAfPs5d5MVTNsCBTcH00Xfdxda1D"
                    )
            charge.save() # Uses the same API Key.

            order = Order.objects.create(costumer=User.objects.get(username=request.user.username),product=Product.objects.get(id=product.id),payed_amount=product.price,is_payed=True)
            send_pay_success(order,amount,'standart')
            return render(request, 'success.html',context={'order':order,'type':'standart' ,'amount':amount})

        return render(request, 'pay.html',context={'product':product})
    

    elif product.type == 'standart' and not request.user.is_authenticated:
        messages.success(request, 'Please signin first!')
        return redirect(reverse_lazy('core:service', kwargs={'category': product.category}))
    
    
    
    elif product.type == 'custom':
        order = get_object_or_404(Order, product = product)
        if order.pay_access == False:
            raise Http404
            
        if not order.deposit_payed:
            amount = int(order.deposit) 
            if request.method == "POST":
                #Create customer
                try:
                    customer = stripe.Customer.create(
                                email=order.costumer.email,
                                name=order.costumer.get_full_name(),
                                description=f"{order.product.name} payment deposit",
                                source=request.POST['stripeToken']
                                )

                except stripe.error.CardError as e:
                    return render(request, 'unseccess.html',context={'head':'CardError', 'message':'There was an error charging your card'})            
                   

                except stripe.error.RateLimitError as e:
                    return render(request, 'unseccess.html',context={'head':'RateLimitError', 'message':'Rate error!'})            
                

                except stripe.error.InvalidRequestError as e:
                    return render(request, 'unseccess.html',context={'head':'InvalidRequestError', 'message':'Invalid Requestor'})            


                except stripe.error.AuthenticationError as e:  
                    return render(request, 'unseccess.html',context={'head':'AuthenticationError', 'message':'Invalid API auth!'})            

                except stripe.error.StripeError as e:  
                    return render(request, 'unseccess.html',context={'head':'StripeError', 'message':'Stripe error!'})            

                except Exception as e:  
                    return render(request, 'unseccess.html',context={'head':'Payment unsuccess', 'message':e}) 
                #Stripe charge 
                charge = stripe.Charge.create(
                        customer=customer,
                            amount=int(amount)*100,
                            currency='usd',
                            description=f"{order.product.name}-{order.product.category} deposit"
                        ) 
                transRetrive = stripe.Charge.retrieve(
                            charge["id"],
                            api_key="sk_test_51MT1tpIpI2DRrDde4li8UJBGaNS73zugCRBzco8SHT71xKHy2byY41Aogmnt33dEbAJDWqTAfPs5d5MVTNsCBTcH00Xfdxda1D"
                        )
                charge.save() # Uses the same API Key.

                order.deposit_payed=True
                order.pay_access=False
                order.payed_amount = amount
                order.save()
                send_pay_success(order,amount,'deposit')
                return render(request, 'success.html',context={'order':order,'type':'deposit' ,'amount':amount})
            

            return render(request, 'custom_order_pay.html',context={'order':order,'payment_type':'deposit','amount':amount})
        elif order.deposit_payed and not order.is_payed:
            amount = int(order.product.price)-int(order.deposit) 
            if request.method == "POST":
                #Create customer
                try:
                    customer = stripe.Customer.create(
                                email=order.costumer.email,
                                name=order.costumer.get_full_name(),
                                description=f"{order.product.name} payment deposit",
                                source=request.POST['stripeToken']
                                )

                except stripe.error.CardError as e:
                    return render(request, 'unseccess.html',context={'head':'CardError', 'message':'There was an error charging your card'})            
                   

                except stripe.error.RateLimitError as e:
                    return render(request, 'unseccess.html',context={'head':'RateLimitError', 'message':'Rate error!'})            
                

                except stripe.error.InvalidRequestError as e:
                    return render(request, 'unseccess.html',context={'head':'InvalidRequestError', 'message':'Invalid Requestor'})            


                except stripe.error.AuthenticationError as e:  
                    return render(request, 'unseccess.html',context={'head':'AuthenticationError', 'message':'Invalid API auth!'})            

                except stripe.error.StripeError as e:  
                    return render(request, 'unseccess.html',context={'head':'StripeError', 'message':'Stripe error!'})            

                except Exception as e:  
                    return render(request, 'unseccess.html',context={'head':'Payment unsuccess', 'message':e})  
                #Stripe charge 
                charge = stripe.Charge.create(
                        customer=customer,
                            amount=int(amount)*100,
                            currency='usd',
                            description=f"{order.product.name}-{order.product.category} sell"
                        ) 
                transRetrive = stripe.Charge.retrieve(
                            charge["id"],
                            api_key="sk_test_51MT1tpIpI2DRrDde4li8UJBGaNS73zugCRBzco8SHT71xKHy2byY41Aogmnt33dEbAJDWqTAfPs5d5MVTNsCBTcH00Xfdxda1D"
                        )
                charge.save() # Uses the same API Key.

                order.is_payed=True
                order.pay_access=False
                order.payed_amount = order.payed_amount + amount
                order.save()
                send_pay_success(order,amount,'remaning part price')

                return render(request, 'success.html',context={'order':order, 'type':'reaming' ,'amount':amount})            

            return render(request, 'custom_order_pay.html',context={'order':order,'payment_type':'remaning part','amount':amount})
        else:
            raise Http404








