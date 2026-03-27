import re
from dataclasses import dataclass
from io import BytesIO
from zipfile import ZipFile

PLACEHOLDER_PATTERN = re.compile(r"\[\[(.+?)\]\]")

FORM_FIELD_CATALOG = {
    'form1': {
        'person.full_name', 'person.snils', 'person.birth_date', 'person.birth_place', 'person.position',
        'person.employment_basis', 'person.employment_type', 'person.hire_date', 'person.functions',
        'person.education_summary', 'person.training_summary', 'person.experience_summary', 'person.status',
        'person.is_active', 'person.education', 'person.trainings', 'person.experience',
    },
    'form2': {
        'si.parameter', 'si.name', 'si.model', 'si.registry_number', 'si.manufacturer', 'si.manufacture_year',
        'si.commissioning_year', 'si.serial_number', 'si.inventory_number', 'si.measurement_range', 'si.accuracy',
        'si.verification_document', 'si.verification_date', 'si.verification_expiry_date', 'si.legal_basis',
        'si.location', 'si.verification_expired',
    },
    'form3': {
        'io.test_type', 'io.object_group', 'io.name', 'io.model', 'io.manufacturer', 'io.specifications',
        'io.commissioning_year', 'io.serial_number', 'io.inventory_number', 'io.attestation_document',
        'io.attestation_expiry_date', 'io.legal_basis', 'io.location',
    },
    'form4': {
        'ae.name', 'ae.manufacturer', 'ae.manufacture_year', 'ae.serial_number', 'ae.inventory_number',
        'ae.purpose', 'ae.location', 'ae.legal_basis',
    },
    'form5': {
        'rm.name', 'rm.type', 'rm.category', 'rm.manufacturer', 'rm.purpose', 'rm.certified_value',
        'rm.uncertainty', 'rm.document_basis', 'rm.issue_date', 'rm.expiry_date', 'rm.batch',
    },
}

SYSTEM_FIELDS = {
    'lab.full_name', 'lab.short_name', 'lab.accreditation_number', 'system.today', 'system.user_name',
}

ITERABLE_ALIASES = {'education', 'training', 'experience'}


@dataclass
class PlaceholderAnalysis:
    placeholders: list[str]
    recognized: list[str]
    unknown: list[str]
    syntax_errors: list[str]


def _extract_from_archive(source) -> list[str]:
    chunks: list[str] = []
    if hasattr(source, 'read'):
        source.seek(0)
        payload = BytesIO(source.read())
        source.seek(0)
        archive_obj = payload
    elif hasattr(source, 'open') and hasattr(source, 'read') is False:
        source.open('rb')
        payload = BytesIO(source.read())
        source.close()
        archive_obj = payload
    else:
        archive_obj = source

    with ZipFile(archive_obj, 'r') as archive:
        for name in archive.namelist():
            if not name.endswith('.xml'):
                continue
            with archive.open(name) as xml_file:
                chunks.append(xml_file.read().decode('utf-8', errors='ignore'))
    return chunks


def extract_placeholders(file_path) -> list[str]:
    placeholders: set[str] = set()
    for text in _extract_from_archive(file_path):
        for match in PLACEHOLDER_PATTERN.findall(text):
            placeholders.add(match.strip())
    return sorted(placeholders)


def _normalize(expression: str) -> tuple[str | None, str | None]:
    expression = expression.strip()
    if not expression:
        return None, 'empty_expression'

    if expression.startswith('format_date:'):
        parts = expression.split(':', 2)
        if len(parts) != 3 or not parts[1].strip() or not parts[2].strip():
            return None, 'invalid_format_date'
        return parts[1].strip(), None

    if expression.startswith('default:'):
        parts = expression.split(':', 2)
        if len(parts) != 3 or not parts[1].strip():
            return None, 'invalid_default'
        return parts[1].strip(), None

    if expression.startswith('if:'):
        condition = expression[3:].strip()
        if not condition:
            return None, 'invalid_if'
        return condition, None

    if expression.startswith('table_start:') or expression.startswith('table_end:'):
        _, field_name = expression.split(':', 1)
        field_name = field_name.strip()
        if not field_name:
            return None, 'invalid_table_block'
        return field_name, None

    if expression == 'endif':
        return 'endif', None

    return expression, None


def analyze_placeholders(file_path, module: str) -> PlaceholderAnalysis:
    known_fields = FORM_FIELD_CATALOG.get(module, set()) | SYSTEM_FIELDS | ITERABLE_ALIASES | {'endif'}

    placeholders = extract_placeholders(file_path)
    recognized: list[str] = []
    unknown: list[str] = []
    syntax_errors: list[str] = []

    for expression in placeholders:
        normalized, error = _normalize(expression)
        if error:
            syntax_errors.append(f'{expression}: {error}')
            continue

        if normalized in known_fields:
            recognized.append(expression)
        else:
            unknown.append(expression)

    return PlaceholderAnalysis(
        placeholders=placeholders,
        recognized=sorted(recognized),
        unknown=sorted(unknown),
        syntax_errors=sorted(syntax_errors),
    )
