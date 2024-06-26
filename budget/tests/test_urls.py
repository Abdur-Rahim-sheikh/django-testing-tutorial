from django.test import SimpleTestCase
from django.urls import reverse, resolve
from budget.views import project_list, project_detail, ProjectCreateView
import logging

logger = logging.getLogger(__name__)


class TestUrls(SimpleTestCase):
    def test_list_url_resolves(self):
        url = reverse('list')
        
        self.assertEqual(resolve(url).func, project_list)

    def test_detail_url_resolves(self):
        url = reverse('detail', args=['some-slug'])
        
        self.assertEquals(resolve(url).func, project_detail)
    
    def test_add_url_resolves(self):
        url = reverse('add')
        
        self.assertEqual(resolve(url).func.view_class, ProjectCreateView)
    