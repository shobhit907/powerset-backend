from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# Create your models here.


class Institute(models.Model):
    name = models.CharField(max_length=200)
    logo = models.URLField(blank=True, null=True)


class Student (models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students')
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name='students')
    isVerified = models.BooleanField(default=False)
    entryNumber = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    motherName = models.CharField(max_length=50)
    fatherName = models.CharField(max_length=50)
    preferredProfile = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=10, choices=[(
        'GEN', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')])
    technicalSkills = models.TextField(blank=True)
    introduction = models.TextField(blank=True)
    careerPlans = models.TextField(blank=True)

    def __str__(self):
        return '%s' % self.entryNumber


class SocialProfile (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    github = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    codechef = models.URLField(blank=True)
    codeforces = models.URLField(blank=True)

    def __str__(self):
        return '%s Social profiles' % self.student.entryNumber


class Project (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    startDate = models.DateField()
    endDate = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Project Title: %s' % (self.student.entryNumber, self.title)


class Patent (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    office = models.CharField(max_length=20)
    number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[(
        'P', 'Patent Pending'), ('I', 'Patent Issued')])
    filingDate = models.DateField()

    def __str__(self):
        return '%s Patent Title: %s' % (self.student.entryNumber, self.title)


class Resume (models.Model):
    number = models.IntegerField(validators=[MinValueValidator(1)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    link = models.URLField()
    isLatest = models.BooleanField(default=True)

    def __str__(self):
        return '%s Resume: %s' % (self.student.entryNumber, self.number)


class AwardAndRecognition (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    issuer = models.CharField(max_length=50)
    issueDate = models.DateField()
    # associatedWith = list of all academic intitutes of student

    def __str__(self):
        return '%s Award or Recognition Title: %s' % (self.student.entryNumber, self.title)


class WorkExperience (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
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


class Course (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseCode = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    gradeSecured = models.CharField(max_length=2, choices=[(
        'A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'), ('C', 'C'), ('C-', 'C-'), ('F', 'F')])

    def __str__(self):
        return '%s Course Title: %s' % (self.student.entryNumber, self.title)


class Competition (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    associatedWith = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Competition Title: %s' % (self.student.entryNumber, self.title)


class PositionsOfResponsibility (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    fromDate = models.DateField()
    toDate = models.DateField()
    organizationName = models.CharField(max_length=50)

    def __str__(self):
        return '%s Position of Responsibility Title: %s' % (self.student.entryNumber, self.title)


class Document (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.URLField()

    def __str__(self):
        return '%s Document Name: %s' % (self.student.entryNumber, self.name)


class Semester (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)])
    sgpa = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    numberOfBacklogs = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    gradeSheetLink = models.URLField()

    def __str__(self):
        return '%s Semester Number: %s' % (self.student.entryNumber, self.number)


class Class (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)])
    instituteName = models.CharField(max_length=50)
    fromDate = models.DateField()
    toDate = models.DateField()
    score = models.FloatField()
    board = models.CharField(max_length=50)
    stream = models.CharField(max_length=50)

    def __str__(self):
        return '%s Class Number: %s' % (self.student.entryNumber, self.number)


class Certification (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    issuingAuthority = models.CharField(max_length=50)
    link = models.URLField()
    date = models.DateField()
    licenseNumber = models.CharField(max_length=50)
    hasExpiry = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s Certification Name: %s' % (self.student.entryNumber, self.name)


class ConferencesAndWorkshop (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    organizer = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return '%s Conference or Workshop Title: %s' % (self.student.entryNumber, self.title)


class CommunicationLanguage (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    proficiency = models.CharField(max_length=20, choices=[('1', 'Elementary proficiency'), ('2', 'Limited working proficiency'), (
        '3', 'Professional working proficiency'), ('4', 'Full professional working proficiency'), ('5', 'Native or bilingual proficiency')])

    def __str__(self):
        return '%s Language Name: %s' % (self.student.entryNumber, self.language)


class Exam (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    scoreFormat = models.CharField(max_length=20, choices=[(
        'S', 'Score'), ('R', 'Rank'), ('P', 'Percentile')])
    score = models.FloatField()
    total = models.FloatField(validators=[MinValueValidator(0.0)])
    examDate = models.DateField()
    associatedWith = models.CharField(max_length=200)

    def __str__(self):
        return '%s Test Title: %s' % (self.student.entryNumber, self.title)
