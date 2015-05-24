from django.test import TestCase, Client
from TaskMan.models import Tasks, UserProfile

class TaskTestCase(TestCase):
    """ Test Cases For TaskMan App"""
    def setUp(self):
        self.profile = UserProfile.objects.create(email='cse@gmil.com', user_name='rmchauhan', password='1234')
        Tasks.objects.create(task="first Test Case", dead_line_date='2016-02-14', user_id=self.profile.id)
        Tasks.objects.create(task="Second Test Case", dead_line_date='2016-02-21', user_id=self.profile.id)

    def test_tasks(self):
        """Animals that can speak are correctly identified"""
        first = Tasks.objects.get(task="first Test Case")
        second = Tasks.objects.get(task="Second Test Case")
        self.assertEqual(first.task, 'first Test Case')
        self.assertEqual(second.task, 'Second Test Case')
        self.assertNotEqual(second.task, 'Second Test Case, Not match')
        self.assertNotEqual(second.task, 'Second Test Case , Not match')
        
    def test_home(self):
        resp = self.client.get('/home/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('all_tasks' in resp.context)
        aa = [task.pk for task in resp.context['all_tasks']]
        self.assertEqual([task.pk for task in resp.context['all_tasks']], [1, 2])
        
    def test_register(self):
        resp = self.client.get('/taskman/register/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/taskman/register/', {'email': self.profile.email, 'password': self.profile.password})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("User profile with this E-Mail already exists.", resp.content)
        resp = self.client.post('/taskman/register/', {'email': 'avx@gmail.com', 'password': '12345'})
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("User profile with this E-Mail already exists.", resp.content)
        
    def test_login(self):
        resp = self.client.get('/taskman/login/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/taskman/login/', {'username': 'avx@gmail.com', 'password': '12345'})
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/taskman/login/', {'username': self.profile.email, 'password': self.profile.password})
        self.assertEqual(resp.status_code, 200)
    
    def test_create_task(self):
        resp = self.client.get('/taskman/create_tasks/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/taskman/create_tasks/', {'username': 'avx@gmail.com', 'password': '12345'})
        self.assertEqual(resp.status_code, 200)
