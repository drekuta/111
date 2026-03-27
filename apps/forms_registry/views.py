from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PersonnelForm
from .models import Personnel


def personnel_list(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    qs = Personnel.objects.all().order_by('-updated_at')
    if query:
        qs = qs.filter(Q(full_name__icontains=query) | Q(position__icontains=query) | Q(note__icontains=query))
    if status:
        qs = qs.filter(status=status)

    return render(request, 'ui/personnel_list.html', {'items': qs, 'q': query, 'status': status})


def personnel_create(request):
    if request.method == 'POST':
        form = PersonnelForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('personnel_detail', pk=obj.pk)
    else:
        form = PersonnelForm()
    return render(request, 'ui/personnel_form.html', {'form': form, 'title': 'Новый сотрудник'})


def personnel_detail(request, pk: int):
    obj = get_object_or_404(Personnel, pk=pk)
    return render(request, 'ui/personnel_detail.html', {'item': obj})
