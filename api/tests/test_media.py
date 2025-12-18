from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from api.models import User, Album, Photo

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class MediaTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            name="Photographer", username="photo_master", email="photo@test.com"
        )

        self.album = Album.objects.create(
            user=self.user,
            title="Tatil Anıları"
        )

        self.photo = Photo.objects.create(
            album=self.album,
            title="Manzara",
            url="https://via.placeholder.com/600/92c952",
            thumbnail_url="https://via.placeholder.com/150/92c952" 
        )


    # 1. ALBUM TESTLERİ

    # GET /api/albums/
    def test_list_albums(self):
        response = self.client.get('/api/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # POST /api/albums/
    def test_create_album(self):
        payload = {
            "userId": self.user.id,
            "title": "Yeni Albüm"
        }
        response = self.client.post('/api/albums/', payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Yeni Albüm")
        self.assertTrue(Album.objects.filter(title="Yeni Albüm").exists())

    # GET /api/albums/?user={id}
    def test_filter_albums_by_user(self):
        other_user = User.objects.create(name="X", username="x", email="x@x.com")
        Album.objects.create(user=other_user, title="X Album")

        response = self.client.get(f'/api/albums/?user={self.user.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['userId'], self.user.id)

    # DELETE /api/albums/{id}/
    def test_delete_album(self):
        response = self.client.delete(f'/api/albums/{self.album.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Album.objects.filter(id=self.album.id).exists())

    # 2. PHOTO TESTLERİ

    # GET /api/photos/
    def test_list_photos(self):
        response = self.client.get('/api/photos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # POST /api/photos/
    def test_create_photo(self):
        payload = {
            "albumId": self.album.id,
            "title": "Yeni Foto",
            "url": "http://test.com/img.jpg",
            "thumbnailUrl": "http://test.com/thumb.jpg" 
        }
        response = self.client.post('/api/photos/', payload, format='json')
        
        if response.status_code != 201:
            print(f"\nPhoto Create Error: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Yeni Foto")

    # GET /api/photos/?album={id}
    def test_filter_photos_by_album(self):
        other_album = Album.objects.create(user=self.user, title="Other")
        Photo.objects.create(album=other_album, title="Other Photo", url="...", thumbnail_url="...")

        response = self.client.get(f'/api/photos/?album={self.album.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['albumId'], self.album.id)