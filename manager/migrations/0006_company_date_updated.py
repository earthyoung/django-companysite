# Generated by Django 4.0.4 on 2022-05-19 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_companyimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
