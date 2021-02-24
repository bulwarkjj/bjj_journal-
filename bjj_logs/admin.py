from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Topic, Entry, Youtube


class YoutubeAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(Youtube, YoutubeAdmin)
admin.site.register(Topic)
admin.site.register(Entry)


