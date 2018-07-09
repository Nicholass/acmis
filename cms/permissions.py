from pybb.compat import is_authenticated
from django.db.models import Q
from pybb import defaults
from pybb.permissions import DefaultPermissionHandler


class HiddenForumPermissionHandler(DefaultPermissionHandler):
    def __init__(self, *args, **kwargs):
        super(HiddenForumPermissionHandler, self).__init__(*args, **kwargs)

    #
    # permission checks on forums
    #
    def filter_forums(self, user, qs):
        """ return a queryset with forums `user` is allowed to see """
        if user.is_superuser:
            return qs

        return qs.filter(Q(hidden=False) | Q(hidden=True, groups__groups__in=list(user.groups.all())) & Q(category__hidden=False))

    def may_view_forum(self, user, forum):
        """ return True if user may view this forum, False if not """
        if user.is_superuser:
            return True

        return forum.hidden == False or (forum.hidden == True and len(set(forum.groups.groups.all()) & set(user.groups.all())) > 0) and forum.category.hidden == False

    #
    # permission checks on topics
    #
    def filter_topics(self, user, qs):
        """ return a queryset with topics `user` is allowed to see """
        if user.is_superuser:
            return qs
        if user.has_perm('pybb.change_topic'):
            # if I can edit, I can view
            return qs

        qs = qs.filter(Q(forum__hidden=False) | Q(forum__hidden=True, forum__groups__groups__in=list(user.groups.all())) & Q(forum__category__hidden=False))
        if is_authenticated(user):
            qs = qs.filter(
                # moderator can view on_moderation
                Q(forum__moderators=user) |
                # author can view on_moderation only if there is one post in the topic
                # (mean that post is owned by author)
                Q(user=user, post_count=1) |
                # posts not on_moderation are accessible
                Q(on_moderation=False)
            )
        else:
            qs = qs.filter(on_moderation=False)
        return qs.distinct()

    def may_view_topic(self, user, topic):
        """ return True if user may view this topic, False otherwise """
        if self.may_moderate_topic(user, topic):
            # If i can moderate, it means I can view.
            return True
        if topic.on_moderation:
            if not topic.head.on_moderation:
                # topic is in general moderation waiting (it has been marked as on_moderation
                # but my post is not on_moderation. So it's a manual action we MUST respect)
                return False
            if topic.head.on_moderation and topic.head.user != user:
                # topic is on moderation because of the first post but this is not my post
                # User must not access to it, only it's author can do in moderation mode
                return False
        return (not topic.forum.hidden or
                (topic.forum.hidden == True and len(set(topic.forum.groups.groups.all()) & set(user.groups.all())) > 0)
                and not topic.forum.category.hidden)

    #
    # permission checks on posts
    #
    def filter_posts(self, user, qs):
        """ return a queryset with posts `user` is allowed to see """

        # first filter by topic availability
        if user.is_superuser:
            return qs
        if user.has_perm('pybb.change_post'):
            # If I can edit all posts, I can view all posts
            return qs

            query = (Q(topic__forum__hidden=False, topic__forum__category__hidden=False) |
                     Q(topic__forum__hidden=True, topic__forum__groups__groups__in=list(user.groups.all())))
        else:
            query = Q(pk__isnull=False)
        if defaults.PYBB_PREMODERATION:
            # remove moderated posts
            query = query & Q(on_moderation=False, topic__on_moderation=False)
        if is_authenticated(user):
            # cancel previous remove if it's my post, or if I'm moderator of the forum
            query = query | Q(user=user) | Q(topic__forum__moderators=user)
        return qs.filter(query).distinct()

    def may_view_post(self, user, post):
        """ return True if `user` may view `post`, False otherwise """
        if user.is_superuser:
            return True
        if self.may_edit_post(user, post):
            # if I can edit, I can view
            return True
        if defaults.PYBB_PREMODERATION and (post.on_moderation or post.topic.on_moderation):
            return False

        return (not post.topic.forum.hidden or
                                 (post.topic.forum.hidden == True and len(set(post.topic.forum.groups.groups.all()) & set(user.groups.all())) > 0)
                                 and not post.topic.forum.category.hidden)
