from django.contrib import admin
from processor.models import Image, Descriptor


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ('title', 'id', 'created')
    filter_horizontal = ('descriptor',)


class DescriptorAdmin(admin.ModelAdmin):
    model = Descriptor
    list_display = ('tag', 'keyPoint_1', 'keyPoint_2')


admin.site.register(Image, ImageAdmin)
admin.site.register(Descriptor, DescriptorAdmin)