
from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
from klachtsysteem.models import Invitation
from django.contrib.auth.forms import UserCreationForm


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
        self.assertRedirects(response, '/klacht/dashboard/')

    def test_login_view_post_failure(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        # self.assertContains(response, 'Invalid credentials')

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.invitation = Invitation.objects.create(code='testcode', is_used=False)
        self.register_url = reverse('register', args=[self.invitation.code])

    def test_register_view_get(self):
        response = self.client.get(f'/register/{self.invitation.code}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_invalid_invitation_code(self):
        response = self.client.get('/register/codeisnot/')
        self.assertRedirects(response, reverse('invalid_code'))


    def test_no_invitation_code(self):
        response = self.client.get(f'/register/')
        self.assertRedirects(response, reverse('invalid_code'))

    def test_get_with_valid_invitation_code(self):
        response = self.client.get(self.register_url, {'invitation_code': self.invitation.code})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_post_invalid_form(self):
        response = self.client.post(self.register_url, {'username': '', 'password': ''})  # Use actual form fields
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(response.context['form'].is_valid())

    def test_post_valid_form(self):
        form_data = {'username': 'newuser', 'password1': 'password314141123', 'password2': 'password314141123'}  # Use actual form fields and valid data
        response = self.client.post(self.register_url, form_data)
        self.assertRedirects(response, reverse('login'))
        updated_invitation = Invitation.objects.get(code='testcode')
        self.assertTrue(updated_invitation.is_used)

    def test_form_initialization_on_get(self):
        response = self.client.get(self.register_url, {'invitation_code': self.invitation.code})
        self.assertIsInstance(response.context['form'], UserCreationForm)
        self.assertEqual(response.context['invitation_code'], self.invitation.code)
