from datetime import time, timedelta
from datetime import datetime, time
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Department(models.Model):
    name=models.CharField(max_length=50)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=0)
    
    def __str__(self):
        return self.name
    
    
class Position(models.Model):
    name=models.CharField(max_length=50)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    salary_coef=models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.department.name}'
    

class Profile(models.Model):
    image = models.ImageField(upload_to='')
    cccd = models.CharField(max_length=12)
    dob=models.DateField()
    phone_number=models.CharField(max_length=12)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200)
    position=models.ForeignKey(Position,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')])
    degree = models.CharField(max_length=20, choices=[('Đại học', 'Đại học'), ('Cao đẳng', 'Cao đẳng')])
    major = models.CharField(max_length=100)
    contract_period = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
         return f'Profile: {self.user.username}'
   

class TopicLetter(models.Model):
  name = models.CharField(max_length=50)
  
  def __str__(self):
      return self.name


class Letter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    topic = models.ForeignKey(TopicLetter, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=30, choices=[('Đang xử lý', 'Đang xử lý'),('Đã xử lý', 'Đã xử lý')], default='Đang xử lý')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.is_anonymous:
            title = f'Thư của {self.user} - {self.topic.name}'
        else:
            title = f'Thư ẩn danh - {self.topic.name}'
        return title


class Sheet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    checkin=models.TimeField()
    checkout=models.TimeField(blank=True, null=True)
    work_hour=models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    salary=models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    status=models.CharField(max_length=20, choices=[('Đúng Giờ', 'Đúng Giờ'), ('Đến Muộn', 'Đến Muộn'), ('Về Sớm', 'Về Sớm')], default='Đúng Giờ')
    ot = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return f'{self.user.username} - {self.date}'


    def update_status(self):
        # Check if the user is late (after 8 AM) or leaves early (before 6 PM)
        if self.checkin > time(8, 0, 0):
            self.status = 'Đến Muộn'
        elif self.checkout and self.checkout < time(18, 0, 0):
            self.status = 'Về Sớm'
        else:
            self.status = 'Đúng Giờ'
        
        # Calculate overtime (OT) if checkout time is after 6 PM
        self.ot = max(0, int(self.work_hour - 10))



    def calculate_salary(self):
        profile = Profile.objects.get(user=self.user)
        # if self.work_hour is not None:
        #     if self.status == 'Muộn':
        #         salary_1hour = profile.position.department.salary * Decimal(0.8)
        #     else:
        #         salary_1hour = profile.position.department.salary
        #     rate = profile.position.salary_coef * salary_1hour
        #     self.salary = rate * Decimal(self.work_hour)
        # else:
        #     self.salary = 0

        self.salary = profile.position.salary_coef * profile.position.department.salary

    def save(self, *args, **kwargs):
        if self.checkin and self.checkout:
            checkin = timezone.datetime.combine(self.date, self.checkin)
            checkout = timezone.datetime.combine(self.date, self.checkout)
            self.work_hour = (checkout - checkin).seconds/3600

        self.update_status()
        self.calculate_salary()
        super().save( *args, **kwargs)