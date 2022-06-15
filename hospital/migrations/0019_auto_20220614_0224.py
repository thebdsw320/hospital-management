# Generated by Django 3.0.5 on 2022-06-14 02:24

from django.db import migrations, models
import django.db.models.deletion
import hospital.utils


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0018_auto_20201015_2036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientdischargedetails',
            old_name='OtherCharge',
            new_name='otherCharge',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='doctorId',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patientId',
        ),
        migrations.RemoveField(
            model_name='patientdischargedetails',
            name='patientId',
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctorID',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patientID',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='patientdischargedetails',
            name='patientID',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='id',
            field=models.CharField(default=hospital.utils.custom_id, max_length=11, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='department',
            field=models.CharField(choices=[('Cardiología', 'Cardiología'), ('Dermatología', 'Dermatología'), ('Emergencias', 'Emergencias'), ('Alergias', 'Alergias'), ('General', 'General')], default='General', max_length=50),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='id',
            field=models.CharField(default=hospital.utils.custom_id, max_length=11, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='assignedDoctorId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.Doctor'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='id',
            field=models.CharField(default=hospital.utils.custom_id, max_length=11, primary_key=True, serialize=False, unique=True),
        ),
    ]
