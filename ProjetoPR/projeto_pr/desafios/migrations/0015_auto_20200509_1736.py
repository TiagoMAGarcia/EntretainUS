# Generated by Django 3.0.4 on 2020-05-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desafios', '0014_comment_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]