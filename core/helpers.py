from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def send_activate_link(user,domain,uid,token):
    subject = 'Confirm your email and start using our platform'
    html_content = render_to_string('activate.html', {
    'user': user,
    'domain': domain,
    'uid':uid,
    'token': token,
    })
    text_content = strip_tags(html_content)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject,text_content, email_from, recipient_list)
    return True





def send_contact(name, user_email, reason, message):
    context ={
        'name' :  name,
        "user_email": user_email,
        "reason" : reason,
        "message" : message
    }
    html_content = render_to_string("contact_mail.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Contact   {user_email}-{reason}',
        text_content,
        settings.EMAIL_HOST_USER ,
        ['ilgarshukuroff@gmail.com']
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return True


def send_order_request(user_email, requirements, description):
    context ={
        "user_email": user_email,
        "requirements" : requirements,
        "description" : description
    }
    html_content = render_to_string("order_request.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Order request   {user_email}-{requirements}',
        text_content,
        settings.EMAIL_HOST_USER ,
        ['ilgarshukuroff@gmail.com']
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return True


def send_pay_success(order,amount,type):
    context ={
        "order": order,
        "amount" : amount,
        "type" : type
    }
    if order.product.type == 'custom':
        reaming_part = order.product.price - order.deposit
        context['reaming_part'] = reaming_part
    html_content = render_to_string("pay_success_mail.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f'Thanks for purchase {order.costumer.get_full_name()}',
        text_content,
        settings.EMAIL_HOST_USER ,
        [order.costumer.email]
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return True