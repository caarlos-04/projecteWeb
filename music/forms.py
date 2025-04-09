from django import forms
from web.models import Artist

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name']


class ArtistSelectionForm(forms.Form):
    artist = forms.ModelChoiceField(
        queryset=Artist.objects.all(),  # type: ignore
        empty_label="Selecciona un artista"
    )