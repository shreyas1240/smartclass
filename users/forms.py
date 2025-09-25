from django import forms
from django.contrib.auth.models import User
from .models import (
    StudentProfile,
    FacultyProfile,
    Assignment,
    AssignmentSubmission,
    Course,
    CourseMaterial,
)

# -------------------------------------------------------------------
# Student Profile Form
# -------------------------------------------------------------------
class StudentProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = StudentProfile
        fields = [
            "roll_no", "semester", "department",
            "father_name", "mother_name", "address",
            "mobile_number", "parent_phone",
            "photo", "signature",
        ]
        widgets = {
            "address": forms.Textarea(attrs={
                "rows": 2,
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "photo": forms.ClearableFileInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "signature": forms.ClearableFileInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.email = self.cleaned_data.get("email", user.email)
        if commit:
            user.save()
            profile.save()
        return profile


# -------------------------------------------------------------------
# Faculty Profile Form
# -------------------------------------------------------------------
class FacultyProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    full_name = forms.CharField(required=True, label="Full Name")
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
        }),
    )
    gender = forms.ChoiceField(
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        required=False,
        widget=forms.Select(attrs={
            "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
        }),
    )

    class Meta:
        model = FacultyProfile
        fields = [
            "full_name", "email", "employee_id", "designation", "department",
            "phone_number", "address", "qualifications", "experience", "photo",
            "date_of_birth", "gender", "father_name", "mother_name",
        ]
        widgets = {
            "address": forms.Textarea(attrs={
                "rows": 2,
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "qualifications": forms.Textarea(attrs={
                "rows": 2,
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "experience": forms.Textarea(attrs={
                "rows": 2,
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "photo": forms.ClearableFileInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email
            self.fields["full_name"].initial = self.instance.user.get_full_name()

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.email = self.cleaned_data.get("email", user.email)
        full_name = self.cleaned_data.get("full_name", user.get_full_name())
        if " " in full_name:
            user.first_name, user.last_name = full_name.split(" ", 1)
        else:
            user.first_name = full_name
            user.last_name = ""
        if commit:
            user.save()
            profile.save()
        return profile


# -------------------------------------------------------------------
# Course Form
# -------------------------------------------------------------------
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["code", "name"]
        widgets = {
            "code": forms.TextInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter course code",
            }),
            "name": forms.TextInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter course name",
            }),
        }


# -------------------------------------------------------------------
# Course Material Form
# -------------------------------------------------------------------
class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ["course", "title", "description", "file"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "description": forms.Textarea(attrs={
                "rows": 2,
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "file": forms.ClearableFileInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
        }


# -------------------------------------------------------------------
# Assignment Form
# -------------------------------------------------------------------
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["course", "title", "description", "due_date", "file"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "description": forms.Textarea(attrs={
                "rows": 2,
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "due_date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
            "file": forms.ClearableFileInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
        }


# -------------------------------------------------------------------
# Assignment Submission Form
# -------------------------------------------------------------------
class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ["submitted_file"]
        widgets = {
            "submitted_file": forms.ClearableFileInput(attrs={
                "class": "w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
            }),
        }
