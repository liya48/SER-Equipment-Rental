from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

class Equipment(models.Model):
    Equipment_types=[
          ('Crane', 'Crane'),
        ('JCB', 'JCB'),
        ('Generator', 'Generator'),
        ('Scaffolding', 'Scaffolding'),
        ('Road Roller', 'Road Roller'),
        ('Dump Truck', 'Dump Truck'),
        ('Concrete Mixer', 'Concrete Mixer'),
        ('Manlift', 'Manlift'),
        ('Telehandler', 'Telehandler'),
        ('Piling Machine', 'Piling Machine'),
    ]
    supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50, choices=Equipment_types)
    description = models.TextField()
    rent_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class RentalRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.buyer.username} - {self.equipment.name}"

    
