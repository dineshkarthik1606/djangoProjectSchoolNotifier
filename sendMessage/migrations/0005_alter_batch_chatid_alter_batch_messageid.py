# Generated by Django 4.2.3 on 2023-07-30 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendMessage', '0004_alter_batch_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='chatID',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='batch',
            name='messageID',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
