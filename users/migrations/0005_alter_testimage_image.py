# Generated by Django 5.0.6 on 2024-06-15 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_test_image_remove_test_points_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimage',
            name='image',
            field=models.TextField(),
        ),
    ]
