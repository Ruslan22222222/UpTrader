from django import template
from django.urls import reverse, resolve
from django.core.cache import cache
from menus.models import Menu, MenuItem

register = template.Library()


@register.inclusion_tag('menus/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    cache_key = f'menu_{menu_name}_{request.path}'
    cached_menu = cache.get(cache_key)

    if cached_menu:
        return cached_menu

    try:
        menu = Menu.objects.prefetch_related(
            'items',
            'items__children',
            'items__children__children'
        ).get(name=menu_name)

        current_path = request.path
        current_url_name = resolve(current_path).url_name

        def get_active_items(items):
            active_items = set()
            for item in items:
                item_url = item.get_url()
                if item.named_url == current_url_name or item_url == current_path:
                    active_items.add(item)
                    parent = item.parent
                    while parent:
                        active_items.add(parent)
                        parent = parent.parent
            return active_items

        active_items = get_active_items(menu.items.all())

        result = {
            'menu': menu,
            'active_items': active_items,
        }

        cache.set(cache_key, result, 3600)

        result['request'] = request
        return result

    except Menu.DoesNotExist:
        return {'menu': None}
