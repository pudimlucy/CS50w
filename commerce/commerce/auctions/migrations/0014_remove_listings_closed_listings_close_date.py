# Generated by Django 4.1.2 on 2022-11-04 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0013_alter_bids_bid_value"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listings",
            name="closed",
        ),
        migrations.AddField(
            model_name="listings",
            name="close_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
