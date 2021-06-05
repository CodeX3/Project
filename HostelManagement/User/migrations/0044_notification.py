# Generated by Django 3.2 on 2021-06-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0043_auto_20210525_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('msg', models.CharField(max_length=100)),
                ('pic', models.ImageField(blank=True, upload_to='')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('temp', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
