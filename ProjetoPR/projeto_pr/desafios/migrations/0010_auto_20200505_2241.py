# Generated by Django 3.0.4 on 2020-05-05 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desafios', '0009_auto_20200505_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
