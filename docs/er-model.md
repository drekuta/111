# ER-модель

```mermaid
erDiagram
    USER ||--o{ ACTION_LOG : performs
    USER ||--o{ GENERATED_DOCUMENT : creates
    USER ||--o{ TEMPLATE : owns

    PERSONNEL ||--o{ PERSON_EDUCATION : has
    PERSONNEL ||--o{ PERSON_TRAINING : has
    PERSONNEL ||--o{ PERSON_INTERNSHIP : has
    PERSONNEL ||--o{ PERSON_EXPERIENCE : has
    PERSONNEL ||--o{ ATTACHMENT : linked

    MEASURING_INSTRUMENT ||--o{ ATTACHMENT : linked
    TEST_EQUIPMENT ||--o{ ATTACHMENT : linked
    AUX_EQUIPMENT ||--o{ ATTACHMENT : linked
    REFERENCE_MATERIAL ||--o{ ATTACHMENT : linked

    TEMPLATE ||--o{ TEMPLATE_VERSION : has
    TEMPLATE_VERSION ||--o{ PLACEHOLDER_MAPPING : has
    TEMPLATE_VERSION ||--o{ GENERATED_DOCUMENT : source

    GENERATED_DOCUMENT }o--|| PERSONNEL : for_entity
    GENERATED_DOCUMENT }o--|| MEASURING_INSTRUMENT : for_entity
    GENERATED_DOCUMENT }o--|| TEST_EQUIPMENT : for_entity
    GENERATED_DOCUMENT }o--|| AUX_EQUIPMENT : for_entity
    GENERATED_DOCUMENT }o--|| REFERENCE_MATERIAL : for_entity
```

## Ключевые сущности
- `personnel` (Форма 1)
- `measuring_instrument` (Форма 2)
- `test_equipment` (Форма 3)
- `aux_equipment` (Форма 4)
- `reference_material` (Форма 5)
- `template`, `template_version`, `placeholder_mapping`
- `generated_document` (архив печатных форм)
- `attachment` (вложения)
- `action_log` (аудит)
