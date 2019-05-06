from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    is_active = models.BooleanField(default=True)

    timestamp = models.DateTimeField(auto_now=True)
    update_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
