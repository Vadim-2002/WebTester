from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('author', 'Автор'),
        ('tester', 'Тестировщик'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


User = get_user_model()


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test by {self.user.username} at {self.created_at}"


class TestImage(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='test_images/')
    rectangles = models.JSONField()
    points = models.JSONField()

    def __str__(self):
        return f"Test Image for {self.test} ({self.image})"
