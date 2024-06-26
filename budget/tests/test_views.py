from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense
import json


class TestViews(TestCase):
    def setUp(self, slug='project1'):
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=[slug])
        self.project1 = Project.objects.create(
            name=slug,
            budget=10000
        )

    def test_project_list_GET(self):

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
      
        self.assertTemplateUsed(response, 'budget/project-list.html')
    

    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
      
        self.assertTemplateUsed(response, 'budget/project-detail.html')

    def test_project_detail_POST_adds_new_expense(self):
        Category.objects.create(
            project = self.project1,
            name='development'
        )
        data = {
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        }
        response = self.client.post(self.detail_url, data)

        self.assertEqual(response.status_code,302)

        self.assertEqual(self.project1.expenses.first().title, data['title'])
        self.assertEqual(self.project1.expenses.first().amount, data['amount'])

    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_deletes_expense(self):
        category1 = Category.objects.create(
            project = self.project1,
            name = 'development1'
        )

        expense = Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount=1000,
            category=category1
        )

        response = self.client.delete(self.detail_url, json.dumps({
            'id': expense.id
        }))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.project1.expenses.count(),0)


    def test_project_detail_DELETE_no_data(self):
        category1 = Category.objects.create(
            project = self.project1,
            name = 'development1'
        )

        expense = Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount=1000,
            category=category1
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.project1.expenses.count(),1)


    def test_project_create_POST(self):
        url = reverse('add')
        project_name = 'project2'
        categories = ['design','developement']
        budget = 10000
        data = {
            'name': project_name,
            'budget': budget,
            'categoriesString': ','.join(categories)
        }
        response = self.client.post(url,data=data)
        project2 = Project.objects.get(name=project_name)

        self.assertEqual(project2.name, project_name)
        first_category = Category.objects.get(name=categories[0])
        self.assertEqual(first_category.project, project2)
        self.assertEqual(first_category.name, categories[0])