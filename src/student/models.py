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
    category = models.CharField(max_length=10, choices=['GEN', 'OBC', 'SC', 'ST'])
    technicalSkills = models.TextField(blank=True)
    introduction = models.TextField(blank=True)
    careerPlans = mdoels.TextField(blank=True)

    def __str__(self):
        return '%s' % self.entryNumber

class SocialProfiles (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    github = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    codechef = models.URLField(blank=True)
    codeforces = models.URLField(blank=True)

    def __str__(self):
        return '%s Social profiles' % self.student.entryNumber

class Projects (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    startDate = models.DateField()
    endDate = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Project Title: %s' % (self.student.entryNumber, self.title)

class Patents (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    Office = CountryField()
    Number = models.CharField(max_length=50)
    Status = models.CharField(max_length=20, choices=[ ('P', 'Patent Pending'), ('I', 'Patent Issued')])
    filingDate = models.DateField()

    def __str__(self):
        return '%s Patent Title: %s' % (self.student.entryNumber, self.title)

class Resumes (models.Model):
    number = models.IntegerField(validators=[MinValueValidator(1)])
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    link = models.URLField()
    isLatest = models.BooleanField(default=True)

    def __str__(self):
        return '%s Resume: %s' % (self.student.entryNumber, self.number)

class AwardsAndRecognitions (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    Issuer = models.CharField(max_length=50)
    issueDate = models.DateField()
    #associatedWith = list of all academic intitutes of student

    def __str__(self):
        return '%s Award or Recognition Title: %s' % (self.student.entryNumber, self.title)

class WorkExperiences (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    jobTitle = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    starDate = models.DateField()
    endDate = models.DateField()
    compensationMin = models.IntegerField(validators=[MinValueValidator(0)])
    compensationMax = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Work Experience Title: %s' % (self.student.entryNumber, self.jobTitle)

class Courses (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    courseCode = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    gradeSecured = models.CharField(choices=['A', 'A-', 'B', 'B-', 'C', 'C-', 'F'])

    def __str__(self):
        return '%s Course Title: %s' % (self.student.entryNumber, self.title)

class Competitions (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    position = model.CharField(max_length=50)
    #associatedWith = list of all academic intitutes of student
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Competition Title: %s' % (self.student.entryNumber, self.title)

class PositionsOfResponsibilities (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    fromDate = models.DateField()
    toDate = models.DateField()
    organizationName = models.CharField(max_length=50)

    def __str__(self):
        return '%s Position of Responsibility Title: %s' % (self.student.entryNumber, self.title)

class Documents (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.URLField()

    def __str__(self):
        return '%s Document Name: %s' % (self.student.entryNumber, self.name)

class Semester (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    sgpa = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    numberOfBacklogs = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100))
    gradeSheetLink = models.URLField()

    def __str__(self):
        return '%s Semester Number: %s' % (self.student.entryNumber, self.number)

class Class (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12))
    InstituteName = models.CharField(max_length=50)
    fromDate = models.DateField()
    toDate = models.DateField()
    score = models.FloatField()
    board = models.CharField(max_length=50)
    stream = models.CharField(max_length=50)

    def __str__(self):
        return '%s Class Number: %s' % (self.student.entryNumber, self.number)

class Certifications (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    issuingAuthority = models.CharField(max_length=50)
    link = models.URLField()
    date = models.DateField()
    licenseNumber = models.CharField(max_length=50)
    hasExpiry = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Certification Name: %s' % (self.student.entryNumber, self.name)

class ConferencesAndWorkshops (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    organizor = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return '%s Conference or Workshop Title: %s' % (self.student.entryNumber, self.title)

class CommunicationLanguages (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    language = models.CharField(max_length=50)
    proficiency = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5))

    def __str__(self):
        return '%s Language Name: %s' % (self.student.entryNumber, self.language)

class TestScores (models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    scoreFormat = models.CharField(choices=[('S', 'Score'), ('R', 'Rank'), ('P', 'Percentile')])
    score = models.FloatField()
    total = models.FloatField(validators=[MinValueValidator(0.0)])
    examDate = models.DateField()
    #associatedWith = list of all academic intitutes of student

    def __str__(self):
        return '%s Test Title: %s' % (self.student.entryNumber, self.title)