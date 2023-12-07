
from django.test import TestCase, Client
from django.contrib.auth.models import User

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view_get(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_success(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect
        self.assertRedirects(response, '/success/')  # Change '/success/' to your actual success URL

    def test_login_view_post_failure(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid credentials')

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view_get(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_register_view_post_success(self):
        response = self.client.post('/register/', {'username': 'newuser', 'password1': 'testpassword123', 'password2': 'testpassword123'})
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a redirect
        self.assertRedirects(response, '/success/')  # Change '/success/' to your actual success URL

        # Check if the user was created in the database
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_failure(self):
        # Test registration with invalid data (passwords don't match)
        response = self.client.post('/register/', {'username': 'newuser', 'password1': 'testpassword123', 'password2': 'mismatchedpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'The two password fields didn’t match.')

        # Check if the user was not created in the database
        self.assertFalse(User.objects.filter(username='newuser').exists())