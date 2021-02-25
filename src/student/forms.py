from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

#Create your forms here.

class InstituteForm (forms.Form):
    name = forms.CharField(max_length=200)
    logo = forms.URLField(required=False)

class StudentForm (forms.Form):
    entry_number = forms.CharField(max_length=50)
    branch = forms.CharField(max_length=50)
    degree = forms.CharField(max_length=50)
    mother_name = forms.CharField(max_length=50)
    father_name = forms.CharField(max_length=50)
    preferred_profile = forms.CharField(max_length=50, required=False)
    category = forms.ChoiceField(choices=[(
        'GEN', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')])
    technical_skills = forms.CharField(widget=forms.Textarea, required=False)
    introduction = forms.CharField(widget=forms.Textarea, required=False)
    career_plans = forms.CharField(widget=forms.Textarea, required=False)

class SocialProfileForm (forms.Form):
    github = forms.URLField(required=False)
    facebook = forms.URLField(required=False)
    linkedin = forms.URLField(required=False)
    codechef = forms.URLField(required=False)
    codeforces = forms.URLField(required=False)

class ProjectForm (forms.Form):
    title = forms.CharField(max_length=50)
    domain = forms.CharField(max_length=50)
    start_date = forms.DateField()
    end_date = forms.DateField()
    description = forms.CharField(widget=forms.Textarea, required=False)

class PatentForm (forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, required=False)
    office = forms.CharField(max_length=20)
    number = forms.CharField(max_length=50)
    status = forms.ChoiceField(choices=[(
        'P', 'Patent Pending'), ('I', 'Patent Issued')])
    filing_date = forms.DateField()

class ResumeForm (forms.Form):
    number = forms.IntegerField(validators=[MinValueValidator(1)])
    link = forms.URLField()
    is_latest = forms.BooleanField()

class AwardAndRecognitionForm (forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, required=False)
    issuer = forms.CharField(max_length=50)
    issue_date = forms.DateField()
    # associatedWith = list of all academic intitutes of student

class WorkExperienceForm (forms.Form):
    job_title = forms.CharField(max_length=50)
    company = forms.CharField(max_length=50)
    location = forms.CharField(max_length=50)
    start_date = forms.DateField()
    end_date = forms.DateField()
    compensation_min = forms.IntegerField(validators=[MinValueValidator(0)])
    compensation_max = forms.IntegerField(validators=[MinValueValidator(0)])
    description = forms.CharField(widget=forms.Textarea, required=False)

class CourseForm (forms.Form):
    code = forms.CharField(max_length=50)
    title = forms.CharField(max_length=50)
    grade_secured = forms.ChoiceField(choices=[(
        'A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'), ('C', 'C'), ('C-', 'C-'), ('F', 'F')])

class CompetitionForm (forms.Form):
    title = forms.CharField(max_length=50)
    position = forms.CharField(max_length=50)
    associated_with = forms.CharField(max_length=200)
    date = forms.DateField()
    description = forms.CharField(widget=forms.Textarea, required=False)

class PositionsOfResponsibilityForm (forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, required=False)
    from_date = forms.DateField()
    to_date = forms.DateField()
    organization_name = forms.CharField(max_length=50)

class DocumentForm (forms.Form):
    name = forms.CharField(max_length=50)
    link = forms.URLField()

class SemesterForm (forms.Form):
    number = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)])
    sgpa = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    number_of_backlogs = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade_sheet_link = forms.URLField()

class ClassForm (forms.Form):
    number = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)])
    institute_name = forms.CharField(max_length=50)
    from_date = forms.DateField()
    to_date = forms.DateField()
    score = forms.FloatField()
    board = forms.CharField(max_length=50)
    stream = forms.CharField(max_length=50)

class CertificationForm (forms.Form):
    name = forms.CharField(max_length=50)
    issuing_authority = forms.CharField(max_length=50)
    link = forms.URLField()
    date = forms.DateField()
    license_number = forms.CharField(max_length=50)
    has_expiry = forms.BooleanField()
    description = forms.CharField(widget=forms.Textarea, required=False)

class ConferencesAndWorkshopForm (forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, required=False)
    organizer = forms.CharField(max_length=50)
    address = forms.CharField(widget=forms.Textarea, )

class CommunicationLanguageForm (forms.Form):
    language = forms.CharField(max_length=50)
    proficiency = forms.ChoiceField(choices=[('1', 'Elementary proficiency'), ('2', 'Limited working proficiency'), (
        '3', 'Professional working proficiency'), ('4', 'Full professional working proficiency'), ('5', 'Native or bilingual proficiency')])

class ExamForm (forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, required=False)
    score_format = forms.ChoiceField(choices=[(
        'S', 'Score'), ('R', 'Rank'), ('P', 'Percentile')])
    score = forms.FloatField()
    total = forms.FloatField(validators=[MinValueValidator(0.0)])
    exam_date = forms.DateField()
    associated_with = forms.CharField(max_length=200)