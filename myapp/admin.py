from django.contrib import admin
from .models import Event, Attendee

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'max_attendees', 'current_attendees', 'event_image']
    list_filter = ['date']
    search_fields = ['title', 'location']
    list_display_links = ['title']

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'event', 'is_attending', 'created_at']
    list_filter = ['event', 'is_attending', 'created_at']
    search_fields = ['name', 'email']