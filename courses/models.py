from django.db import models
from accounts.models import Teacher, Student
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

#----------------------course-------------------------
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(Student, through='Enrollment', related_name='enrolled_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        #ensures a student cant enroll in the exact same course twice
        unique_together = ('course', 'student')

#-----------------------course material---------------------
class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_materials/') #this handles pdf and image automatically
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"
    
#--------------------course feedback------------------------
class CourseFeedback(models.Model):
    #links the feedback to a specific course
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.student.user.real_name} for {self.course.title}"

#--------------------delete file ------------------------
@receiver(post_delete, sender=CourseMaterial)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    #delete file from server when coursematerial object is deleted from db
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
