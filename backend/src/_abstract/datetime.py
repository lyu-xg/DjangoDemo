import os, hashlib, random,json, twilio
from datetime import datetime, date
from django.core.exceptions import ValidationError

def calculate_age(value):
    today = date.today()
    return today.year - value.year - ((today.month, today.day) < (value.month, value.day))

def less_than_18(value):
    if calculate_age(value)<18:
        raise ValidationError("You're too young to use this application!")

