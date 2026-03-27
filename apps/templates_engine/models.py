from django.db import models


class Template(models.Model):
    MODULE_CHOICES = [
        ('form1', 'Форма 1 — Персонал'),
        ('form2', 'Форма 2 — СИ'),
        ('form3', 'Форма 3 — ИО'),
        ('form4', 'Форма 4 — Вспом. оборудование'),
        ('form5', 'Форма 5 — СО'),
    ]
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=10, choices=MODULE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TemplateVersion(models.Model):
    FORMAT_CHOICES = [('docx', 'DOCX'), ('xlsx', 'XLSX')]
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='versions')
    version = models.PositiveIntegerField()
    file = models.FileField(upload_to='template_versions/%Y/%m/%d')
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    placeholder_schema = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('template', 'version')


class GeneratedDocument(models.Model):
    template_version = models.ForeignKey(TemplateVersion, on_delete=models.PROTECT)
    entity_type = models.CharField(max_length=32)
    entity_id = models.PositiveIntegerField()
    generated_file = models.FileField(upload_to='generated/%Y/%m/%d')
    generated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
