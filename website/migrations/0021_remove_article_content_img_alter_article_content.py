# Generated by Django 4.1.1 on 2022-10-02 23:27

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_article_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='content_img',
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
