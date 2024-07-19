from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from nblog.models import Post

register = template.Library()


@register.simple_tag
def related_posts(post_id):
    post = Post.objects.get(id=post_id)
    tags = post.tag.all()
    related_posts = Post.objects.filter(tag__in=tags).exclude(id=post_id)

    # Count the number of times each related post appears
    related_posts_count = {}
    for related_post in related_posts:
        count = 1
        for tag in related_post.tag.all():
            if tag in tags:
                count += 1
        related_posts_count[related_post] = count

    # Sort related posts by count in descending order
    related_posts_sorted = sorted(related_posts_count.items(), key=lambda x: x[1], reverse=True)

    # Return the related posts, without tag counts
    return [related_post[0] for related_post in related_posts_sorted][:4]


