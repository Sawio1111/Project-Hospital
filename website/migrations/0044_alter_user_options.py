# Generated by Django 4.1.1 on 2022-10-07 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0043_opinion_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('client', 'Hospital patient'), ('doctor', 'Hospital worker'), ('administrator', 'Website management'))},
        ),
    ]
