# Generated by Django 4.1.2 on 2022-11-04 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0014_remove_listings_closed_listings_close_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comments",
            old_name="comment",
            new_name="comment_text",
        ),
    ]
