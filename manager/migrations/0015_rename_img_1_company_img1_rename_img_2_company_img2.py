# Generated by Django 4.0.4 on 2022-05-20 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0014_remove_companyimg_company_company_img_1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='img_1',
            new_name='img1',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='img_2',
            new_name='img2',
        ),
    ]
