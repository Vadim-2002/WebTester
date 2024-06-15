# Generated by Django 5.0.6 on 2024-06-12 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='test_images/')),
                ('rectangles', models.JSONField()),
                ('points', models.JSONField()),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.test')),
            ],
        ),
    ]
