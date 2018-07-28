from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
  def validate_user(self, request):
    email = request.POST['email']
    password = request.POST['password']
    errors = []
    
    #Check first name
    if request.POST['firstName'] == '':         
      errors.append('First Name cannot be blank')
        
    if any(char.isdigit() for char in request.POST['firstName']) == True:              
      errors.append('First Name cannot have numbers')
    
    #Check last name
    if request.POST['lastName'] == '':             
      errors.append('Last Name cannot be blank')
        
    if any(char.isdigit() for char in request.POST['lastName']) == True:              
      errors.append('Last Name cannot have numbers')
 
    #Check email
    if request.POST['email'] == '':             
      errors.append('Email cannot be blank')
        
    if not EMAIL_REGEX.match(request.POST['email']):        
      errors.append('Invalid email address')
   
    #Check password
    if request.POST['password'] == '':      
      errors.append('Password cannot be blank')
        
    if len(request.POST['password']) < 8:              
      errors.append('Password must be greater than 8 characters')        
   
    #Check confirmation password
    if request.POST['confirmPassword'] == '':              
        errors.append('Please confirm password')
        
    if request.POST['confirmPassword'] != request.POST['password']:               
        errors.append('Passwords do not match')   

    try:
      self.get(email=email)
      errors.append('Email already in use.')
      return errors
    except:      
      return errors

  def reg_validation(self, request):
      # Refer back to the validation_error function
      errors = self.validate_user(request)
      # If there are any errors, return those errors instead of moving on
      if len(errors) > 0:
          return (False, errors)
      # If there are no errors, hash the password using Bcrypt, then add user to database
      pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
      user = self.create(first_name=request.POST['firstName'], last_name=request.POST['lastName'], email=request.POST['email'], password=pw_hash)
      return (True, user)

  def login_validation(self, request):
    # Check if user email and password are in database, and if they match    
    try:
        # user = self.get(email=request.POST['email'])
        # password = request.POST['password'].encode()      
        # if bcrypt.checkpw(password.encode(),  user.password.encode()):
        user = self.get(email=request.POST['email'])
        hashed = user.password        
        hashed = hashed.encode('utf-8')        
        password = request.POST['password']
        password = password.encode('utf-8')        
        if bcrypt.hashpw(password, hashed) == hashed:          
          return (True, user)
      # If neither exist, just return false automatically. If one of these returns false, return the same result to keep confidentiality
    except ObjectDoesNotExist:
      pass
    return (False, ["Email/password don't match"])

class User(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email = models.CharField(max_length = 60)
  password = models.CharField(max_length = 30) 
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = UserManager()
  