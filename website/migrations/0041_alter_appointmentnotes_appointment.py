# Generated by Django 4.1.1 on 2022-10-04 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0040_appointmentnotes_medications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentnotes',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='appointment', serialize=False, to='website.appointment', unique=True),
        ),
    ]
