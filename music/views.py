from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from web.models import Artist
from .forms import ArtistSelectionForm
from .templates import *

@login_required
def artist_selection_view(request):
    form = ArtistSelectionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():

        selected_artist = form.cleaned_data['artist']

        return redirect('song_selection', artist_id=selected_artist.id)
    context = {
        'form': form,
        'artists': Artist.objects.all()
    }
    return render(request, 'artist_selection.html', context)

@login_required
def song_selection_view(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    context = {'artist': artist}
    return render(request, 'song_selection.html', context)

@login_required
def base_song_selection_view(request):
    return render(request, 'song_selection.html')