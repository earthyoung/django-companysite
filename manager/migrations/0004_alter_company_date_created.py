# Generated by Django 4.0.4 on 2022-05-16 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_company_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
