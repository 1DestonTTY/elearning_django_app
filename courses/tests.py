from django.test import TestCase
from django.urls import reverse
from accounts.models import User, Student, Teacher
from .models import Course, Enrollment

class CourseAppTests(TestCase):
    def setUp(self):
        #set up dummy users
        self.teacher_user = User.objects.create_user(username='teacher1', password='pw', is_teacher=True)
        self.student_user = User.objects.create_user(username='student1', password='pw', is_student=True)
        
        self.teacher_profile = self.teacher_user.teacher
        self.student_profile = self.student_user.student
        
        #set up a dummy course
        self.course = Course.objects.create(
            title="Advanced Web Dev Test",
            description="Testing 123",
            teacher=self.teacher_profile
        )

    #model test
    def test_course_creation_and_enrollment(self):
        #check has course created correctly
        self.assertEqual(self.course.title, "Advanced Web Dev Test")
        self.assertEqual(self.course.teacher, self.teacher_profile)
        
        #enroll student using custom enrollment model
        Enrollment.objects.create(course=self.course, student=self.student_profile)
        
        #verify the student count went up to 1
        self.assertEqual(self.course.students.count(), 1)
        self.assertIn(self.student_profile, self.course.students.all())

    #view and security test
    def test_course_detail_login_required(self):
        #try to access the course details without logging in
        url = reverse('course_detail', args=[self.course.id])
        response = self.client.get(url)
        
        #django should block them and redirect (status code 302) to the login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))