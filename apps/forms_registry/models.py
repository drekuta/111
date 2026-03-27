from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Personnel(TimestampedModel):
    full_name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=64, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=255, blank=True)
    engagement_basis = models.TextField(blank=True)
    employment_type = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    contract_details = models.TextField(blank=True)
    position = models.CharField(max_length=255, blank=True)
    functions = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience_summary = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='active')
    note = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class PersonnelTraining(TimestampedModel):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='trainings')
    title = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, blank=True)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True)


class PersonnelInternship(TimestampedModel):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='internships')
    organization = models.CharField(max_length=255)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True)


class PersonnelExperience(TimestampedModel):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='experiences')
    organization = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True)


class MeasuringInstrument(TimestampedModel):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255, blank=True)
    verification_due_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default='active')


class TestEquipment(TimestampedModel):
    name = models.CharField(max_length=255)
    attestation_due_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default='active')


class AuxEquipment(TimestampedModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default='active')


class ReferenceMaterial(TimestampedModel):
    name = models.CharField(max_length=255)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='active')


class Attachment(TimestampedModel):
    content_type = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    file = models.FileField(upload_to='attachments/%Y/%m/%d')
    original_name = models.CharField(max_length=255)
    uploaded_by = models.CharField(max_length=255, blank=True)
    is_archived = models.BooleanField(default=False)
