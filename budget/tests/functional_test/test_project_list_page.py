from selenium import webdriver
from budget.models import Project
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

class TestProjectListPage(StaticLiveServerTestCase):

    def test_foo(self):
        self.assertEqual(0,1)