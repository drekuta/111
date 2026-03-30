import logging

from django.shortcuts import render
from django.db.utils import OperationalError, ProgrammingError

from apps.forms_registry.models import Personnel
from apps.templates_engine.models import GeneratedDocument


logger = logging.getLogger(__name__)


def dashboard(request):
    context = {
        'personnel_count': 0,
        'recent_personnel': [],
        'recent_docs': [],
    }

    try:
        context.update({
            'personnel_count': Personnel.objects.count(),
            'recent_personnel': Personnel.objects.order_by('-updated_at')[:5],
            'recent_docs': GeneratedDocument.objects.order_by('-created_at')[:5],
        })
    except (OperationalError, ProgrammingError):
        logger.warning('Dashboard database tables are unavailable. Apply migrations to restore data widgets.')

    return render(request, 'ui/dashboard.html', context)
