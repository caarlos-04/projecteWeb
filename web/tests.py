from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from web.models import Playlist, Track, Album, Artist

class MusicViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_redirect_to_login_if_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('music_info'))
        self.assertRedirects(response, reverse('spotify_login'))

    def test_search_artist_and_view_tracks(self):
        response = self.client.get(reverse('music_info'), {'artist': 'Shakira'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shakira")  # esperem que aparegui el nom

    def test_view_top_songs(self):
        response = self.client.get(reverse('top_songs'), {'artist': 'Coldplay'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Coldplay")

    def test_create_new_playlist_and_add_track(self):
        response = self.client.post(reverse('music_info'), {
            'track_title': 'Believer',
            'album_title': 'Evolve',
            'artist_name': 'Imagine Dragons',
            'new_playlist_title': 'Nova Playlist'
        })
        self.assertEqual(response.status_code, 302)  # redirecció després de guardar

        playlist = Playlist.objects.get(user=self.user, title='Nova Playlist')
        self.assertTrue(playlist.tracks.filter(title='Believer').exists())

    def test_add_track_to_existing_playlist(self):
        playlist = Playlist.objects.create(user=self.user, title='Workout')

        response = self.client.post(reverse('music_info'), {
            'track_title': 'Wake Me Up',
            'album_title': 'True',
            'artist_name': 'Avicii',
            'playlist_id': playlist.id
        })

        self.assertEqual(response.status_code, 302)
        playlist.refresh_from_db()
        self.assertTrue(playlist.tracks.filter(title='Wake Me Up').exists())

    def test_view_playlists(self):
        Playlist.objects.create(user=self.user, title='Chill Vibes')
        response = self.client.get(reverse('playlists'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chill Vibes')

    def test_delete_playlist(self):
        playlist = Playlist.objects.create(user=self.user, title='To Delete')

        response = self.client.post(reverse('delete_playlist', args=[playlist.id]))
        self.assertRedirects(response, reverse('playlists'))
        self.assertFalse(Playlist.objects.filter(id=playlist.id).exists())

    def test_remove_track_from_playlist(self):
        artist = Artist.objects.create(name="Adele")
        album = Album.objects.create(title="30", artist=artist)
        track = Track.objects.create(title="Easy On Me", album=album, artist=artist)
        playlist = Playlist.objects.create(user=self.user, title="Ballads")
        playlist.tracks.add(track)

        response = self.client.post(reverse('remove_track_from_playlist', args=[playlist.id, track.id]))
        self.assertRedirects(response, reverse('playlists'))

        playlist.refresh_from_db()
        self.assertFalse(playlist.tracks.filter(id=track.id).exists())

    def test_cannot_access_other_user_playlist(self):
        other_user = User.objects.create_user(username='otheruser', password='1234')
        Playlist.objects.create(user=other_user, title='Private')

        response = self.client.get(reverse('playlists'))
        self.assertNotContains(response, 'Private')
