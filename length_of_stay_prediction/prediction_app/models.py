from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _



class UserManager(BaseUserManager):
    def create_user(self, username, date_of_birth, password=None):
        """
        Creates and saves a User with the given role, date of
        birth and password.
        """

        user = self.model(
            username=username,
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given username, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.role = 'admin'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.role == 'admin'
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

class Room(models.Model):
    status = models.CharField(max_length=10, null=True, blank=True)
    number = models.IntegerField()

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('SP', 'Separated'),
        ('W', 'Widowed'),
    ]

    RELIGION_CHOICES = [
        ('NS', 'Not Specified'),
        ('CH', 'Christian'),
        ('IS', 'Islam'),
        ('JW', 'Jewish'),
        ('BD', 'Buddhist'),
        ('OT', 'Other'),
    ]

    ETHNICITY_CHOICES = [
        ('asian', 'Asian'),
        ('black', 'Black / African American'),
        ('white', 'White'),
        ('hispanic', 'Hispanic / Latino'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=150,  blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=2, choices=MARITAL_STATUS_CHOICES)
    religion = models.CharField(max_length=2, choices=RELIGION_CHOICES, default='NS')
    ethnicity = models.CharField(
        max_length=100, 
        choices=ETHNICITY_CHOICES, 
        null=True, 
        blank=True,
        default='other'
    )
    photo = models.ImageField(upload_to='patient_photos/', blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Admission(models.Model):
    ADMISSION_TYPE_CHOICES = [
        ('E', 'Emergency '),
        ('U', 'Urgent '),
        ('EL', 'Elective '),
        ('OT', 'Other'),
    ]
    LOS_CHOICES = [
        ('L', 'Long-Term'),
        ('M', 'Mid-Term'),
        ('S', 'Short-Term'),
    ]
    STATUS_CHOICES = [
        ('I', 'In Treatment'),
        ('D', 'Dischagred'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    diagnose = models.TextField()
    clinical_note = models.TextField(null=True, blank=True)
    icd_code = models.CharField(max_length=7)
    type = models.CharField(max_length=2, choices=ADMISSION_TYPE_CHOICES, default='OT')
    los_number = models.IntegerField(null=True, blank=True, default=0)
    los_category = models.CharField(null=True, blank=True, max_length=2, choices=LOS_CHOICES, default='S')
    status = models.CharField(null=True, blank=True, max_length=2, choices=STATUS_CHOICES, default='I')
    