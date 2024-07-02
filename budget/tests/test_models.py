from django.test import TestCase
from budget.models import Project, Category, Expense

class TestModels(TestCase):

    def setUp(self):
        self.project1 = Project.objects.create(
            name = 'Project 1',
            budget = 1000
        )

    
    def test_project_is_assigned_slug_on_creation(self):
        self.assertEqual(self.project1.slug, 'project-1')

    def test_budget_left(self):
        category1 = Category.objects.create(
            project = self.project1,
            name='development'
        )
        category2 = Category.objects.create(
            project = self.project1,
            name='finance'
        )

        given_amount = 1000
        Expense.objects.create(
            project = self.project1,
            title='expense1',
            amount=given_amount,
            category=category1
        )
        self.assertEqual(self.project1.budget_left, self.project1.budget-given_amount)

        next_amount = 2000
        Expense.objects.create(
            project = self.project1,
            title='expense 2',
            amount=next_amount,
            category=category2
        )

        self.assertEqual(self.project1.budget_left, 
                         self.project1.budget-given_amount-next_amount)
        
    def test_project_total_transactions(self):
        project2 = Project.objects.create(
            name="Project 2",
            budget=2300
        )
        # though used category of different project
        category1 = Category.objects.create(
            project = self.project1,
            name='development'
        )
        category2 = Category.objects.create(
            project = project2,
            name='finance'
        )

        given_amount = 1000
        Expense.objects.create(
            project = project2,
            title='expense1',
            amount=given_amount,
            category=category1
        )

        Expense.objects.create(
            project = project2,
            title='expense 2',
            amount=50,
            category=category2
        )
        # total transaction should be 2 as two expense created on project 2
        self.assertEqual(project2.total_transactions, 2)