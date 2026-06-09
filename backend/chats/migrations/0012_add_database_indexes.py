# Generated migration for database indexes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0011_alter_chatroommember_unique_together_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='chatroommember',
            index=models.Index(fields=['room'], name='chats_chatr_room_idx'),
        ),
        migrations.AddIndex(
            model_name='chatroommember',
            index=models.Index(fields=['user'], name='chats_chatr_user_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['room', '-timestamp'], name='chats_messag_room_ts_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['sender'], name='chats_messag_sender_idx'),
        ),
    ]
