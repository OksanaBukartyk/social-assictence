# Generated by Django 3.0.8 on 2021-05-20 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='address',
            field=models.TextField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to='images'),
        ),
    ]
