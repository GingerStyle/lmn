from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import Venue, Artist, Note, Show, LikeNote
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm
from django.db.models import Count, Max
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST' :

        form = NewNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.posted_date = timezone.now()
            note.save()
            return redirect('lmn:note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , { 'form' : form , 'show':show })



def latest_notes(request):
    notes = Note.objects.all().order_by('posted_date').reverse()
    return render(request, 'lmn/notes/note_list.html', {'notes':notes})


def notes_for_show(request, show_pk):   # pk = show pk

    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('posted_date').reverse()
    show = Show.objects.get(pk=show_pk)  # Contains artist, venue

    return render(request, 'lmn/notes/note_list.html', {'show': show, 'notes':notes } )


def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html' , {'note' : note })

@login_required
def add_note_like(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    user = request.user
    try:
        query = LikeNote.objects.filter(note=note_pk)
        like = query.get(user=user.pk)
        if like.value != 1:
            note.add_like()
        like.like()
    except LikeNote.DoesNotExist:
        like = LikeNote(note=note, user=user, value=0)
        like.save()
        like.like()
        note.add_like()
    return render(request, 'lmn/notes/note_detail.html', {'note': note })

@login_required
def add_note_dislike(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    user = request.user
    try:
        query = LikeNote.objects.filter(note=note_pk)
        like = query.get(user=user.pk)
        if like.value != -1:
            note.add_dislike()
        like.dislike()
    except LikeNote.DoesNotExist:
        like = LikeNote(note=note, user=note, value=0)
        like.save()
        like.dislike()
        note.add_dislike()
    return render(request, 'lmn/notes/note_detail.html', {'note': note})


def popular_notes(request):
    notes = Note.objects.all().order_by('rating', 'likes').reverse()
    return render(request, 'lmn/notes/note_list.html', {'notes': notes})

@login_required
def edit_note(request, note_pk):
    note = Note.objects.get(pk=note_pk)
    show = Show.objects.get(pk=note.show_id)
    if request.user!=note.user:
        return redirect('lmn:latest_notes')
    if request.method=='POST':
        form = NewNoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            return redirect('lmn:note_detail', note_pk=note.pk)
    else:
        form = NewNoteForm(initial={'title': note.title, 'text': note.text, 'rating': note.rating, 'image': note.image})
        return render(request, 'lmn/notes/edit_note.html', {'show': show, 'note': note, 'form': form})


@login_required
def delete_note(request, note_pk):
    note = Note.objects.get(pk=note_pk)
    if request.user != note.user:
        return redirect('lmn:latest_notes')
    Note.objects.filter(pk=note_pk).delete()
    return redirect('lmn:latest_notes')


@login_required
def popular_shows(request):
    shows = Show.objects.annotate(notes=Count('note')).order_by('notes').reverse()
    return render(request, 'lmn/shows/show_list.html', {'shows': shows})
