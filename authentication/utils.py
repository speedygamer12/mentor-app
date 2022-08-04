from django.core.mail import EmailMultiAlternatives
from django.template import Context

import threading

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        htmly_content = data['html_content'].render(data['context'])
        texty_content = data['text_content'].render(data['context'])
        print(data.get('context'))
        email = EmailMultiAlternatives(
            subject=data['email_subject'], body=texty_content, to=[data['to_email']])
        email.attach_alternative(htmly_content, "text/html")
        EmailThread(email).start()
