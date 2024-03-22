# custum tags are defined here

from django import template

register = template.Library()

# Renders header as a component on the page, passing in the tags from parent context_dict
@register.inclusion_tag('CheeseBoardSite/header.html')
def render_header(tags):
    return {'tags': tags}

# Renders a grid showing all the posts
@register.inclusion_tag('CheeseBoardSite/post_grid.html')
def render_post_grid(posts, list_flag):
    return {'posts': posts,
            'list_flag': list_flag}

# Renders a single post
@register.inclusion_tag('CheeseBoardSite/post_card.html')
def render_post(post):
    return {'post': post}

# Renders a single comment
@register.inclusion_tag('CheeseBoardSite/comment.html')
def render_comment(comment):
    return {'comment': comment}

# Renders a single post as card for list
@register.inclusion_tag('CheeseBoardSite/post_list_card.html')
def render_post_list_card(post):
    return {'post': post}