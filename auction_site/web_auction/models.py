from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)

    # Override default related names to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    priority = models.IntegerField()
    image = models.ImageField(upload_to='auction_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    bidder_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for auction {self.auction.title} by {self.bidder_name}"