# Generated by Django 4.0.4 on 2022-05-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_alter_companyimg_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyimg',
            name='img',
            field=models.ImageField(blank=True, upload_to='C:\\Users\\USER\\Desktop\\KSY\\2022\\BoltAndNut\\assignment\\webproject\\media'),
        ),
    ]
