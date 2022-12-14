# Generated by Django 4.1.2 on 2022-10-28 16:34

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="listings",
            name="category",
            field=models.CharField(default=("ETC", "Everything Else"), max_length=250),
        ),
        migrations.AddField(
            model_name="listings",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="listings",
            name="image_link",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="listings",
            name="start_price",
            field=djmoney.models.fields.MoneyField(
                decimal_places=2,
                default=Decimal("0"),
                default_currency="USD",
                max_digits=19,
            ),
        ),
    ]
