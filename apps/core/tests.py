from unittest.mock import patch

from django.db.utils import OperationalError
from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    @patch('apps.core.views.GeneratedDocument.objects.order_by', side_effect=OperationalError)
    @patch('apps.core.views.Personnel.objects.order_by', side_effect=OperationalError)
    @patch('apps.core.views.Personnel.objects.count', side_effect=OperationalError)
    def test_dashboard_returns_200_when_migrations_not_applied(
        self,
        _mock_count,
        _mock_personnel_order,
        _mock_docs_order,
    ):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['personnel_count'], 0)
        self.assertEqual(response.context['recent_personnel'], [])
        self.assertEqual(response.context['recent_docs'], [])
