from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ---------------- User Profile ----------------
class Profile(models.Model):
    ROLE_CHOICES = (('student', 'Student'), ('faculty', 'Faculty'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ---------------- Student ----------------
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    roll_no = models.CharField(max_length=50, blank=True, null=True)
    semester = models.PositiveIntegerField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    parent_phone = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    signature = models.ImageField(upload_to='student_signatures/', blank=True, null=True)

    def __str__(self):
        return f"StudentProfile: {self.user.username}"


# ---------------- Faculty ----------------
class FacultyProfile(models.Model):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='facultyprofile')
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='faculty_photos/', blank=True, null=True)

    def __str__(self):
        return f"FacultyProfile: {self.user.username}"


# ---------------- Courses ----------------
class Course(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f"{self.code} - {self.name}"


# ---------------- Course Materials ----------------
class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="course_materials/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.code})"


# ---------------- Attendance ----------------
class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendances")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student.user.username} - {self.course.code} - {self.date} - {self.status}"


# ---------------- Assignment ----------------
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    file = models.FileField(upload_to='assignments/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"


# ---------------- Assignment Submission ----------------
class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="assignment_submissions")
    submitted_file = models.FileField(upload_to='assignment_submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"


# ---------------- Signals ----------------
@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_related_profiles(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    if hasattr(instance, 'studentprofile'):
        instance.studentprofile.save()
    if hasattr(instance, 'facultyprofile'):
        instance.facultyprofile.save()
