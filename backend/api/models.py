from django.db import models
from django.contrib.auth.models import User
import string
import random
from django.conf import settings

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class ExpenseGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    invite_code = models.CharField(max_length=10, unique=True, default=generate_invite_code)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='expense_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    group = models.ForeignKey(ExpenseGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='expenses')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    description = models.CharField(max_length=255)  # maps to remarks
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPE_CHOICES)

    payment_method = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    date = models.DateField()
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    group = models.ForeignKey(ExpenseGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('weekly', 'Weekly'), ('yearly', 'Yearly')])
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
     
def avatar_upload_to(instance, filename):
    # e.g. avatars/user_12/20251127_filename.jpg
    return f"avatars/user_{instance.user.id}/{filename}"

class UserSettings(models.Model):
    STORAGE_CHOICES = [
        ('local', 'LocalStorage'),
        ('pinia', 'Pinia'),
        ('supabase', 'Supabase'),
        ('firebase', 'Firebase'),
        ('vuex', 'Vuex'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    avatar = models.ImageField(upload_to=avatar_upload_to, null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    currency = models.CharField(max_length=10, default='USD')
    dark_mode = models.BooleanField(default=False)
    accent_color = models.CharField(max_length=9, default='#6366f1')
    sound = models.BooleanField(default=True)
    haptics = models.BooleanField(default=True)

    # Advanced
    app_lock_enabled = models.BooleanField(default=False)
    app_lock_pin_hash = models.CharField(max_length=256, null=True, blank=True)  # hashed PIN

    notifications_enabled = models.BooleanField(default=True)
    notifications_daily_summary = models.BooleanField(default=False)

    auto_backup_enabled = models.BooleanField(default=False)
    auto_backup_schedule = models.CharField(max_length=20, default='daily')
    storage_provider = models.CharField(max_length=20, choices=STORAGE_CHOICES, default='local')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.username}"    