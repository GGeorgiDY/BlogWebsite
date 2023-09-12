from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# creating a Custom User Manager
class MyAccountManager(BaseUserManager):
    # What I want to happen when a new user is created
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        # create the user
        user = self.model(
            # normalize_email will convert all the characters in the email to lower case.
            # normalize_email is available only in BaseUserManager
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # What I want to happen when a new superuser is created
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# creating a custom user model
class AppUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    # required fields
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # log in with email
    USERNAME_FIELD = 'email'

    # required field on registration
    REQUIRED_FIELDS = ['username', ]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # required functions when creating custom user models
    # for checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

