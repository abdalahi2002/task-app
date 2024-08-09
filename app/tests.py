from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Projet, Tache
from users.models import User

class ProjectTests(APITestCase):

    def setUp(self):
        self.manager = User.objects.create_user(email='manager@example.com', password='password', nom='Manager', is_staff=True)
        print(self.manager)
        self.client = APIClient()
        self.client.force_authenticate(user=self.manager)
        self.project_data = {
            'name': 'Test Project',
            'description': 'Test Description',
            'manger': self.manager.id  # Utiliser l'ID de l'utilisateur
        }

    def test_create_project(self):
        url = reverse('list_create_url')
        response = self.client.post(url, self.project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Projet.objects.count(), 1)
        self.assertEqual(Projet.objects.get().name, 'Test Project')

    def test_list_projects(self):
        # Create a project instance
        Projet.objects.create(
            name='Test Project 3',
            description='Test Description 4',
            manger=self.manager
        )
        
        # Retrieve the list of projects
        url = reverse('list_create_url')
        response = self.client.get(url, format='json')
        
        # Assert the response status and the number of projects
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        

    def test_retrieve_project(self):
        project = Projet.objects.create(name='Test Project', description='Test Description',manger=self.manager)
        url = reverse('retrieve_update_destroy_url', kwargs={'pk': project.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], project.name)

    def test_update_project(self):
        project = Projet.objects.create(name='Test Project', description='Test Description',manger=self.manager)
        url = reverse('retrieve_update_destroy_url', kwargs={'pk': project.id})
        response = self.client.put(url, {'name': 'Updated Project', 'description': 'Updated Description','manger':str(self.manager.id)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.name, 'Updated Project')

    def test_delete_project(self):
        project = Projet.objects.create(name='Test Project', description='Test Description',manger=self.manager)
        url = reverse('retrieve_update_destroy_url', kwargs={'pk': project.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Projet.objects.count(), 0)
        

class TaskTests(APITestCase):

    def setUp(self):
        self.manager = User.objects.create_user(email='manager@example.com', password='password', nom='Manager', is_staff=True)
        self.assignee = User.objects.create_user(email='assignee@example.com', password='password', nom='Assignee')
        self.client = APIClient()
        self.client.force_authenticate(user=self.manager)
        
        self.project = Projet.objects.create(name='Test Project', description='Test Description', manger=self.manager)
        
        self.task_data = {
            'titre': 'Test Task',
            'description': 'Test Task Description',
            'projet': self.project.id,
            'assigned_to': self.assignee.id,
            'status': 'PENDING'
        }

    def test_create_task(self):
        url = reverse('task_list_create_url')
        response = self.client.post(url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tache.objects.count(), 1)
        self.assertEqual(Tache.objects.get().titre, 'Test Task')

    def test_list_tasks(self):
        # Create a task instance
        Tache.objects.create(
            titre='Test Task 2',
            description='Test Task Description 2',
            projet=self.project,
            assigned_to=self.assignee,
            status='PENDING'
        )
        
        # Retrieve the list of tasks
        url = reverse('task_list_create_url')
        response = self.client.get(url, format='json')
        
        # Assert the response status and the number of tasks
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # Optional: Assert the content of the response if needed
        self.assertEqual(response.data[0]['titre'], 'Test Task 2')
        self.assertEqual(response.data[0]['description'], 'Test Task Description 2')

    def test_retrieve_task(self):
        task = Tache.objects.create(
            titre='Test Task',
            description='Test Task Description',
            projet=self.project,
            assigned_to=self.assignee,
            status='PENDING'
        )
        url = reverse('task_retrieve_update_destroy_url', kwargs={'pk': task.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titre'], task.titre)

    def test_update_task(self):
        task = Tache.objects.create(
            titre='Test Task',
            description='Test Task Description',
            projet=self.project,
            assigned_to=self.assignee,
            status='PENDING'
        )
        url = reverse('task_retrieve_update_destroy_url', kwargs={'pk': task.id})
        response = self.client.put(url, {
            'titre': 'Updated Task',
            'description': 'Updated Task Description',
            'projet': str(self.project.id),
            'assigned_to': str(self.assignee.id),
            'status': 'IN_PROGRESS'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.titre, 'Updated Task')

    def test_delete_task(self):
        task = Tache.objects.create(
            titre='Test Task',
            description='Test Task Description',
            projet=self.project,
            assigned_to=self.assignee,
            status='PENDING'
        )
        url = reverse('task_retrieve_update_destroy_url', kwargs={'pk': task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tache.objects.count(), 0)