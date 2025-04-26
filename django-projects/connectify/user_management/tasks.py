from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def send_verification_email(send_to: str, subject: str, context, template_name: str):
    html_content = render_to_string(
        template_name=template_name,
        context=context
    )
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        to=send_to
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()



@shared_task
def send_verification_email_task(send_to: str, send_to_username: str, verification_token: str):
    subject = "Verify your email"
    template_name = 'verifications/templates/user_verification_email_template.html'
    context = {
        'username': send_to_username,
        'verification_url': f"{verification_token}"
    }
    send_verification_email(
        send_to=send_to, 
        subject=subject,
        context=context,
        template_name=template_name
    )