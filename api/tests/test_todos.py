from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from api.models import User, Todo

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class TodoTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            name="Task TAAAA", username="taskusername", email="task@test.com"
        )

        self.todo_done = Todo.objects.create(
            user=self.user, 
            title="Bitmiş Görev", 
            completed=True
        )

        self.todo_pending = Todo.objects.create(
            user=self.user, 
            title="Bekleyen Görev", 
            completed=False
        )

            
    # GET /api/todos/ 
    def test_list_todos(self):
        """Tum gorevlerin listelenmesini dogrular."""
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertGreaterEqual(len(response.data), 2)

    # POST /api/todos/
    def test_create_todo(self):
        """Yeni gorev olusturmayi test eder."""
        payload = {
            "userId": self.user.id,
            "title": "Yeni Görev",
            "completed": False
        }
        response = self.client.post('/api/todos/', payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Yeni Görev")
        self.assertFalse(response.data['completed'])

    # GET /api/todos/{id}/
    def test_retrieve_todo(self):
        """gorev detayinin dogru geldigini test eder."""
        response = self.client.get(f'/api/todos/{self.todo_pending.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Bekleyen Görev")

    # PATCH /api/todos/{id}/
    def test_update_todo_status(self):
        """
        Gorev durumunun guncellenmesini test eder. 
        Degisikligin veritabanina yansidigini dogrular.
        """
        response = self.client.patch(
            f'/api/todos/{self.todo_pending.id}/', 
            {"completed": True}, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['completed'])
        
        self.todo_pending.refresh_from_db()
        self.assertTrue(self.todo_pending.completed)

    # DELETE /api/todos/{id}/
    def test_delete_todo(self):
        """Gorev silme islemini ve veritabanindan kaldirildigini dogrular."""
        response = self.client.delete(f'/api/todos/{self.todo_done.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=self.todo_done.id).exists())

    # GET /api/todos/?user={id}
    def test_filter_todos_by_user(self):
        """
        user={id} filtresine gore gorevleri getirmeyi test eder.
        """
        other_user = User.objects.create(name="Other Kullanici", username="otherK", email="o@k.com")
        Todo.objects.create(user=other_user, title="Other Task", completed=False)

        response = self.client.get(f'/api/todos/?user={self.user.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for task in response.data:
            self.assertEqual(task['userId'], self.user.id)

    # GET /api/todos/?completed=true
    def test_filter_todos_completed_true(self):
        """sadece tamamlanmis gorevleri getirdigini test eder."""
        response = self.client.get('/api/todos/?completed=true')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Bitmiş Görev")
        self.assertTrue(response.data[0]['completed'])

    # GET /api/todos/?completed=false
    def test_filter_todos_completed_false(self):
        """sadece tamamlanmamis gorevleri getirdigini test eder."""
        response = self.client.get('/api/todos/?completed=false')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Bekleyen Görev")
        self.assertFalse(response.data[0]['completed'])

    # GET /api/todos/?user={id}&completed=false
    def test_complex_filter(self):
        """Birden fazla filtre parametresinin (user, completed) ayni anda calistigini test eder."""
        response = self.client.get(f'/api/todos/?user={self.user.id}&completed=false')
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Bekleyen Görev")