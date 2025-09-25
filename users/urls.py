from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ---------------- Landing Page ----------------
    path("", views.landing, name="landing"),

    # ---------------- Registration ----------------
    path("student/register/", views.student_register, name="student_register"),
    path("faculty/register/", views.faculty_register, name="faculty_register"),

    # ---------------- Login ----------------
    path("student/login/", views.student_login, name="student_login"),
    path("faculty/login/", views.faculty_login, name="faculty_login"),

    # ---------------- Dashboards ----------------
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("faculty/dashboard/", views.faculty_dashboard, name="faculty_dashboard"),

    # ---------------- Student Profile ----------------
    path("student/profile/", views.student_profile, name="student_profile"),
    path("student/profile/edit/", views.edit_student_profile, name="edit_student_profile"),

    # ---------------- Faculty Profile ----------------
    path("faculty/profile/", views.faculty_profile, name="faculty_profile"),
    path("faculty/profile/edit/", views.edit_faculty_profile, name="edit_faculty_profile"),

    # ---------------- Student Pages ----------------
    path("student/courses/", views.courses_page, name="courses_page"),
    path(
        "student/courses/<int:course_id>/materials/",
        views.view_course_materials,
        name="view_course_materials",
    ),
    path("student/attendance/", views.attendance_page, name="attendance_page"),
    path("student/results/", views.results_page, name="results_page"),
    path("student/assignments/", views.assignments_page, name="assignments_page"),
    path(
        "student/assignments/<int:assignment_id>/submit/",
        views.submit_assignment,
        name="submit_assignment",
    ),

    # ---------------- Faculty Pages ----------------
    path("faculty/courses/", views.faculty_courses, name="faculty_courses"),
    path("faculty/courses/create/", views.create_course, name="create_course"),
    path(
        "faculty/courses/<int:course_id>/materials/upload/",
        views.upload_course_material,
        name="upload_course_material",
    ),
    path("faculty/attendance/", views.faculty_attendance, name="faculty_attendance"),
    path("faculty/results/", views.faculty_results, name="faculty_results"),
    path("faculty/assignments/", views.faculty_assignments, name="faculty_assignments"),
    path("faculty/assignments/create/", views.create_assignment, name="create_assignment"),
    path(
        "faculty/assignments/<int:assignment_id>/submissions/",
        views.view_submissions,
        name="view_submissions",
    ),

    # ---------------- Logout ----------------
    path("logout/", views.user_logout, name="user_logout"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
