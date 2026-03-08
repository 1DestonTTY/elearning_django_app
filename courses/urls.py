from django.urls import path
from . import views

urlpatterns = [
    #show course list
    path('', views.course_list, name='course_list'),

    #create course page
    path('create/', views.create_course, name='create_course'),

    #get the id course and pass it to enroll course view
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    
    #show detail of specific course
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    
    #show the student list from a specific course
    path('<int:course_id>/roster/', views.course_roster, name='course_roster'),
    
    #remove student by id
    path('<int:course_id>/remove/<int:student_id>/', views.remove_student, name='remove_student'),
    
    #show logged in student a list of their enroll course
    path('my-enrollments/', views.student_enrollments, name='student_enrollments'),
    
    #submit feedback
    path('<int:course_id>/feedback/', views.add_feedback, name='add_feedback'),

    #delete course material
    path('material/<int:material_id>/delete/', views.delete_material, name='delete_material'),
]