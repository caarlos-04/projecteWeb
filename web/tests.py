from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from web.models import Playlist, Track, Album, Artist
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class MusicTests(StaticLiveServerTestCase):
    """Pruebas integradas para la aplicación musical (unitarias y E2E)"""

    def setUp(self):
        """Configuración inicial para todas las pruebas"""
        # Crear usuarios para probar restricciones de acceso
        self.user1 = User.objects.create_user(username="user1", password="password1_")
        self.user2 = User.objects.create_user(username="user2", password="password2_")

        # Crear artistas, álbumes y canciones para las pruebas
        self.artist1 = Artist.objects.create(name="The Beatles")
        self.artist2 = Artist.objects.create(name="Coldplay")

        self.album1 = Album.objects.create(title="Abbey Road", artist=self.artist1)
        self.album2 = Album.objects.create(title="A Night at the Opera", artist=self.artist2)

        self.track1 = Track.objects.create(title="Come Together", album=self.album1, artist=self.artist1)
        self.track2 = Track.objects.create(title="Something", album=self.album1, artist=self.artist1)
        self.track3 = Track.objects.create(title="Bohemian Rhapsody", album=self.album2, artist=self.artist2)

        # Crear playlists para cada usuario
        self.playlist1 = Playlist.objects.create(title="Rock Clásico", user=self.user1)
        self.playlist1.tracks.add(self.track1, self.track3)

        self.playlist2 = Playlist.objects.create(title="Para Estudiar", user=self.user2)
        self.playlist2.tracks.add(self.track2)

        # Cliente para simular navegador
        self.client = Client()

    # PRUEBAS DE AUTENTICACIÓN Y SEGURIDAD

    def test_redirect_to_login_if_not_authenticated(self):
        """Verificar redirección al login cuando no hay autenticación"""
        self.client.logout()
        response = self.client.get(reverse('music_info'))
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('music_info'),
                             fetch_redirect_response=False)

    def test_authentication_required(self):
        """E2E: Verificar que se requiere autenticación para acceder a las funcionalidades"""
        self.client.logout()
        response = self.client.get(reverse('playlists'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('save_track_to_playlist'), {
            'track_title': self.track1.title,
            'album_title': self.album1.title,
            'artist_name': self.artist1.name,
            'new_playlist_title': 'No debería crearse'
        })
        self.assertEqual(response.status_code, 302)
        self.client.login(username="user1", password="password1_")
        response = self.client.get(reverse('playlists'))
        self.assertNotContains(response, "No debería crearse")

    def test_security_restrictions(self):
        """E2E: Verificar restricciones de seguridad para acceso a playlists"""
        self.client.login(username="user2", password="password2_")
        response = self.client.post(reverse('delete_playlist', args=[self.playlist1.id]))
        self.assertEqual(response.status_code, 404)
        self.client.logout()
        self.client.login(username="user1", password="password1_")
        response = self.client.get(reverse('playlists'))
        self.assertContains(response, "Rock Clásico")
        self.client.logout()
        self.client.login(username="user2", password="password2_")
        response = self.client.get(reverse('playlists'))
        self.assertContains(response, "Para Estudiar")
        self.assertNotContains(response, "Rock Clásico")

    # PRUEBAS DE BÚSQUEDA Y VISUALIZACIÓN

    def test_search_artist_and_view_tracks(self):
        """Probar la búsqueda de artistas y visualización de canciones"""
        self.client.login(username="user1", password="password1_")
        response = self.client.get(reverse('music_info'), {'artist': 'Coldplay'})
        self.assertEqual(response.status_code, 200)

    def test_view_top_songs(self):
        """Probar la visualización de canciones más populares"""
        self.client.login(username="user1", password="password1_")
        response = self.client.get(reverse('top_songs_search'), {'artist': 'Coldplay'})
        self.assertEqual(response.status_code, 200)

    def test_view_playlists(self):
        """Probar la visualización de playlists del usuario"""
        self.client.login(username="user1", password="password1_")
        response = self.client.get(reverse('playlists'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rock Clásico')

    # PRUEBAS DE OPERACIONES CRUD INDIVIDUALES

    def test_create_new_playlist_and_add_track(self):
        """Probar la creación de una nueva playlist con una canción"""
        self.client.login(username="user1", password="password1_")
        response = self.client.post(reverse('save_track_to_playlist'), {
            'track_title': 'Believer',
            'album_title': 'Evolve',
            'artist_name': 'Imagine Dragons',
            'new_playlist_title': 'Nova Playlist'
        })
        self.assertEqual(response.status_code, 200)
        playlist = Playlist.objects.get(user=self.user1, title='Nova Playlist')
        self.assertTrue(playlist.tracks.filter(title='Believer').exists())

    def test_add_track_to_existing_playlist(self):
        """Probar la adición de una canción a una playlist existente"""
        self.client.login(username="user1", password="password1_")
        response = self.client.post(reverse('save_track_to_playlist'), {
            'track_title': self.track2.title,
            'album_title': self.album1.title,
            'artist_name': self.artist1.name,
            'playlist_id': self.playlist1.id
        })
        self.assertEqual(response.status_code, 200)
        self.playlist1.refresh_from_db()
        self.assertTrue(self.playlist1.tracks.filter(title=self.track2.title).exists())

    def test_remove_track_from_playlist(self):
        """Probar la eliminación de una canción de una playlist"""
        self.client.login(username="user1", password="password1_")
        response = self.client.post(
            reverse('remove_track_from_playlist', args=[self.playlist1.id, self.track1.id])
        )
        self.assertEqual(response.status_code, 302)
        self.playlist1.refresh_from_db()
        self.assertFalse(self.playlist1.tracks.filter(id=self.track1.id).exists())

    def test_delete_playlist(self):
        """Probar la eliminación de una playlist"""
        self.client.login(username="user1", password="password1_")
        response = self.client.post(reverse('delete_playlist', args=[self.playlist1.id]))
        self.assertRedirects(response, reverse('user_playlists'))
        self.assertFalse(Playlist.objects.filter(id=self.playlist1.id).exists())

    def test_error_handling_invalid_playlist(self):
        """Verificar manejo de errores al intentar acceder a una playlist inválida"""
        self.client.login(username="user1", password="password1_")
        response = self.client.get(reverse('delete_playlist', args=[99999]))
        self.assertEqual(response.status_code, 405)

    # PRUEBAS DE FLUJOS COMPLETOS (E2E)

    def test_create_playlist_workflow(self):
        """E2E: Flujo completo de creación de una playlist con varias canciones"""
        self.client.login(username="user1", password="password1_")
        response = self.client.get(reverse('music_info'), {'artist': 'Coldplay'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('save_track_to_playlist'), {
            'track_title': self.track3.title,
            'album_title': self.album2.title,
            'artist_name': self.artist2.name,
            'new_playlist_title': 'Mis Favoritos'
        })
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('playlists'))
        self.assertContains(response, 'Mis Favoritos')
        self.assertContains(response, self.track3.title)
        playlist = Playlist.objects.get(user=self.user1, title='Mis Favoritos')
        response = self.client.post(reverse('save_track_to_playlist'), {
            'track_title': self.track1.title,
            'album_title': self.album1.title,
            'artist_name': self.artist1.name,
            'playlist_id': playlist.id
        })
        response = self.client.get(reverse('playlists'))
        self.assertContains(response, self.track1.title)
        self.assertContains(response, self.track3.title)

    def test_update_playlist_workflow(self):
        """E2E: Flujo completo de actualización de una playlist"""
        self.client.login(username="user1", password="password1_")
        response = self.client.get(reverse('playlists'))
        self.assertContains(response, "Rock Clásico")
        self.assertContains(response, self.track1.title)
        self.assertContains(response, self.track3.title)
        response = self.client.post(
            reverse('remove_track_from_playlist', args=[self.playlist1.id, self.track1.id])
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('playlists'))
        self.assertContains(response, "Rock Clásico")
        self.assertNotContains(response, self.track1.title)
        self.assertContains(response, self.track3.title)
        response = self.client.post(reverse('save_track_to_playlist'), {
            'track_title': self.track2.title,
            'album_title': self.album1.title,
            'artist_name': self.artist1.name,
            'playlist_id': self.playlist1.id
        })
        response = self.client.get(reverse('playlists'))
        self.assertContains(response, "Rock Clásico")
        self.assertContains(response, self.track2.title)
