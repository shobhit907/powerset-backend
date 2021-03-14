from django.db import models
from django.conf import settings
from django.utils import timezone
from multiselectfield import MultiSelectField
# Create your models here.

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

class Institute(models.Model):
    name = models.CharField(max_length=200)
    logo = models.FileField(blank=True, null=True, upload_to='logos')

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Placement(models.Model):
    institute = models.ForeignKey(
        Institute, related_name='placements', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now, blank=True)
    end_date = models.DateField(blank=True)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.institute.name+", "+self.name


class Coordinator(models.Model):
    student = models.ForeignKey(
        'student.Student', on_delete=models.CASCADE, related_name='placements_coordinator')
    placement = models.ForeignKey(
        Placement, on_delete=models.CASCADE, related_name='placements')

    class Meta:
        unique_together = ['student', 'placement']

    def __str__(self) -> str:
        return self.student.user.name + ', ' + self.placement.name


class JobProfile(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='job_profiles')
    placement = models.ForeignKey(
        Placement, on_delete=models.CASCADE, related_name='job_profiles')
    title = models.CharField(max_length=200)
    domain = models.CharField(max_length=200, blank=True)
    min_cgpa = models.FloatField(default=0.0, blank=True)
    description = models.TextField()
    min_ctc = models.FloatField()
    max_ctc = models.FloatField()
    start_date = models.DateField(default=timezone.localdate, blank=True)
    end_date = models.DateField(blank=True)
    max_backlogs = models.IntegerField(default=0, blank=True)
    # To-do : add all branches options
    branches_eligible = MultiSelectField(choices=branch_choices)
    job_description = models.FileField(blank=True)
    salary_breakup = models.TextField(blank=True, null=True)
    gender_allowed = models.CharField(
        max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')])
    extra_data = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.placement.name + ', '+self.company.name+', '+self.title


class JobRound(models.Model):
    round_no = models.IntegerField(default=0)
    job_profile = models.ForeignKey(
        JobProfile, on_delete=models.CASCADE, related_name='rounds')
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.job_profile.title+', '+str(self.round_no)


class JobApplicant(models.Model):
    job_profile = models.ForeignKey(
        JobProfile, on_delete=models.CASCADE, related_name='applicants')
    student = models.ForeignKey(
        'student.Student', on_delete=models.CASCADE, related_name='jobs_applied')
    date_applied = models.DateField(auto_now=True, blank=True)
    is_selected = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    job_round = models.ForeignKey(
        JobRound, on_delete=models.CASCADE, related_name='applicants')

    def __str__(self) -> str:
        return self.job_profile.title + ', '+self.student.entry_number+', '+str(self.job_round.round_no)
