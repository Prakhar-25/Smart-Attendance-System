# Generated by Django 5.1.1 on 2024-10-31 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recognition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('known_name', models.CharField(max_length=70)),
                ('known_encoding', models.BinaryField()),
            ],
        ),
    ]
