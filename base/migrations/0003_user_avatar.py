# Generated by Django 4.0.2 on 2022-02-21 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_bio_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]
