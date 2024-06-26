from django.contrib.auth.models import AbstractUser
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
    testers = models.ManyToManyField(User, related_name='assigned_tests')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, default='Unnamed Test')

    def __str__(self):
        return f"{self.name} by {self.user.username} at {self.created_at}"


class TestImage(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    image = models.TextField()  # Base64 encoded image
    rectangles = models.JSONField()
    points = models.JSONField()

    def __str__(self):
        return f"Test Image for {self.test} ({self.image})"


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_results')
    tester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f"TestResult for {self.test} by {self.tester.username} from {self.start} to {self.end}"
