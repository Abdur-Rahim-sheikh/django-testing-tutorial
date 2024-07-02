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
            "Sorry, you don't have any projects, yet."
        )

    def test_no_projects_alert_button_redirect_to_add_page(self):
        self.browser.get(self.live_server_url)
        add_url = self.live_server_url + reverse('add')
        # The user requests to the page for the first time
        self.browser.find_element(By.TAG_NAME,'a').click()
        
        self.assertEqual(
            self.browser.current_url,
            add_url
        )

    def test_user_sees_project_list(self):
        project_name = 'project1'
        project1 = Project.objects.create(
            name=project_name,
            budget=10000
        )
        self.browser.get(self.live_server_url)

        # the user sees the project on the screen
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME,'h5').text,
            project_name
        )

    def test_user_is_redirected_to_project_detail(self):
        project_name = 'project1'
        project1 = Project.objects.create(
            name=project_name,
            budget=10000
        )
        self.browser.get(self.live_server_url)

        # The user sees the project on the scree, He clicks the 'VISIT' Link
        # and is redirected to the detail page

        detail_url = self.live_server_url + reverse('detail',args=[project1.slug])
        

        self.browser.find_element(By.LINK_TEXT,'VISIT').click()

        self.assertEqual(self.browser.current_url, detail_url)