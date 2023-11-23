
from django.db import models


class VisitorLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_name = models.CharField(max_length=255, null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    is_unique = models.BooleanField(default=True, null=True)

    def save(self, *args, **kwargs):
        if not self.session_key:
            self.session_key = self.generate_session_key()

        super().save(*args, **kwargs)

    def generate_session_key(self):
        if self.user_name:
            return f"registered_{self.user_name}_{self.ip_address}_{self.timestamp}"
        else:
            return f"unregistered_{self.ip_address}_{self.timestamp}" 
        
    def __str__(self):
        return f"{self.user_name} ({self.session_key}): {self.ip_address} - {self.timestamp}"