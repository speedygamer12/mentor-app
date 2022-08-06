from concurrent.futures import thread
from django.core.mail import EmailMultiAlternatives
from twilio.rest import Client
from django.conf import settings

import threading

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class PhoneThread(threading.Thread):

    def __init__(self, phone):
        self.phone = phone
        threading.Thread.__init__(self)

    def run(self):
        self.phone.send


class Util:
    @staticmethod
    def send_email(data):
        htmly_content = data['html_content'].render(data['context'])
        texty_content = data['text_content'].render(data['context'])
        email = EmailMultiAlternatives(
            subject=data['email_subject'], body=texty_content, to=[data['to_email']])
        email.attach_alternative(htmly_content, "text/html")
        EmailThread(email).start()


    def send_phone(data):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN )
        message = client.messages.create(
            to= str(data['phone_number']), 
            from_="+13252387711", 
            body="Hey I hope you received this message",
            short_description = "Send text campaign"
            )

        PhoneThread(message).start()

    