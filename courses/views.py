from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, CourseMaterial, CourseFeedback, Enrollment
from .forms import CourseCreationForm, CourseMaterialForm, CourseFeedbackForm
from accounts.models import Student, Notification

#-----------------course create----------------------
@login_required
def create_course(request):
    #only teacher can create courses
    if not request.user.is_teacher:
        return redirect('home')

    #handle create course
    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user.teacher 
            course.save()
            return redirect('course_list')
    else:
        form = CourseCreationForm()
    
    return render(request, 'courses/create_course.html', {'form': form})

#-------------------course list----------------------
@login_required
def course_list(request):
    query = request.GET.get('q') #get search term 
    
    if query:
        #filter courses by title
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()
        
    return render(request, 'courses/course_list.html', {'courses': courses})

#----------------student enroll in course--------------
@login_required
def enroll_course(request, course_id):
    #only students can enroll
    if not request.user.is_student:
        return redirect('home')
        
    #get the specific course
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student
    
    if not Enrollment.objects.filter(course=course, student=student).exists():
        Enrollment.objects.create(course=course, student=student)
        
        Notification.objects.create(
            recipient=course.teacher.user,
            message=f"{student.user.real_name} has enrolled in your course: {course.title}"
        )
    
    return redirect('course_list')

#------------------course detail---------------------
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    #check current viewer is the owner of the course
    is_teacher = request.user.is_teacher and course.teacher.user == request.user

    #handle material uploads
    if request.method == 'POST' and is_teacher:
        form = CourseMaterialForm(request.POST, request.FILES) 
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course 
            material.save()

            #notification alert for all enrolled students
            for student in course.students.all():
                Notification.objects.create(
                    recipient=student.user,
                    message=f"New material '{material.title}' was added to {course.title}"
                )

            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseMaterialForm()

    #empty feedback form for student 
    feedback_form = CourseFeedbackForm()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'materials': course.materials.all(), 
        'form': form,
        'is_teacher': is_teacher,
        'feedback_form': feedback_form,
    })

#-------------delete course material--------------
@login_required
def delete_material(request, material_id):
    material = get_object_or_404(CourseMaterial, id=material_id)
    course = material.course
    
    #only the teacher of exact course can delete 
    if request.user.is_teacher and course.teacher.user == request.user:
        if request.method == 'POST':
            material.delete()
            
    #redirect back to the course detail page
    return redirect('course_detail', course_id=course.id)

#----------------course feedback------------------
@login_required
def add_feedback(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    #only student post are allow
    if request.method == 'POST' and request.user.is_student:
        #check if the student is actually enrolled in the course
        if request.user.student in course.students.all():
            form = CourseFeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.course = course
                feedback.student = request.user.student
                feedback.save()
                
    #redirect back to the course page
    return redirect('course_detail', course_id=course.id)

#---------------------course roster--------------------
@login_required
def course_roster(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    #only the teacher of the course can see the roster
    if not request.user.is_teacher or course.teacher.user != request.user:
        return redirect('course_detail', course_id=course.id)

    #redirect back to roster page
    return render(request, 'courses/course_roster.html', {'course': course})

#----------------------remove student------------------
@login_required
def remove_student(request, course_id, student_id):
    course = get_object_or_404(Course, id=course_id)
    
    #only teacher of this exact course can remove students
    if request.user.is_teacher and course.teacher.user == request.user:
        
        if request.method == 'POST':
            student_to_remove = get_object_or_404(Student, pk=student_id)
            Enrollment.objects.filter(course=course, student=student_to_remove).delete()
            
    #redirect back to the roster page
    return redirect('course_roster', course_id=course.id)

#-----------------------student enrollment------------------
@login_required
def student_enrollments(request):
    #only students can access this page
    if not request.user.is_student:
        return redirect('home')
    
    #filter courses to show the student has joined in which courses
    enrolled_courses = Course.objects.filter(students=request.user.student)
    
    return render(request, 'courses/student_enrollments.html', {'courses': enrolled_courses})