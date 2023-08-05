# Generated by Django 4.1.2 on 2022-10-28 21:17

from django.db import migrations, models
import django_finances.transactions.validators


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_add_recurring_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurringtransaction',
            name='recurrence',
            field=models.TextField(validators=[django_finances.transactions.validators.validate_rrule], verbose_name='recurrence'),
        ),
    ]
