# Generated by Django 4.1.1 on 2022-10-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0039_alter_appointmentnotes_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentnotes',
            name='medications',
            field=models.CharField(max_length=2048, null=True),
        ),
    ]