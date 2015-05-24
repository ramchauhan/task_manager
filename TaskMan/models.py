import datetime
from django.db import models
from django.contrib.auth import models as auth_models

from TaskMan import constants


class CustomUserManager(auth_models.BaseUserManager):
    def create_user(self, email, user_name, password):
    
        user = self.model(
                            email = CustomUserManager.normalize_email(email),
                            user_name = user_name,
                         )
        user.is_staff = True
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, user_name, password):

        user = self.model(
                            email = CustomUserManager.normalize_email(email),
                            user_name = user_name,
                         )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using = self._db)
        return user


class UserProfile(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    """ Model for user profile """

    email = models.EmailField(verbose_name = 'E-Mail', unique = True)
    user_name = models.CharField(verbose_name = 'User Name', max_length=20, unique = True)    
    is_staff = models.BooleanField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', ]
    
    objects = CustomUserManager()
    
    def get_full_name(self):
        return self.user_name
    
    def get_short_name(self):
        return self.user_name

    def __unicode__(self):
        return self.email

    def is_staff(self):
        return self.is_staff
        
class Tasks(models.Model):
    
    user = models.ForeignKey(UserProfile)
    task = models.CharField(verbose_name = 'Task Name', max_length=100, blank=False)
    created_date = models.DateField(auto_now_add=True)
    dead_line_date = models.DateField(verbose_name = 'Specify Dead Line Date', blank=False, default=datetime.date.today)
    is_completed = models.CharField(choices=constants.TASK_STATUS_CHOICES, default='INC', max_length=10)
    
    def __unicode__(self):
        return self.task
        

    
    


