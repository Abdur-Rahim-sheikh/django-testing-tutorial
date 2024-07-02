from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from budget.models import Project
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
class TestProjectListPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        print(f"{self.browser=}")
    def tearDown(self) -> None:
        self.browser.close()


    def test_no_projects_alert_is_displayed(self):
        self.browser.get(self.live_server_url)
        # The user requests the page for the first time
        alert = self.browser.find_element(By.CLASS_NAME,'noproject-wrapper')
        self.assertEqual(
            alert.find_element(By.TAG_NAME,'h3').text,
            "Sorry, you don't have any projects, yet. ---"
        )