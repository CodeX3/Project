# Generated by Django 3.1.7 on 2021-03-26 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_student_sd_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='sd_email',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
