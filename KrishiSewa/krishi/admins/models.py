from django.contrib.auth.models import User
from django.db import models

class Ticket(models.Model):
    category_types = [
        ('Product', 'Product'),
        ('Equipment', 'Equipment'),
        ('User', 'User'),
    ]

    status_types = [
        ('Resolved', 'Resolved'),
        ('Pending', 'Pending'),
    ]

    title = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=category_types, default='Product')
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=status_types, default='Pending')
    ticket_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class TicketResponse(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    response = models.TextField()
    response_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    response_date = models.DateTimeField(auto_now_add=True)
    
