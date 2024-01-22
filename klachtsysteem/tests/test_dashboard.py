from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse
from datetime import datetime
from django.utils import timezone

from ..models import Klacht, Status
from ..forms import ComplaintSearchForm  # Replace with your actual form import

class ComplaintsDashboardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test data for Klacht and Status models
        status1 = Status.objects.create(waarde=1, beschrijving='aangemaakt')
        status2 = Status.objects.create(waarde=2, beschrijving='in werking')

        Klacht.objects.create(
            naam='Test Complaint 1',
            omschrijving='This is a test complaint 1',
            email='test@example.com',
            GPS_locatie='POINT(0 0)',
            datum_melding=timezone.make_aware(datetime(2023, 1, 1)),  # Use timezone-aware datetime
            status=status1
        )
        Klacht.objects.create(
            naam='Test Complaint 2',
            omschrijving='This is a test complaint 2',
            email='test@example.com',
            GPS_locatie='POINT(1 1)',
            datum_melding=timezone.make_aware(datetime(2023, 2, 1)),  # Use timezone-aware datetime
            status=status2
        )

    def setUp(self):
        # Log in the user before each test
        self.client.login(username='testuser', password='testpassword')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/klacht/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('complaints_dashboard'))  # Replace with your view's URL name
        self.assertTemplateUsed(response, 'klachtbeheer.html')

    def test_view_returns_queryset_filtered_by_search_query(self):
        response = self.client.get(reverse('complaints_dashboard') + '?search_query=Test Complaint 1')
        self.assertEqual(len(response.context['klachten']), 1)

    def test_view_returns_queryset_filtered_by_status(self):
        response = self.client.get(reverse('complaints_dashboard') + '?status=1')  # Status ID for 'Open'
        self.assertEqual(len(response.context['klachten']), 1)

    def test_view_context_contains_search_form(self):
        response = self.client.get(reverse('complaints_dashboard'))
        self.assertIsInstance(response.context['search_form'], ComplaintSearchForm)

    def test_view_context_contains_statuses(self):
        response = self.client.get(reverse('complaints_dashboard'))
        self.assertEqual(len(response.context['statuses']), 2)  # Assuming you have two statuses
