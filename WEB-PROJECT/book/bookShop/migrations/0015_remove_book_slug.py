# Generated by Django 3.2.4 on 2021-11-30 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookShop', '0014_book_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='slug',
        ),
    ]