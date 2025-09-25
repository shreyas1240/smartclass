from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import (
    StudentProfile,
    FacultyProfile,
    Course,
    Attendance,
    Assignment,
    AssignmentSubmission,
    CourseMaterial,
)
from .forms import (
    StudentProfileForm,
    FacultyProfileForm,
    AssignmentForm,
    AssignmentSubmissionForm,
    CourseForm,
    CourseMaterialForm,
)

# ---------------- Landing ----------------
def landing(request):
    """Public landing page."""
    return render(request, "users/landing.html")


# ---------------- Registration ----------------
def student_register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Please provide username and password.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            StudentProfile.objects.get_or_create(user=user)
            messages.success(request, "Student registration successful.")
            return redirect("student_login")
    return render(request, "users/student_register.html")


def faculty_register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Please provide username and password.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            FacultyProfile.objects.get_or_create(user=user)
            messages.success(request, "Faculty registration successful.")
            return redirect("faculty_login")
    return render(request, "users/faculty_register.html")


# ---------------- Login ----------------
def student_login(request):
    if request.user.is_authenticated and hasattr(request.user, "studentprofile"):
        return redirect("student_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, "studentprofile"):
            login(request, user)
            return redirect("student_dashboard")
        messages.error(request, "Invalid credentials or not a student.")
    return render(request, "users/student_login.html")


def faculty_login(request):
    if request.user.is_authenticated and hasattr(request.user, "facultyprofile"):
        return redirect("faculty_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, "facultyprofile"):
            login(request, user)
            return redirect("faculty_dashboard")
        messages.error(request, "Invalid credentials or not a faculty.")
    return render(request, "users/faculty_login.html")


# ---------------- Dashboards ----------------
@login_required
def student_dashboard(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    return render(request, "users/student_dashboard.html", {"student": student})


@login_required
def faculty_dashboard(request):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    return render(request, "users/faculty_dashboard.html", {"faculty": faculty})


# ---------------- Profiles ----------------
@login_required
def student_profile(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    return render(request, "users/student_profile.html", {"student": student})


@login_required
def edit_student_profile(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("student_profile")
    else:
        form = StudentProfileForm(instance=student)
    return render(request, "users/edit_student_profile.html", {"form": form, "student": student})


@login_required
def faculty_profile(request):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    return render(request, "users/faculty_profile.html", {"faculty": faculty})


@login_required
def edit_faculty_profile(request):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    if request.method == "POST":
        form = FacultyProfileForm(request.POST, request.FILES, instance=faculty)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty profile updated successfully.")
            return redirect("faculty_profile")
    else:
        form = FacultyProfileForm(instance=faculty)
    return render(request, "users/edit_faculty_profile.html", {"form": form, "faculty": faculty})


# ---------------- Student Pages ----------------
@login_required
def courses_page(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    courses = Course.objects.all()
    return render(request, "users/courses.html", {"student": student, "courses": courses})


@login_required
def view_course_materials(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = CourseMaterial.objects.filter(course=course)
    return render(request, "users/view_course_materials.html", {"course": course, "materials": materials})


@login_required
def attendance_page(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    records = Attendance.objects.filter(student=student).order_by("date")
    course_stats = {}
    for rec in records:
        c = rec.course
        course_stats.setdefault(c, {"total": 0, "present": 0})
        course_stats[c]["total"] += 1
        if rec.status == "Present":
            course_stats[c]["present"] += 1
    for c, stats in course_stats.items():
        total = stats["total"]
        stats["percentage"] = round((stats["present"] / total) * 100, 2) if total else 0
    return render(
        request,
        "users/attendance.html",
        {"student": student, "records": records, "course_stats": course_stats},
    )


@login_required
def results_page(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    courses = Course.objects.all()
    return render(request, "users/results.html", {"student": student, "courses": courses})


# ---------------- Student Assignments ----------------
@login_required
def assignments_page(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    assignments = Assignment.objects.filter(course__in=student.course_set.all())
    submission_status = {
        a.id: AssignmentSubmission.objects.filter(assignment=a, student=student).first()
        for a in assignments
    }
    return render(
        request,
        "users/assignments_page.html",
        {"student": student, "assignments": assignments, "submission_status": submission_status},
    )


@login_required
def submit_assignment(request, assignment_id):
    student = get_object_or_404(StudentProfile, user=request.user)
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=student).first()
    submitted = submission is not None

    if request.method == "POST" and not submitted:
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.assignment = assignment
            new_submission.student = student
            new_submission.save()
            messages.success(request, "Assignment submitted successfully.")
            return redirect("assignments_page")
    else:
        form = AssignmentSubmissionForm()

    return render(
        request,
        "users/submit_assignment.html",
        {"form": form, "assignment": assignment, "submitted": submitted, "submission": submission},
    )


# ---------------- Faculty Pages ----------------
@login_required
def faculty_courses(request):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    courses = Course.objects.filter(faculty=faculty)
    return render(request, "users/faculty_courses.html", {"faculty": faculty, "courses": courses})


@login_required
def create_course(request):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.faculty = faculty
            course.save()
            messages.success(request, "Course created successfully.")
            return redirect("faculty_courses")
    else:
        form = CourseForm()
    return render(request, "users/create_course.html", {"form": form, "faculty": faculty})


@login_required
def upload_course_material(request, course_id):
    """Upload course material (with file)."""
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    course = get_object_or_404(Course, id=course_id, faculty=faculty)
    if request.method == "POST":
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            messages.success(request, "Material uploaded successfully.")
            return redirect("faculty_courses")
    else:
        form = CourseMaterialForm()
    return render(
        request,
        "users/upload_course_material.html",
        {"form": form, "course": course, "faculty": faculty},
    )


@login_required
def faculty_attendance(request):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    courses = Course.objects.filter(faculty=faculty)
    selected_course_id = request.GET.get("course")
    selected_date_str = request.GET.get("date")
    try:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date() if selected_date_str else date.today()
    except Exception:
        selected_date = date.today()
    students = []
    attendance_records = {}
    if selected_course_id:
        course = get_object_or_404(Course, id=selected_course_id, faculty=faculty)
        students = StudentProfile.objects.filter(course=course)  # FIXED: only course students
        attendance_records = {
            att.student.id: att.status
            for att in Attendance.objects.filter(course=course, date=selected_date)
        }
        if request.method == "POST":
            for s in students:
                status = request.POST.get(f"status_{s.id}", "Absent")
                Attendance.objects.update_or_create(
                    student=s,
                    course=course,
                    date=selected_date,
                    defaults={"status": status},
                )
            messages.success(request, f"Attendance for {course.name} on {selected_date} saved.")
            return redirect(f"{request.path}?course={course.id}&date={selected_date}")
    return render(
        request,
        "users/faculty_attendance.html",
        {
            "faculty": faculty,
            "courses": courses,
            "students": students,
            "attendance_records": attendance_records,
            "selected_course_id": selected_course_id,
            "selected_date": selected_date,
        },
    )


@login_required
def faculty_results(request):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    courses = Course.objects.filter(faculty=faculty)
    return render(request, "users/faculty_results.html", {"faculty": faculty, "courses": courses})


@login_required
def create_assignment(request):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            if assignment.course.faculty == faculty:
                assignment.save()
                messages.success(request, "Assignment created successfully.")
                return redirect("faculty_assignments")
            messages.error(request, "Invalid course selection.")
    else:
        form = AssignmentForm()
    return render(request, "users/create_assignment.html", {"form": form, "faculty": faculty})


@login_required
def faculty_assignments(request):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    courses = Course.objects.filter(faculty=faculty)
    assignments = Assignment.objects.filter(course__faculty=faculty)
    form = AssignmentForm()
    return render(
        request,
        "users/faculty_assignments.html",
        {"faculty": faculty, "courses": courses, "assignments": assignments, "form": form},
    )


@login_required
def view_submissions(request, assignment_id):
    faculty = get_object_or_404(FacultyProfile, user=request.user)
    assignment = get_object_or_404(Assignment, id=assignment_id, course__faculty=faculty)
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)
    return render(
        request,
        "users/view_submissions.html",
        {"faculty": faculty, "assignment": assignment, "submissions": submissions},
    )


# ---------------- Logout ----------------
def user_logout(request):
    logout(request)
    return redirect("landing")
