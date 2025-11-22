from django import forms
from .models import Event, Attendee

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'max_attendees', 'event_image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'max_attendees': forms.NumberInput(attrs={'class': 'form-control'}),
            'event_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event_image'].required = False

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'email', 'phone', 'is_attending', 'dietary_restrictions', 'plus_one', 'notes']
        widgets = {
            'dietary_restrictions': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any dietary restrictions or allergies', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any additional notes', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_attending': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plus_one': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.event and Attendee.objects.filter(event=self.event, email=email).exists():
            raise forms.ValidationError("This email has already RSVP'd for this event.")
        return email