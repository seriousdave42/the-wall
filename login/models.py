from django.db import models
import re
from datetime import datetime, timedelta

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least two characters long"
        elif (not post_data['first_name'].isalpha()):
            errors['first_name'] = "First name can only contain letters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least two characters long"
        elif (not post_data['last_name'].isalpha()):
            errors['last_name'] = "Last name can only contain letters"
        if len(post_data['birthdate']) <= 0:
            errors['birthdate'] = "Please enter a birthdate"
        elif datetime.fromisoformat(post_data['birthdate']) > datetime.now():
            errors["birthdate"] = "Birthdate cannot be in the future, Marty"
        elif datetime.now() - datetime.fromisoformat(post_data['birthdate']) < timedelta(days=13*365+3):
            errors["birthdate"] = "Users must be at least 13 years of age"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address"
        elif len(User.objects.filter(email = post_data['email'])) > 0:
            errors['email'] = "Email already exists"
        PW_REGEX = re.compile(r'^(?=.*cat)(?=.*5)[a-zA-Z0-9]{8,}$')
        if not PW_REGEX.match(post_data['password']):
            errors['password'] = "Password must be at least 8 characters, contain \"cat\", the number 5, and no special characters"
        if not post_data['password'] == post_data['pw_check']:
            errors['pw_check'] = "Passwords do not match!"
        return errors
    
        
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    birthdate = models.DateTimeField()
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 80)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()