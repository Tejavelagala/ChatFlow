# Generated migration for unique_together constraint

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0014_remove_message_reactions_userprofile_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chatroommember',
            unique_together={('user', 'room')},
        ),
    ]
