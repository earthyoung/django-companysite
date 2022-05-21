# Generated by Django 4.0.4 on 2022-05-20 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0013_alter_companyimg_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyimg',
            name='company',
        ),
        migrations.AddField(
            model_name='company',
            name='img_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company1', to='manager.companyimg'),
        ),
        migrations.AddField(
            model_name='company',
            name='img_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company2', to='manager.companyimg'),
        ),
    ]