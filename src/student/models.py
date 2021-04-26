from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from placement.models import Institute

branch_choices = (('CSE', 'Computer Science & Engineering'),
                  ('EE', 'Electrical Engineering'),
                  ('ME', 'Mechanical Engineering'),
                  ('CE', 'Civil Engineering'),
                  ('MME', 'Metallurgical and Materials Engineering'),
                  ('MNC', 'Mathematics & Computing'),
                  ('CBME', 'Center for BioMedical Engineering'),
                  ('HSS', 'Humanities and Social Sciences'),
                  ('P', 'Physics'),
                  ('C', 'Chemistry'),
                  ('M', 'Mathematics'))

class Student (models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students')
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name='students')
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)
    entry_number = models.CharField(max_length=50, unique=True, null=False)
    gender = models.CharField(default='M',
        max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    branch = models.CharField(max_length=50, default='CSE', choices=branch_choices, null=False)
    degree = models.CharField(max_length=50, null=False)
    batch = models.IntegerField(validators=[MinValueValidator(2000)], default=2020)
    cgpa = models.FloatField(default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    mother_name = models.CharField(max_length=50, null=False)
    father_name = models.CharField(max_length=50, null=False)
    preferred_profile = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=10, choices=[(
        'GEN', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')], null=False)
    technical_skills = models.TextField(blank=True)
    introduction = models.TextField(blank=True)
    career_plans = models.TextField(blank=True)
    is_selected = models.BooleanField(default=False)

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
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Social profiles' % self.student.entry_number


class Project (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='project')
    title = models.CharField(max_length=50, null=False)
    domain = models.CharField(max_length=50, null=False)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    description = models.TextField(blank=True)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Project Title: %s' % (self.student.entry_number, self.title)


class Patent (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='patent')
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=True)
    office = models.CharField(max_length=20, null=False)
    number = models.CharField(max_length=50, null=False)
    status = models.CharField(max_length=20, choices=[(
        'P', 'Patent Pending'), ('I', 'Patent Issued')], null=False)
    filing_date = models.DateField()
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Patent Title: %s' % (self.student.entry_number, self.title)


def get_resume_upload_path(instance, filename):
    return "resumes/{userid}/{filename}".format(userid=instance.student.entry_number, filename=filename)


class Resume (models.Model):
    name = models.CharField(max_length=100, null=False)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='resume')
    resume = models.FileField(upload_to=get_resume_upload_path, null=True)
    is_latest = models.BooleanField(default=True)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Resume: %s' % (self.student.entry_number, self.name)


class AwardAndRecognition (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='awardAndRecognition')
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=True)
    issuer = models.CharField(max_length=50, null=False)
    issue_date = models.DateField()
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)
    # associatedWith = list of all academic intitutes of student

    def __str__(self):
        return '%s Award or Recognition Title: %s' % (self.student.entry_number, self.title)


class WorkExperience (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='workExperience')
    job_title = models.CharField(max_length=50, null=False)
    company = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=50, null=False)
    start_date = models.DateField()
    end_date = models.DateField()
    compensation_min = models.IntegerField(validators=[MinValueValidator(0)])
    compensation_max = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Work Experience Title: %s' % (self.student.entry_number, self.job_title)


class Course (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='course')
    code = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=50, null=False)
    grade_secured = models.CharField(max_length=2, choices=[(
        'A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'), ('C', 'C'), ('C-', 'C-'), ('F', 'F')], null=False)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Course Title: %s' % (self.student.entry_number, self.code)


class Competition (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='competition')
    title = models.CharField(max_length=50, null=False)
    position = models.CharField(max_length=50, null=False)
    associated_with = models.CharField(max_length=200, null=False)
    date = models.DateField()
    description = models.TextField(blank=True)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Competition Title: %s' % (self.student.entry_number, self.title)


class PositionsOfResponsibility (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='positionsOfResponsibility')
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    organization_name = models.CharField(max_length=50, null=False)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Position of Responsibility Title: %s' % (self.student.entry_number, self.title)


def get_document_upload_path(instance, filename):
    return "documents/{userid}/{filename}".format(userid=instance.student.entry_number, filename=filename)


class Document (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='document')
    name = models.CharField(max_length=50)
    document = models.FileField(upload_to=get_document_upload_path, null=True)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Document Name: %s' % (self.student.entry_number, self.name)


def get_grade_sheet_upload_path(instance, filename):
    return "grade_sheets/{userid}/{filename}".format(userid=instance.student.entry_number, filename=filename)


class Semester (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='semester')
    number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)])
    sgpa = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    number_of_backlogs = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade_sheet = models.FileField(
        upload_to=get_grade_sheet_upload_path, null=True)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Semester Number: %s' % (self.student.entry_number, self.number)


class Class (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='clas')
    number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)])
    institute_name = models.CharField(max_length=50, null=False)
    from_date = models.DateField()
    to_date = models.DateField()
    score = models.FloatField()
    board = models.CharField(max_length=50, null=False)
    stream = models.CharField(max_length=50)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Class Number: %s' % (self.student.entry_number, self.number)


class Certification (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='certification')
    name = models.CharField(max_length=50, null=False)
    issuing_authority = models.CharField(max_length=50, null=False)
    link = models.URLField(null=False)
    date = models.DateField()
    license_number = models.CharField(max_length=50)
    has_expiry = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Certification Name: %s' % (self.student.entry_number, self.name)


class ConferencesAndWorkshop (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='conferenceAndWorkshop')
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=True)
    organizer = models.CharField(max_length=50, null=False)
    address = models.TextField()
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Conference or Workshop Title: %s' % (self.student.entry_number, self.title)


class CommunicationLanguage (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='communicationLanguage')
    language = models.CharField(max_length=50, null=False)
    proficiency = models.CharField(max_length=20, choices=[('1', 'Elementary proficiency'), ('2', 'Limited working proficiency'), (
        '3', 'Professional working proficiency'), ('4', 'Full professional working proficiency'), ('5', 'Native or bilingual proficiency')], null=False)

    def __str__(self):
        return '%s Language Name: %s' % (self.student.entry_number, self.language)


class Exam (models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='exam')
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=True)
    score_format = models.CharField(max_length=20, choices=[(
        'S', 'Score'), ('R', 'Rank'), ('P', 'Percentile')], null=False)
    score = models.FloatField()
    total = models.FloatField(validators=[MinValueValidator(0.0)])
    exam_date = models.DateField()
    associated_with = models.CharField(max_length=200, null=False)
    is_verified = models.CharField(max_length= 10, default='Unverified', choices=[('Unverified', 'Unverified'), ('Verified', 'Verified'), ('Rejected', 'Rejected')])
    verification_message = models.TextField(blank=True)

    def __str__(self):
        return '%s Test Title: %s' % (self.student.entry_number, self.title)
