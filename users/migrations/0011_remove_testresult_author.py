# Generated by Django 5.0.6 on 2024-06-18 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_test_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='author',
        ),
    ]
