# Generated by Django 4.2.16 on 2024-11-20 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0003_depositproducts_dcls_end_day_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='cur_con',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
