from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=300)
    max_attendees = models.PositiveIntegerField(default=100)
    event_image = models.ImageField(
        upload_to='event_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def current_attendees(self):
        return self.attendees.filter(is_confirmed=True).count()

    @property
    def is_full(self):
        return self.current_attendees >= self.max_attendees
        
    @property
    def capacity_percentage(self):
        if self.max_attendees == 0:
            return 0
        return int((self.current_attendees / self.max_attendees) * 100)

class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees') # Ensure related_name is 'attendees'
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    is_attending = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    dietary_restrictions = models.TextField(blank=True)
    plus_one = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    class Meta:
        unique_together = ['event', 'email']