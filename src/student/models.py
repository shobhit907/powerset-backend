from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# Create your models here.


class Institute(models.Model):
    name = models.CharField(max_length=200)
    logo = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Student (models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students')
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name='students')
    is_verified = models.BooleanField(default=False)
    entry_number = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    preferred_profile = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=10, choices=[(
        'GEN', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')])
    technical_skills = models.TextField(blank=True)
    introduction = models.TextField(blank=True)
    career_plans = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)+' '+self.entry_number


class SocialProfile (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='socialProfile')
    github = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    codechef = models.URLField(blank=True)
    codeforces = models.URLField(blank=True)

    def __str__(self):
        return '%s Social profiles' % self.student.entry_number


class Project (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='project')
    title = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Project Title: %s' % (self.student.entry_number, self.title)


class Patent (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='patent')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    office = models.CharField(max_length=20)
    number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[(
        'P', 'Patent Pending'), ('I', 'Patent Issued')])
    filing_date = models.DateField()

    def __str__(self):
        return '%s Patent Title: %s' % (self.student.entry_number, self.title)


class Resume (models.Model):
    number = models.IntegerField(validators=[MinValueValidator(1)])
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='resume')
    link = models.URLField()
    is_latest = models.BooleanField(default=True)

    def __str__(self):
        return '%s Resume: %s' % (self.student.entry_number, self.number)


class AwardAndRecognition (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='awardAndRecognition')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    issuer = models.CharField(max_length=50)
    issue_date = models.DateField()
    # associatedWith = list of all academic intitutes of student

    def __str__(self):
        return '%s Award or Recognition Title: %s' % (self.student.entry_number, self.title)


class WorkExperience (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='workExperience')
    job_title = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    compensation_min = models.IntegerField(validators=[MinValueValidator(0)])
    compensation_max = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Work Experience Title: %s' % (self.student.entry_number, self.jobTitle)


class Course (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='course')
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    grade_secured = models.CharField(max_length=2, choices=[(
        'A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'), ('C', 'C'), ('C-', 'C-'), ('F', 'F')])

    def __str__(self):
        return '%s Course Title: %s' % (self.student.entry_number, self.title)


class Competition (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='competition')
    title = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    associated_with = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Competition Title: %s' % (self.student.entry_number, self.title)


class PositionsOfResponsibility (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='positionsOfResponsibility')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    organization_name = models.CharField(max_length=50)

    def __str__(self):
        return '%s Position of Responsibility Title: %s' % (self.student.entry_number, self.title)


class Document (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='document')
    name = models.CharField(max_length=50)
    link = models.URLField()

    def __str__(self):
        return '%s Document Name: %s' % (self.student.entry_number, self.name)


class Semester (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='semester')
    number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)])
    sgpa = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    number_of_backlogs = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade_sheet_link = models.URLField()

    def __str__(self):
        return '%s Semester Number: %s' % (self.student.entry_number, self.number)


class Class (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='clas')
    number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)])
    institute_name = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField()
    score = models.FloatField()
    board = models.CharField(max_length=50)
    stream = models.CharField(max_length=50)

    def __str__(self):
        return '%s Class Number: %s' % (self.student.entry_number, self.number)


class Certification (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='certification')
    name = models.CharField(max_length=50)
    issuing_authority = models.CharField(max_length=50)
    link = models.URLField()
    date = models.DateField()
    license_number = models.CharField(max_length=50)
    has_expiry = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Certification Name: %s' % (self.student.entry_number, self.name)


class ConferencesAndWorkshop (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='conferenceAndWorkshop')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    organizer = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return '%s Conference or Workshop Title: %s' % (self.student.entry_number, self.title)


class CommunicationLanguage (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='communicationLanguage')
    language = models.CharField(max_length=50)
    proficiency = models.CharField(max_length=20, choices=[('1', 'Elementary proficiency'), ('2', 'Limited working proficiency'), (
        '3', 'Professional working proficiency'), ('4', 'Full professional working proficiency'), ('5', 'Native or bilingual proficiency')])

    def __str__(self):
        return '%s Language Name: %s' % (self.student.entry_number, self.language)


class Exam (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='exam')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    score_format = models.CharField(max_length=20, choices=[(
        'S', 'Score'), ('R', 'Rank'), ('P', 'Percentile')])
    score = models.FloatField()
    total = models.FloatField(validators=[MinValueValidator(0.0)])
    exam_date = models.DateField()
    associated_with = models.CharField(max_length=200)

    def __str__(self):
        return '%s Test Title: %s' % (self.student.entry_number, self.title)
