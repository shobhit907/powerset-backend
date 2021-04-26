from student.models import Student, Semester
from .models import JobRound
from django.core.mail import send_mail
import os

# def CreateJobRound(roundNo, jobProfile):
#     jobRound = JobRound()

def GetNumberOfBacklogs(student):
    noOfBacklogs = 0
    semesters = Semester.objects.filter(student=student)
    for semester in semesters:
        noOfBacklogs += semester.number_of_backlogs
    return noOfBacklogs

def SendEmailToEligibleStudents(jobProfile):

    # print(jobProfile.gender_allowed)
    #Get list of eligible students
    eligibleStudents = Student.objects.filter(cgpa__gte=jobProfile.min_cgpa, gender__in=jobProfile.gender_allowed, branch__in=jobProfile.branches_eligible, is_selected=False)

    # for student in eligibleStudents:
    #     print(student.gender)

    #filtering students based on their backlogs
    uneligibleIds = []
    for student in eligibleStudents:
        noOfBacklogs = GetNumberOfBacklogs(student)                 #Calculate backlogs
        if (noOfBacklogs > jobProfile.max_backlogs):
            uneligibleIds.append(student.id)
    eligibleStudents = eligibleStudents.exclude(id__in=uneligibleIds)

    # for student in eligibleStudents:
    #     print(student.id)

    # print(uneligibleIds)

    recepients = []
    for student in eligibleStudents:
        recepients.append(student.user.email)

    # print(recepients)

    subject = 'Open for application - ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title)
    message = 'Dear Student,\n\nYou are eligible for applying in ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title) + '. Please make sure to apply for the same before ' + str(jobProfile.end_date) + '.\n\nRegards\nPowerset team'
    send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), recepients, fail_silently = False)