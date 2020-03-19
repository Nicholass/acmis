from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver
from webpush import send_user_notification
from django.conf import settings

from vendors.django_messages.models import Message
from .comment import Comment

@receiver(post_save, sender=Message)
def push_on_pm(sender, instance, created, **kwargs):
    message = Message.objects.get(pk=instance.pk)

    if created:
        payload = {
            'head': 'Нове повідомлення',
            'body': 'Ви отримали нове особисте повідомлення на сайті diggers.kiev.ua',
            'icon': getattr(settings, 'WEBPUSH_ICON_URL'),
            'url': reverse('messages_detail', kwargs={'message_id': message.pk}),
        }
        send_user_notification(user=message.recipient, payload=payload, ttl=1000)

@receiver(post_save, sender=Comment)
def push_on_reply(sender, instance, created, **kwargs):
    certain_comment = Comment.objects.get(pk=instance.pk)

    if created and certain_comment.parent:
        payload = {
            'head': 'Відповідь на ваш коментар',
            'body': 'Ви отримали відповідь на ваш коментар на сайті diggers.kiev.ua',
            'icon': getattr(settings, 'WEBPUSH_ICON_URL'),
            'url': '%s#comment%s' % (reverse('post_detail', kwargs={'pk': certain_comment.post.pk}), certain_comment.pk),
        }
        send_user_notification(user=certain_comment.parent.author, payload=payload, ttl=1000)
