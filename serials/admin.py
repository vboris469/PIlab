from django.contrib import admin
from serials.models import *


class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 1


class SerialAdmin(admin.ModelAdmin):
    inlines = [EpisodeInline]


class LinkInline(admin.StackedInline):
    model = Link
    extra = 1


class EpisodeAdmin(admin.ModelAdmin):
    inlines = [LinkInline]


admin.site.register(Serial, SerialAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Link)