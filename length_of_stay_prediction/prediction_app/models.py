from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

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
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='admin')

    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

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


class Area(models.Model):
    status = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=10)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    max_rooms = models.IntegerField(null=True, blank=True, default=4)


class Room(models.Model):
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    number = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    max_beds = models.IntegerField(null=True, blank=True, default=4)

    def __str__(self):
        return f"{_ if self.area is None else self.area.name}-{self.number}"


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'SINGLE'),
        ('MARRIED', 'MARRIED'),                     
        ('WIDOWED', 'WIDOWED'),
        ('DIVORCED', 'DIVORCED'),
        ('SEPARATED', 'SEPARATED'),
        ('LIFE PARTNER', 'LIFE PARTNER'),
        ('UNKNOWN', 'UNKNOWN'),
    ]

    RELIGION_CHOICES = [
        ('RELIGIOUS', 'RELIGIOUS'),                 
        ('NOT SPECIFIED', 'NOT SPECIFIED'),
        ('UNOBTAINABLE', 'UNOBTAINABLE'),
    ]

    ETHNICITY_CHOICES = [
        ('WHITE', 'WHITE'),                                                                                            
        ('BLACK/AFRICAN AMERICAN', 'BLACK/AFRICAN AMERICAN'),
        ('HISPANIC OR LATINO', 'HISPANIC OR LATINO'),
        ('ASIAN', 'ASIAN'),
        ('OTHER/UNKNOWN', 'OTHER/UNKNOWN'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=150,  blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(
        max_length=15, choices=MARITAL_STATUS_CHOICES, default='UNKNOWN')
    religion = models.CharField(
        max_length=20, choices=RELIGION_CHOICES)
    ethnicity = models.CharField(
        max_length=100,
        choices=ETHNICITY_CHOICES,
        null=True,
        blank=True,
        default='ASIAN'
    )
    photo = models.ImageField(
        upload_to='patient_photos/', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Admission(models.Model):
    LOS_LABLE_TO_NUMBER = {
        'Less than 3 days': 3,
        '3-7 days': 7,
        '7-14 days': 14,
        'More than 14 days': 30,
    }
    ADMISSION_TYPE_CHOICES = [
        ('EMERGENCY', 'EMERGENCY'),
        ('ELECTIVE', 'ELECTIVE'),
        ('URGENT', 'URGENT'),
        ('NEWBORN', 'NEWBORN'),
    ]
    LOS_CHOICES = [
        ('Less than 3 days', 'Less than 3 days'),
        ('3-7 days', '3-7 days'),
        ('7-14 days', '7-14 days'),
        ('More than 14 days', 'More than 14 days'),
    ]
    STATUS_CHOICES = [
        ('In Treatment', 'In Treatment'),
        ('Dischagred', 'Dischagred'),
    ]
    INSURANCE_CHOICES = [
        ('Medicare', 'Medicare'),
        ('Private', 'Private'),
        ('Medicaid', 'Medicaid'),
        ('Government', 'Government'),
        ('Self Pay', 'Self Pay')
    ]
    FIRST_CAREUNIT = [
        ("ICU", "ICU"),
        ("NICU", "NICU"),
    ]
    hadm_id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Patient, on_delete=models.CASCADE)
    insurance = models.TextField(max_length=10, choices=INSURANCE_CHOICES)
    diagnose = models.JSONField()
    clinical_note = models.TextField(null=True, blank=True)
    admission_type = models.CharField(max_length=10, choices=ADMISSION_TYPE_CHOICES)
    first_careunit = models.TextField(max_length=4, choices=FIRST_CAREUNIT)
    los_number = models.IntegerField(null=True, blank=True, default=3)
    los_label = models.CharField(
        null=True, blank=True, max_length=20, choices=LOS_CHOICES)
    los_actual = models.IntegerField(null=True, blank=True, default=0)
    los_actual_label = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(
        null=True, blank=True, max_length=15, choices=STATUS_CHOICES, default='In Treatment')
    admittime = models.DateTimeField(auto_now_add=True)
    dischtime = models.DateTimeField(blank=True, null=True)
    dischtime_estimate = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if self.los_label:
            self.los_number = self.LOS_LABLE_TO_NUMBER.get(self.los_label)
        if self.admittime and self.los_number:
            self.dischtime_estimate = self.admittime + timedelta(days=self.los_number)
        elif self.admittime is None and self.los_number:
            self.dischtime_estimate = datetime.now() + timedelta(days=self.los_number)
        if self.dischtime and self.admittime:
            self.los_actual = (self.dischtime - self.admittime).days
            if self.los_actual <= 3:
                self.los_actual_label = 'Less than 3 days'
            elif 3 < self.los_actual <= 7:
                self.los_actual_label = '3-7 days'
            elif 7 < self.los_actual <= 14:
                self.los_actual_label = '7-14 days'
            else:
                self.los_actual_label = 'More than 14 days'
        super().save(*args, **kwargs)


class AIModelStats(models.Model):
    accuracy = models.FloatField(null=True, blank=True)
    num_samples = models.IntegerField(null=True, blank=True)
    last_training_time = models.DateTimeField()

    def __str__(self):
        return f"Accuracy: {self.accuracy}, Samples: {self.num_samples}, Last Trained: {self.last_training_time}"
