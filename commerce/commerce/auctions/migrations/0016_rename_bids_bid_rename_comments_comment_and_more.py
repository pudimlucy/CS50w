# Generated by Django 4.1.2 on 2022-11-04 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0015_rename_comment_comments_comment_text"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Bids",
            new_name="Bid",
        ),
        migrations.RenameModel(
            old_name="Comments",
            new_name="Comment",
        ),
        migrations.RenameModel(
            old_name="Listings",
            new_name="Listing",
        ),
        migrations.RenameModel(
            old_name="Watches",
            new_name="Watch",
        ),
    ]
