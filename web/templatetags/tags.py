from django import template


register = template.Library()
@register.filter(name='in_category')
def in_category(item, category):
    return item.filter(comment=category)


@register.filter(name='count_reply')
def count_reply(item, category):
    tt =  item.filter(comment=category)
    return tt.count()