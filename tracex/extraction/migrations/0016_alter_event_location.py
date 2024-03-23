# Generated by Django 5.0.2 on 2024-03-23 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extraction', '0015_trace_cohort'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(choices=[('Home', 'Home'), ('Hospital', 'Hospital'), ('Doctors', 'Doctors')], max_length=25),
        ),
    ]