# Generated by Django 5.0.5 on 2024-10-30 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='pms',
            field=models.CharField(blank=True, choices=[('Apaleo', 'Apaleo PMS')], max_length=50, null=True),
        ),
    ]