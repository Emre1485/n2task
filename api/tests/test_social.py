from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from api.models import User, Post, Comment

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class SocialTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            name="Social User", username="social", email="social@test.com"
        )

        self.post = Post.objects.create(
            user=self.user,
            title="İlk Gönderi",
            body="Merhabalar arkadaslar!!!!!!"
        )

        self.comment = Comment.objects.create(
            post=self.post,
            name="Takipciiii",
            email="fan@test.com",
            body="Çok beğendim derdim ama diyemiyorum!"
        )

    # POST TEST

    # GET /api/posts/
    def test_list_posts(self):
        """Tum gonderilerin listelenmesini test eder."""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # POST /api/posts/
    def test_create_post(self):
        """
        Yeni gonderi olusturmayi test eder.
        Frontend'den gelen 'userId' alaninin backend'de dogru iliskilendirildigini kontrol eder.
        """
        payload = {
            "userId": self.user.id,
            "title": "Yeni Haber",
            "body": "Son dakika gelişmesi..."
        }
        response = self.client.post('/api/posts/', payload)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Yeni Haber")
        self.assertTrue(Post.objects.filter(title="Yeni Haber").exists())
    
    # GET /api/posts/?user={id}
    def test_filter_posts_by_user(self):
        """
        user={id} parametresi ile gonderilerin kullanici bazli filtrelenmesini test eder.
        Baska kullaniciya ait gonderilerin listeye karismadigini dogrular.
        """
        other_user = User.objects.create(name="Other", username="other", email="other@t.com")
        Post.objects.create(user=other_user, title="Other Post", body="...")
        response = self.client.get(f'/api/posts/?user={self.user.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['userId'], self.user.id)

    # PATCH /api/posts/{id}/
    def test_update_post(self):
        """gonderi basliginin guncellenmesini test eder."""
        response = self.client.patch(f'/api/posts/{self.post.id}/', {"title": "Editlendi"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Editlendi")

    # DELETE /api/posts/{id}/
    def test_delete_post(self):
        """Gonderi silme islemini ve veritabanindan kaldirilmasini test eder."""
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    # COMMENT TEST

    # GET /api/comments/
    def test_list_comments(self):
        """Yorum listeleme endpoint'inin erisilebilir oldugunu test eder."""
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # POST /api/comments/
    def test_create_comment(self):
        """Bir gonderiye yorum yapilmasini ve 'postId' iliskisinin kurulmasini test eder."""
        payload = {
            "postId": self.post.id,
            "name": "Yeni Yorum",
            "email": "yorumcu@test.com",
            "body": "Güzel içerik."
        }
        response = self.client.post('/api/comments/', payload)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], "yorumcu@test.com")

    # GET /api/comments/?post={id}
    def test_filter_comments_by_post(self):
        """Yorumlarin bagli olduklari gonderiye gore filtrelenmesini test eder."""
        other_post = Post.objects.create(user=self.user, title="X", body="Y")
        Comment.objects.create(post=other_post, name="X", email="x@x.com", body="Z")

        response = self.client.get(f'/api/comments/?post={self.post.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['postId'], self.post.id)

    # GET /api/comments/?email={email}
    def test_filter_comments_by_email(self):
        """Yorumlarin e-posta adresine gore filtrelenmesini test eder."""
        target_email = "fan@test.com"
        response = self.client.get(f'/api/comments/?email={target_email}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], target_email)