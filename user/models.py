from django.db import models

class User(models.Model):
    """
    User model to store user information.
    """
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    mobile_country_code = models.CharField(max_length=5, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']
        # Adding indexes for faster lookups
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['mobile_number']),
        ]
        
    def __str__(self):
        return self.email
    

class UserAccount(models.Model):
    """
    User account model to store user account information.
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=255, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        db_table = 'user_account'
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'
        ordering = ['user']
        indexes = [
            models.Index(fields=['user']),

        ]
   
        
    def __str__(self):
        return f"{self.username} - {self.user.email}"

