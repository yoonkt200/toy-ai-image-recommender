from django.contrib import admin
from processor.models import Image, Descriptor


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ('title', 'id', 'created')


admin.site.register(Image, ImageAdmin)