# Generated by Django 4.2.16 on 2024-11-26 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0002_loanoption_loanproducts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanoption',
            old_name='clcrdt_lend_rate_type',
            new_name='crdt_lend_rate_type',
        ),
        migrations.RenameField(
            model_name='loanoption',
            old_name='clcrdt_lend_rate_type_nm',
            new_name='crdt_lend_rate_type_nm',
        ),
    ]
