# Generated by Django 4.0.4 on 2022-05-17 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_company_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
    ]
