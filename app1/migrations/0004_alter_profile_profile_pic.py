# Generated by Django 4.2.2 on 2024-01-23 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='image/profile_pic/default.jpg', upload_to='image/profile_pic/'),
        ),
    ]
