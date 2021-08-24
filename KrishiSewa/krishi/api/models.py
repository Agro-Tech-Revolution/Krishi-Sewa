from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user_choices = [
        ("Farmers", "Farmers"),
        ("Vendors", "Vendors"),
        ("Buyers", "Buyers"),
        ("Admins", "Admins"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_type = models.CharField(max_length=50, choices=user_choices)
    contact = models.IntegerField(null=True, blank=True)
    profile_pic = models.CharField(max_length=500,
                                   null=True,
                                   default='static/profile_pic/default_profile.jpg')
    address = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)


class ReportUser(models.Model):
    categories = [
        ("False Information", "False Information"),
        ("Fake Account", "Fake Account"),
        ("Posts Disturbing content", "Posts Disturbing content"),
        ("Something Else", "Something Else"),
    ]

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='reported_user')
    report_category = models.CharField(max_length=50, choices=categories, default="Fake Account")
    report_description = models.CharField(max_length=200)
    reported_date = models.DateTimeField(auto_now_add=True)






