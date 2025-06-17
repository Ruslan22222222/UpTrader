from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    name = models.CharField(_('Название меню'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('Меню')
        verbose_name_plural = _('Меню')

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(_('Название пункта меню'), max_length=100)
    url = models.CharField(_('URL'), max_length=255, blank=True)
    named_url = models.CharField(_('Named URL'), max_length=100, blank=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Пункт меню')
        verbose_name_plural = _('Пункты меню')
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.url
