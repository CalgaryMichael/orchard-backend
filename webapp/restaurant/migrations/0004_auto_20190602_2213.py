# Generated by Django 2.2.1 on 2019-06-02 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20190602_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='violation',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
