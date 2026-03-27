from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TemplateForm, TemplateVersionForm
from .models import Template
from .placeholders import FORM_FIELD_CATALOG, SYSTEM_FIELDS, analyze_placeholders


def template_list(request):
    items = Template.objects.all().order_by('-created_at')
    return render(request, 'ui/template_list.html', {'items': items})


def template_create(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('template_detail', pk=obj.pk)
    else:
        form = TemplateForm()
    return render(request, 'ui/template_form.html', {'form': form, 'title': 'Новый шаблон'})


def template_detail(request, pk: int):
    obj = get_object_or_404(Template, pk=pk)
    available_fields = sorted(FORM_FIELD_CATALOG.get(obj.module, set()) | SYSTEM_FIELDS)
    return render(
        request,
        'ui/template_detail.html',
        {
            'item': obj,
            'available_fields': available_fields,
        },
    )


def template_version_create(request, pk: int):
    tmpl = get_object_or_404(Template, pk=pk)
    if request.method == 'POST':
        form = TemplateVersionForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.template = tmpl
            analysis = analyze_placeholders(obj.file, tmpl.module)
            obj.placeholder_schema = {
                'placeholders': analysis.placeholders,
                'recognized': analysis.recognized,
                'unknown': analysis.unknown,
                'syntax_errors': analysis.syntax_errors,
            }
            obj.save()

            if analysis.unknown or analysis.syntax_errors:
                messages.warning(
                    request,
                    'Версия сохранена с предупреждениями: есть неизвестные плейсмаркеры или ошибки синтаксиса.',
                )
            else:
                messages.success(request, 'Версия шаблона успешно сохранена и проверена.')
            return redirect('template_detail', pk=tmpl.pk)
    else:
        form = TemplateVersionForm()
    return render(request, 'ui/template_version_form.html', {'form': form, 'template': tmpl})
