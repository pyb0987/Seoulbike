from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



class sendEmail:
    def __init__(self):
        self.instance = None
    def sendEmail(self, instance, token_created):
        if self.instance == instance:
            return
        self.instance = instance
        # send an e-mail to the user
        context = {
            'current_user': token_created.user,
            'username': token_created.user.username,
            'email': token_created.user.email,
            'reset_password_url': "{}?token={}".format(
                "http://localhost:8080/#/users/renew-password/",
                token_created.key)
        }

        # render email text
        email_html_message = render_to_string('../templates/user_reset_password.html', context)
        email_plaintext_message = render_to_string('../templates/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "{title} 비밀번호 변경 메일입니다.".format(title="Seoulbike"),
            # message:
            email_plaintext_message,
            # from:
            "noreply@somehost.local",
            # to:
            [token_created.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
        print('sent')

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print('password_reset_token_created')
    sendemail.sendEmail(instance, reset_password_token)
    reset_password_token_created.disconnect(sender=instance)
    reset_password_token_created.disconnect(sender=sender)
    return 

sendemail = sendEmail()