# Generated by Django 3.0.5 on 2022-06-14 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0019_auto_20220614_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='assignedDoctorId',
            field=models.PositiveIntegerField(),
        ),
    ]