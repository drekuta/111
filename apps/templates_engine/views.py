from django.shortcuts import get_object_or_404, redirect, render
from .forms import TemplateForm, TemplateVersionForm
from .models import Template


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
    return render(request, 'ui/template_detail.html', {'item': obj})


def template_version_create(request, pk: int):
    tmpl = get_object_or_404(Template, pk=pk)
    if request.method == 'POST':
        form = TemplateVersionForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.template = tmpl
            obj.save()
            return redirect('template_detail', pk=tmpl.pk)
    else:
        form = TemplateVersionForm()
    return render(request, 'ui/template_version_form.html', {'form': form, 'template': tmpl})
