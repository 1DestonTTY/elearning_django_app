from django import forms
from .models import Course, CourseMaterial, CourseFeedback

#course creation form
class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

#course material form
class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'file']

#course feedback form
class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave your feedback here...'}),
        }