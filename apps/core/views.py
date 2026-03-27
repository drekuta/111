from django.shortcuts import render
from apps.forms_registry.models import Personnel
from apps.templates_engine.models import GeneratedDocument


def dashboard(request):
    context = {
        'personnel_count': Personnel.objects.count(),
        'recent_personnel': Personnel.objects.order_by('-updated_at')[:5],
        'recent_docs': GeneratedDocument.objects.order_by('-created_at')[:5],
    }
    return render(request, 'ui/dashboard.html', context)
