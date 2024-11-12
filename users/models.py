import base64

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django import forms


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('author', 'Автор'),
        ('tester', 'Тестировщик'),
    )
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    avatar_base64 = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def save_avatar(self, avatar_file):
        """
        This method encodes the avatar file in base64 and saves it in the database.
        """
        if avatar_file:
            encoded_string = base64.b64encode(avatar_file.read()).decode('utf-8')
            self.avatar_base64 = encoded_string
            self.save()


User = get_user_model()


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    testers = models.ManyToManyField(User, related_name='teams', blank=True)

    def __str__(self):
        return self.name


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')
    middle_name = forms.CharField(max_length=30, required=False, label='Отчество')
    avatar = forms.ImageField(required=False, label='Аватар')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'avatar']

    def save(self, commit=True):
        user = super(ProfileEditForm, self).save(commit=False)
        if 'avatar' in self.cleaned_data and self.cleaned_data['avatar']:
            user.save_avatar(self.cleaned_data['avatar'])
        if commit:
            user.save()
        return user


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
    duration = models.CharField(max_length=12, blank=True, null=True)  # MM:SS:ms

    def __str__(self):
        return f"TestResult for {self.test} by {self.tester.username} from {self.start} to {self.end}"

    def save(self, *args, **kwargs):
        if self.start and self.end:
            duration_td = self.end - self.start
            minutes, seconds = divmod(duration_td.total_seconds(), 60)
            milliseconds = duration_td.microseconds // 1000
            self.duration = f"{int(minutes):02}:{int(seconds):02}:{milliseconds:03}"
        super().save(*args, **kwargs)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} at {self.timestamp}'