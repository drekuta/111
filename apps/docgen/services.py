from pathlib import Path
from django.core.files.base import File
from docxtpl import DocxTemplate
from apps.forms_registry.models import Personnel
from apps.templates_engine.models import GeneratedDocument, TemplateVersion


def build_personnel_context(person: Personnel) -> dict:
    return {
        'full_name': person.full_name,
        'identifier': person.identifier,
        'birth_date': person.birth_date,
        'birth_place': person.birth_place,
        'employment_type': person.employment_type,
        'position': person.position,
        'functions': person.functions,
        'education': person.education,
        'experience_summary': person.experience_summary,
        'status': person.status,
        'note': person.note,
        'trainings': list(person.trainings.values('title', 'provider', 'date_from', 'date_to', 'details')),
        'internships': list(person.internships.values('organization', 'date_from', 'date_to', 'details')),
        'experiences': list(person.experiences.values('organization', 'position', 'date_from', 'date_to', 'details')),
    }


def generate_form1_docx(personnel_id: int, template_version_id: int, generated_by: str = '') -> GeneratedDocument:
    person = Personnel.objects.get(pk=personnel_id)
    version = TemplateVersion.objects.get(pk=template_version_id, file_format='docx')

    tpl = DocxTemplate(version.file.path)
    context = build_personnel_context(person)
    tpl.render(context)

    output_dir = Path('storage/generated')
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f'form1_{person.id}_v{version.version}.docx'
    output_path = output_dir / filename
    tpl.save(output_path)

    doc = GeneratedDocument(template_version=version, entity_type='personnel', entity_id=person.id, generated_by=generated_by)
    with output_path.open('rb') as fh:
        doc.generated_file.save(filename, File(fh), save=True)
    return doc
