from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from apps.forms_registry.models import Personnel
from apps.templates_engine.models import TemplateVersion
from .services import generate_form1_docx


def generate_personnel_form(request, pk: int):
    person = get_object_or_404(Personnel, pk=pk)
    version = (
        TemplateVersion.objects
        .filter(template__module='form1', file_format='docx', is_active=True)
        .order_by('-created_at')
        .first()
    )
    if not version:
        messages.error(request, 'Нет активного DOCX-шаблона для Формы 1.')
        return redirect('personnel_detail', pk=person.pk)

    try:
        generate_form1_docx(person.id, version.id, generated_by=str(request.user) if request.user.is_authenticated else '')
    except RuntimeError as exc:
        messages.error(request, str(exc))
        return redirect('personnel_detail', pk=person.pk)

    messages.success(request, 'Печатная форма успешно сформирована и помещена в архив.')
    return redirect('personnel_detail', pk=person.pk)
