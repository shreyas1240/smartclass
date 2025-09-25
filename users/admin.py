from django.contrib import admin
from .models import (
    Profile,
    StudentProfile,
    FacultyProfile,
    Course,
    CourseMaterial,
    Attendance,
    Assignment,
    AssignmentSubmission,
)

# ---------------- Profile Admin ----------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    search_fields = ("user__username", "user__email", "role")
    list_filter = ("role",)


# ---------------- Student Profile Admin ----------------
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_no", "department", "semester")
    search_fields = ("user__username", "user__email", "roll_no")
    list_filter = ("department", "semester")


# ---------------- Faculty Profile Admin ----------------
@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "employee_id",
        "designation",
        "department",
        "phone_number",
        "date_of_birth",
        "gender",
    )
    search_fields = ("user__username", "user__email", "employee_id", "designation")
    list_filter = ("department", "gender")
    date_hierarchy = "date_of_birth"


# ---------------- Course Admin ----------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "faculty")
    search_fields = ("code", "name", "faculty__user__username")
    list_filter = ("faculty__department",)


# ---------------- Course Materials Admin ----------------
@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "uploaded_at")
    search_fields = ("title", "course__name", "course__code")
    list_filter = ("course", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)


# ---------------- Attendance Admin ----------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date", "status")
    search_fields = ("student__user__username", "course__code", "course__name")
    list_filter = ("course", "status", "date")
    date_hierarchy = "date"
    ordering = ("-date",)


# ---------------- Assignment Admin ----------------
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "due_date")
    search_fields = ("title", "course__name", "course__code")
    list_filter = ("course", "due_date")
    date_hierarchy = "due_date"
    ordering = ("-due_date",)


# ---------------- Assignment Submission Admin ----------------
@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "submitted_file", "submitted_at")
    search_fields = ("assignment__title", "student__user__username", "student__roll_no")
    list_filter = ("assignment", "submitted_at")
    readonly_fields = ("submitted_at",)
    date_hierarchy = "submitted_at"
    ordering = ("-submitted_at",)
