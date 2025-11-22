from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail  # Import send_mail
from .models import Event, Attendee
from .forms import EventForm, AttendeeForm

def index(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'rsvp/index.html', {'events': events})

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'rsvp/create_event.html', {'form': form})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = event.attendees.filter(is_confirmed=True).order_by('-created_at')
    
    # Check if event is nearly full (within 10% of capacity)
    is_nearly_full = event.current_attendees >= event.max_attendees * 0.9 and not event.is_full
    
    form = AttendeeForm(initial={'is_attending': True}, event=event)
    
    if request.method == 'POST':
        form = AttendeeForm(request.POST, event=event)
        if form.is_valid():
            with transaction.atomic():
                attendee = form.save(commit=False)
                attendee.event = event
                if not event.is_full or not attendee.is_attending:
                    attendee.is_confirmed = True
                    attendee.save()
                    
                    # --- EMAIL SENDING LOGIC ---
                    # Prepare email content
                    subject = f'RSVP Confirmation for {event.title}'
                    message = f"""
                    Dear {attendee.name},

                    This is to confirm your RSVP for the event:

                    Event: {event.title}
                    Date: {event.date.strftime('%B %d, %Y at %I:%M %p')}
                    Location: {event.location}

                    We look forward to seeing you there!

                    Best regards,
                    The Event Team
                    """
                    
                    # Send the email
                    try:
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
                            recipient_list=[attendee.email],
                            fail_silently=False,  # Set to True in production to avoid crashes
                        )
                        messages.success(request, 'RSVP submitted successfully! A confirmation email has been sent.')
                    except Exception as e:
                        # Handle potential email sending errors
                        messages.success(request, 'RSVP submitted successfully!')
                        messages.error(request, f'RSVP confirmed, but there was an issue sending the confirmation email: {str(e)}')
                    
                    # --- END EMAIL SENDING LOGIC ---
                    
                    return redirect('success')
                else:
                    messages.error(request, 'Sorry, this event is full!')
    
    return render(request, 'rsvp/event_detail.html', {
        'event': event,
        'attendees': attendees,
        'form': form,
        'is_full': event.is_full,
        'is_nearly_full': is_nearly_full,
        'capacity_percentage': event.capacity_percentage
    })

def success(request):
    return render(request, 'rsvp/success.html')