# rooms/admin.py
from django.contrib import admin
from .models import Room, Player, Tutorial, TutorialCategory

# Register Room and Player models
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic')
    search_fields = ('id', 'topic__name')
    list_filter = ('topic',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'room', 'total_score')
    list_filter = ('role', 'room')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'role', 'room')
        }),
        ('Scoring', {
            'fields': ('content_score', 'style_score', 'strategy_score', 'poi_score', 'total_score', 'notes')
        })
    )

# Register Tutorial Category model
@admin.register(TutorialCategory)
class TutorialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'order')
    search_fields = ('name',)
    list_editable = ('order',)

# Register Tutorial model with custom admin
@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'category', 'featured', 'order')
    list_filter = ('resource_type', 'category', 'featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured', 'order')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'slug', 'category', 'resource_type', 'icon_class')
        }),
        ('Display Options', {
            'fields': ('featured', 'order'),
        }),
        ('Resource Details', {
            'fields': ('file', 'url', 'external_link', 'length', 'doc_image'),  # 🔥 added doc_image here
            'classes': ('collapse',),
            'description': 'For documents, PDFs, and external resources'
        }),
        ('Video Options', {
            'fields': ('video_embed_url', 'duration'),
            'classes': ('collapse',),
            'description': 'For video tutorials only'
        }),
    )

    def get_fieldsets(self, request, obj=None):
        """Show relevant fields based on resource type"""
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.resource_type == 'video':
            # For video resources, expand the video section
            fieldsets[3][1]['classes'] = ()  # Remove 'collapse' class
        elif obj and obj.resource_type in ['pdf', 'article', 'guide']:
            # For reading materials, expand the resource details section
            fieldsets[2][1]['classes'] = ()  # Remove 'collapse' class
        return fieldsets
