from django.contrib import sitemaps
from django.urls import reverse


class StaticSiteMap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ['accounts:signup', 'accounts:register', 'accounts:logout', 'accounts:change_password', ]

    def location(self, item):
        return reverse(item)

