from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('home_page', views.home_page, name="home_page"),
    path('login',views.login, name='login'),

    # staff side
    path('teacher_home', views.teacher_home, name="teacher_home"),
    path('teacher_view_profile', views.teacher_view_profile, name='teacher_view_profile'),

    # student registration
    path('teacher_view_feedback', views.teacher_view_feedback, name='teacher_view_feedback'),
    path('staff_view_cnotification', views.staff_view_cnotification, name='staff_view_cnotification'),
    path('staff_view_department', views.staff_view_department, name='staff_view_department'),
    path('staff_view_course/<int:id>', views.staff_view_course, name='staff_view_course'),
    path('staff_view_semester/<int:id>', views.staff_view_semester, name='staff_view_semester'),
    path('staff_view_notification/<int:id>', views.staff_view_notification, name='staff_view_notification'),
    path('staff_view_timetable/<int:id>', views.staff_view_timetable, name='staff_view_timetable'),
    path('register_student/<int:id>', views.register_student, name='register_student'),
    path('signup', views.stud_register, name='stud_register'),
    path('attendence/<int:id>', views.attendence, name='attendence'),
    path('make_attendence', views.make_attendence, name='make_attendence'),
    path('view_attendence/<int:id>', views.view_attendence, name='view_attendence'),
    path('remove_attendence/<int:id>', views.remove_attendence, name='remove_attendence'),
    path('internals/<int:id>', views.internals, name='internals'),
    path("make_internal",views.make_internal, name='make_internal'),
    path('view_internal/<int:id>', views.view_internal, name='view_internal'),
    path('remove_internal/<int:id>', views.remove_internal, name='remove_internal'),

    #------------admin side-------------
    path('admin_home', views.admin_home, name="admin_home"),

    # college unotification
    path('upload_cnotification', views.upload_cnotification, name='upload_cnotification'),
    path('add_cnotification', views.add_cnotification, name='add_cnotification'),
    path('view_cnotification', views.view_cnotification, name='view_cnotification'),

    # department,course, subject  table maintaining
    path('reg_dep', views.reg_dep, name='reg_dep'),
    path('add_dep', views.add_dep, name='add_dep'),
    path('view_department', views.view_department, name='view_department'),
    path('reg_course/<int:id>', views.reg_course, name='reg_course'),
    path('add_course/<int:id>', views.add_course, name='add_course'),
    path('view_course/<int:id>', views.view_course, name='view_course'),
    path('reg_subject/<int:id>', views.reg_subject, name='reg_subject'),
    path('add_subject/<int:id>', views.add_subject, name='add_subject'),
    path('view_subject/<int:id>', views.view_subject, name='view_subject'),
    path('admin_view_semester/<int:id>', views.admin_view_semester, name='admin_view_semester'),
    path('reg_timetable/<str:id>/<str:sem>', views.reg_timetable, name='reg_timetable'),
    path('add_timetable/<int:id>', views.add_timetable, name='add_timetable'),
    path('view_timetable/<int:id>', views.view_timetable, name='view_timetable'),

    # university unotification
    path('upload_notification/<int:id>', views.upload_notification, name='upload_notification'),
    path('add_notification/<int:id>', views.add_notification, name='add_notification'),
    path('view_notification/<int:id>', views.view_notification, name='view_notification'),


    # staff registration
    path('add_staff', views.add_staff, name='add_staff'),
    path('staff_register', views.staff_register, name="staff_register"),
    path('view_staff', views.view_staffreg_, name='view_staffreg_'),

    # student home
    path('student_home', views.student_home, name='student_home'),
    path('stud_view_profile', views.stud_view_profile, name='stud_view_profile'),
    path('stud_view_department', views.stud_view_department, name='stud_view_department'),
    path('change_password/<int:id>', views.change_password, name='change_password'),
    path('update_password',views.update_password, name='update_password'),
    path('teacher_change_password/<str:id>', views.teacher_change_password, name='teacher_change_password'),
    path('teacher_update_password',views.teacher_update_password, name='teacher_update_password'),
    path('manager_change_password/<str:id>', views.manager_change_password, name='manager_change_password'),
    path('manager_update_password',views.manager_update_password, name='manager_update_password'),
    path('mentor_change_password/<str:id>', views.mentor_change_password, name='mentor_change_password'),
    path('mentor_update_password',views.mentor_update_password, name='mentor_update_password'),

    path('stud_view_cnotification', views.stud_view_cnotification, name='stud_view_cnotification'),
    path('stud_view_course/<int:id>', views.stud_view_course, name='stud_view_course'),
    path('stud_view_subject/<int:id>', views.stud_view_subject, name='stud_view_subject'),
    path('stud_view_timetable/<int:id>', views.stud_view_timetable, name='stud_view_timetable'),
    path('stud_view_notification/<int:id>', views.stud_view_notification, name='stud_view_notification'),
    path('stud_leave_status', views.stud_leave_status, name='stud_leave_status'),
    path('send_feedback', views.send_feedback, name="send_feedback"),
    path('sendfb', views.sendfb, name="sendfb"),
    path('view_fb', views.view_fb, name="view_fb"),
    path('apply_leaves', views.apply_leaves, name="apply_leave"),
    path('sendleave', views.sendleave, name="sendleave"),
    path('view_leaves', views.view_leaves, name='view_leaves'),
    path('stud_view_attendance/<int:id>', views.stud_view_attendance, name='stud_view_attendance'),
    path('stud_view_internals/<int:id>', views.stud_view_internals, name='stud_view_internals'),

    path('manager_home', views.manager_home, name='manager_home'),
    path('manager_view_profile', views.manager_view_profile, name='manager_view_profile'),
    path('manager_view_department', views.manager_view_department, name='manager_view_department'),
    path('manager_view_course/<int:id>', views.manager_view_course, name='manager_view_course'),
    path('manager_view_semester/<int:id>', views.manager_view_semester, name='manager_view_semester'),
    path('manager_view_notification/<int:id>', views.manager_view_notification, name='manager_view_notification'),
    path('manager_view_timetable/<int:id>', views.manager_view_timetable, name='manager_view_timetable'),
    path('managerr_view_attendance/<str:id>', views.manager_view_attendance, name='manager_view_attendance'),
    path('manager_add_fees/<str:id>', views.manager_add_fees, name='manager_add_fees'),
    path('add_fees_type/<str:id>', views.add_fees_type, name='add_fees_type'),
    path('manager_view_fees/<str:id>', views.manager_view_fees, name='manager_view_fees'),


    path('manager_stud_fees/<str:id>', views.manager_stud_fees, name='manager_stud_fees'),
    path('approve_stud_fees/<str:id>', views.approve_stud_fees, name='approve_stud_fees'),
    path('reject_stud_fees/<str:id>', views.reject_stud_fees, name='reject_stud_fees'),
    path('update_to_next_sem/<str:id>', views.update_to_next_sem, name='update_to_next_sem'),
    path('teacher_stud_fees/<str:id>',views.teacher_stud_fees, name='teacher_stud_fees'),



    path('mentor_home', views.mentor_home, name='mentor_home'),
    path('mentor_view_profile', views.mentor_view_profile, name='mentor_view_profile'),
    path('mentor_view_cnotification', views.mentor_view_cnotification, name='mentor_view_cnotification'),
    path('mentor_view_department', views.mentor_view_department, name='mentor_view_department'),
    path('mentor_view_course/<int:id>', views.mentor_view_course, name='mentor_view_course'),
    path('mentor_view_semester/<int:id>', views.mentor_view_semester, name='mentor_view_semester'),
    path('mentor_view_notification/<int:id>', views.mentor_view_notification, name='mentor_view_notification'),
    path('mentor_view_timetable/<int:id>', views.mentor_view_timetable, name='mentor_view_timetable'),
    path('mentor_view_attendance/<str:id>',views.mentor_view_attendance, name='mentor_view_attendance'),
    path('mentor_view_leaves', views.mentor_view_leaves, name='mentor_view_leaves'),
    path('approve_pending_leave/<int:id>', views.approve_pending_leave, name='approve_pending_leave'),
    path('reject_pending_leave/<int:id>', views.reject_pending_leave, name='reject_pending_leave'),




    path('stud_attend', views.stud_attend, name="stud_attend"),
    path('stud_course', views.stud_course, name="stud_course"),
    path('stud_feedback', views.stud_feedback, name="stud_feedback"),
    path('stud_leave', views.stud_leave, name="stud_leave"),
    path('stud_view_fees/<str:id>', views.stud_view_fees, name='stud_view_fees'),
    path('stud_add_fees/<str:id>', views.stud_add_fees, name='stud_add_fees'),
    path('proceed_payment_details/<str:id>',views.proceed_payment_details, name='proceed_payment_details'),

    path('sub_entre', views.sub_entre, name="sub_entre"),
    path('view_attend_', views.view_attend_, name="view_attend_"),
    path('edit_attend_', views.edit_attend_, name="edit_attend_"),
    path('view_course_', views.view_course_, name="view_course_"),
    path('edit_coursedetails_/<int:sid>', views.edit_coursedetails_, name="edit_coursedetails_"),
    path('view_feedback_', views.view_feedback_, name="view_feedback_"),
    path('edit_feedback_/<int:sid>', views.edit_feedback_, name="edit_feedback_"),
    path('view_leave_', views.view_leave_, name="view_leave_"),
    path('edit_leave_/<int:sid>', views.edit_leave_, name="edit_leave_"),
    path('view_staffreg_', views.view_staffreg_, name="view_staffreg_"),
    path('edit_staffreg_/<int:sid>', views.edit_staffreg_, name="edit_staffreg_"),
    path('view_studreg_', views.view_studreg_, name="view_studreg_"),
    path('edit_studreg_/<int:sid>', views.edit_studreg_, name="edit_studreg_"),
    path('view_sub_', views.view_sub_, name="view_sub_"),
    path('edit_sub_/<int:sid>', views.edit_sub_, name="edit_sub_"),
    path('delete_attendence/<int:id>', views.delete_attendence, name="delete_attendence"),
    path('delete_course/<int:aid>', views.delete_course, name="delete_course"),
    path('delete_feedback/<int:fid>', views.delete_feedback, name="delete_feedback"),
    path('delete_fees_payment/<int:feid>', views.delete_fees_payment, name="delete_fees_payment"),
    path('delete_internal_mark/<int:imid>', views.delete_internal_mark, name="delete_internal_mark"),
    path('delete_late_attendence/<int:laid>', views.delete_late_attendence, name="delete_late_attendence"),
    path('delete_leave/<int:leaveid>', views.delete_leave, name="delete_leave"),
    path('delete_notification/<int:nid>', views.delete_notification, name="delete_notification"),
    path('delete_staff_details/<int:sdid>', views.delete_staff_details, name="delete_staff_details"),
    path('delete_sudent/<int:sid>', views.delete_sudent, name="delete_sudent"),
    path('delete_subject/<int:suid>', views.delete_subject, name="delete_subject"),

]