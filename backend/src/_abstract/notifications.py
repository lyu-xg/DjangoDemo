import re
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.query import QuerySet



def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class EmailNotification(object):
    def __init__(self, subject=None, text=None, html=None, variables=None, from_email=None):
        self.subject = subject
        self.text = text
        self.html = html
        self.variables = variables
        self.template_text = convert(self.__class__.__name__) + '.txt'
        self.template_html = convert(self.__class__.__name__) + '.html'
        self.from_email = from_email if from_email else settings.DEFAULT_FROM_EMAIL

    def __call__(self, to_email=None):
        content_text = render_to_string(self.template_text, self.variables) if self.variables else self.text
        content_html = render_to_string(self.template_html, self.variables) if self.variables else self.html

        # validate before sending
        if not any([self.subject, to_email, content_html, content_text]):
            raise ValueError("Can't send email as notification data corrupted")
        # convert to tuple, as this is what django needs
        if isinstance(to_email, str):
            to_email = (to_email,)

        # send mail
        send_mail(self.subject, content_text, self.from_email, to_email, fail_silently=False, html_message=content_html)
