from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class Students (models.Model):
    #user (FK)
    #institute (FK)
    isVerified = models.BooleanField(default=False)
    entryNumber = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    motherName = models.CharField(max_length=50)
    fatherName = models.CharField(max_length=50)
    preferredProfile = models.CharField(blank=True)
    category = models.CharField(max_length=50)
    technicalSkills = models.TextField(blank=True)
    introduction = models.TextField(blank=True)
    careerPlans = mdoels.TextField(blank=True)

class SocialProfiles (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    github = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    codechef = models.URLField(blank=True)
    codeforces = models.URLField(blank=True)

class Projects (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    startDate = models.DateField()
    endDate = models.DateField()
    description = models.TextField(blank=True)

class Patents (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    Office = CountryField()
    Number = models.CharField(max_length=50)
    Status = models.CharField(choices=[ ('P', 'Patent Pending'), ('I', 'Patent Issued')])
    filingDate = models.DateField()

class Resumes (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    link = models.URLField()
    isLatest = models.BooleanField(default=True)

class AwardsAndRecognitions (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    Issuer = models.CharField(max_length=50)
    issueDate = models.DateField()
    #associatedWith = list of all academic intitutes of student

class WorkExperience (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    jobTitle = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    starDate = models.DateField()
    endDate = models.DateField()
    compensationMin = models.IntegerField(validators=[MinValueValidator(0)])
    compensationMax = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)

class Courses (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    courseCode = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    gradeSecured = models.CharField(choices=['A', 'A-', 'B', 'B-', 'C', 'C-', 'F'])

class Competitions (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    position = model.CharField(max_length=50)
    #associatedWith = list of all academic intitutes of student
    date = models.DateField()
    description = models.TextField(blank=True)

class PositionsOfResponsibilities (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    fromDate = models.DateField()
    toDate = models.DateField()
    organizationName = models.CharField(max_length=50)

class Documents (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.URLField()

class Semester (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    semesterNumber = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    sgpa = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    numberOfBacklogs = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100))
    gradeSheetLink = models.URLField()

class Class (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12))
    InstituteName = models.CharField(max_length=50)
    fromDate = models.DateField()
    toDate = models.DateField()
    score = models.FloatField()
    board = models.CharField(max_length=50)
    stream = models.CharField(max_length=50)

class Certifications (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    issuingAuthority = models.CharField(max_length=50)
    link = models.URLField()
    date = models.DateField()
    licenseNumber = models.CharField(max_length=50)
    hasExpiry = models.BooleanField(default=False)
    description = models.TextField(blank=True)

class ConferencesAndWorkshops (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    organizor = models.CharField(max_length=50)
    address = models.TextField()

class CommunicationLanguages (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    language = models.CharField(max_length=50)
    proficiency = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5))

class TestScores (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    scoreFormat = models.CharField(choices=[('S', 'Score'), ('R', 'Rank'), ('P', 'Percentile')])
    score = models.FloatField()
    total = models.FloatField(validators=[MinValueValidator(0.0)])
    examDate = models.DateField()
    #associatedWith = list of all academic intitutes of student