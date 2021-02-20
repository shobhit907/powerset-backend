from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class Students (models.Model):
    #user (FK)
    #institute (FK)
    isVerified = models.BooleanField(default=False)
    entryNumber = models.CharField()
    branch = models.CharField()
    degree = models.CharField()
    motherName = models.CharField()
    fatherName = models.CharField()
    preferredProfile = models.CharField(blank=True)
    category = models.CharField()
    technicalSkills = models.CharField(blank=True)
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
    title = models.CharField()
    domain = models.CharField()
    startDate = models.DateField()
    endDate = models.DateField()
    description = models.TextField(blank=True)

class Patents (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField()
    description = models.TextField(blank=True)
    Office = CountryField()
    Number = models.CharField()
    Status = models.CharField(choices=[ ('P', 'Patent Pending'), ('I', 'Patent Issued')])
    filingDate = models.DateField()

class Resumes (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    link = models.URLField()
    isLatest = models.BooleanField(default=True)

class AwardsAndRecognitions (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField()
    description = models.TextField(blank=True)
    Issuer = models.CharField()
    issueDate = models.DateField()
    #associatedWith = list of all academic intitutes of student

class WorkExperience (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    jobTitle = models.CharField()
    company = models.CharField()
    location = models.CharField()
    starDate = models.DateField()
    endDate = models.DateField()
    compensationMin = models.IntegerField()
    compensationMax = models.IntegerField()
    description = models.TextField(blank=True)

class Courses (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    courseCode = models.CharField()
    title = models.CharField()
    gradeSecured = models.CharField(choices=['A', 'A-', 'B', 'B-', 'C', 'C-', 'F'])

class Competitions (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField()
    position = model.CharField()
    #associatedWith = list of all academic intitutes of student
    date = models.DateField()
    description = models.TextField(blank=True)

class PositionsOfResponsibilities (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField()
    description = models.TextField(blank=True)
    fromDate = models.DateField()
    toDate = models.DateField()
    organizationName = models.CharField()

class Documents (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    name = models.CharField()
    link = models.URLField()

class Semester (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    semesterNumber = models.IntegerField()
    sgpa = models.FloatField()
    numberOfBacklogs = models.IntegerField()
    gradeSheetLink = models.URLField()

class Class (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    number = models.IntegerField()
    InstituteName = models.CharField()
    fromDate = models.DateField()
    toDate = models.DateField()
    score = models.FloatField()
    board = models.CharField()
    stream = models.CharField()

class Certifications (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    name = models.CharField()
    issuingAuthority = models.CharField()
    link = models.URLField()
    date = models.DateField()
    licenseNumber = models.CharField()
    hasExpiry = models.BooleanField(default=False)
    description = models.TextField(blank=True)

class ConferencesAndWorkshops (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField()
    description = models.TextField(blank=True)
    organizor = models.charField()
    address = models.TextField()

class CommunicationLanguages (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    language = models.CharField()
    proficiency = models.IntegerField()

class TestScores (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField()
    description = models.TextField(blank=True)
    scoreFormat = models.CharField(choices=[('S', 'Score'), ('R', 'Rank'), ('P', 'Percentile')])
    score = models.FloatField()
    total = models.FloatField()
    examDate = models.DateField()
    #associatedWith = list of all academic intitutes of student