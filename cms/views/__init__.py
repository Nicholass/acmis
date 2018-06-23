from .comment import comment_reply, comment_new, comment_edit, comment_delete
from .map import serve_map_file
from .post import post_new, post_list, post_edit, post_detail, post_delete, post_publish, post_unpublish, post_approve, post_disapproved
from .registration import registration, activation, send_activation_code, remember_login, edit_email, edit_email_done
from .profile import profile, profile_edit, owner_profile
from .ajax import get_simular_tags
from .sitemap import CategoriesSitemap, PostsSitemap, StaticSitemap
from .rss import LatestEntriesFeed