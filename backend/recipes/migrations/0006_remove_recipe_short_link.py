# Generated by Django 4.2.15 on 2024-08-19 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_ingredient_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='short_link',
        ),
    ]
