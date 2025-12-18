from decimal import Decimal 
from django.test import TestCase, override_settings
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from api.models import User, Post, Album, Todo, Address, Company, Geo

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class AccountTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            name="Mevcut User",
            username="mevcutuser",
            email="mevcut@test.com",
            phone="1234567890",
            website="website.com"
        )

        self.address = Address.objects.create(
            user=self.user,
            street="Eski Cadde",
            city="Ankara",
            zipcode="06000"
        )

        Geo.objects.create(address=self.address, lat="10.00", lng="20.00")
        Company.objects.create(user=self.user, name="Mevcut A.Ş.")

        self.valid_payload = {
            "name": "Yeni User",
            "username": "yeniuser",
            "email": "yeni@test.com",
            "phone": "5551234567",
            "website": "yenisite.com",
            "address": {
                "street": "Yeni Sokak",
                "suite": "Daire 5",
                "city": "Amasya",
                "zipcode": "05000",
                "geo": {
                    "lat": "41.0082",
                    "lng": "28.9784"
                }
            },
            "company": {
                "name": "Yeni Sirkettt",
            }
        }

    # USER TEST

    # GET /api/users/
    def test_list_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # POST /api/users/
    def test_create_user_nested(self):
        response = self.client.post('/api/users/', self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(response.data['username'], 'yeniuser')
        new_user = User.objects.get(email="yeni@test.com")
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.address.city, "Amasya")
        self.assertEqual(new_user.address.geo.lat, Decimal("41.0082"))
        self.assertEqual(new_user.company.name, "Yeni Sirkettt")

    # GET /api/users/{id}/
    def test_retrieve_user(self):
        response = self.client.get(f'/api/users/{self.user.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Mevcut User")
        self.assertEqual(response.data['address']['city'], "Ankara")
        self.assertEqual(response.data['company']['name'], "Mevcut A.Ş.")

    # PATCH /api/users/{id}/
    def test_update_user_partial(self):
        data = {"name": "İsim Değişti"}
        
        response = self.client.patch(f'/api/users/{self.user.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "İsim Değişti")
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "İsim Değişti")

    # DELETE /api/users/{id}/
    def test_delete_user(self):
        user_id = self.user.id
        self.assertTrue(Address.objects.filter(user_id=user_id).exists())
        response = self.client.delete(f'/api/users/{user_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertFalse(Address.objects.filter(user_id=user_id).exists())


    # USER ACTION TEST

    # GET /api/users/{id}/posts/
    def test_action_posts(self):
        Post.objects.create(user=self.user, title="Test Post", body="Content")
        response = self.client.get(f'/api/users/{self.user.id}/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Post")

    # GET /api/users/{id}/albums/
    def test_action_albums(self):
        Album.objects.create(user=self.user, title="Test Album")
        
        response = self.client.get(f'/api/users/{self.user.id}/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # GET /api/users/{id}/todos/
    def test_action_todos(self):
        Todo.objects.create(user=self.user, title="Test Todo", completed=False)
        
        response = self.client.get(f'/api/users/{self.user.id}/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)