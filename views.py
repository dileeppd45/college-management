from django.shortcuts import render

from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

import os
# reg.text

def home_page(request):
	return render(request, 'index.html')

def login(request):
		if request.method == "POST":
			userid = request.POST['userid']
			password = request.POST['password']
			cursor = connection.cursor()
			cursor.execute("select * from login where admin_id= '" + userid + "' AND password = '" + password + "'")
			admin = cursor.fetchone()
			if admin == None:
				cursor.execute("select * from staff_details where staff_id ='" + str(userid) + "' and password ='" + str(password) + "' ")
				staff = cursor.fetchone()
				if staff == None:
					cursor.execute("select * from student where register_number= '" + userid + "' AND password = '" + password + "'")
					student = cursor.fetchone()
					if student == None:
						return HttpResponse("<script> alert('Invalid Username Or Password!!');window.location='../login';</script>")
					else:
						request.session['studid'] = userid
						return redirect('student_home')
				else:
					request.session['staffid'] = userid
					cursor.execute("select * from staff_details where staff_id ='" + str(userid) + "' and password ='" + str(password) + "' and staff_type ='teacher' ")
					teacher=cursor.fetchone()
					if teacher == None:
						cursor.execute("select * from staff_details where staff_id ='" + str(userid) + "' and password ='" + str(password) + "'and staff_type ='mentor' ")
						mentor=cursor.fetchone()
						if mentor == None:
							cursor.execute("select * from staff_details where staff_id ='" + str(userid) + "' and password ='" + str(password) + "'and staff_type ='manager' ")
							manager=cursor.fetchone()
							if manager == None:
								return HttpResponse("<script> alert('Invalid Username Or Password!!');window.location='../login';</script>")
							else:
								return redirect('manager_home')

						else:
							return redirect('mentor_home')

					else:
						return redirect('teacher_home')

			else:
				return redirect("admin_home")
		return render(request, "login.html")

def admin_home(request):
    return render(request, "admin_home.html")

def teacher_home(request):
	return render(request,"teacher_home.html")

def manager_home(request):
	return render(request,"manager_home.html")

def mentor_home(request):
	return render(request,'mentor_home.html')

def student_home(request):
	return render(request, "student_home.html")

def stud_view_cnotification(request):
	cursor = connection.cursor()
	cursor.execute("select * from college_notification  ")
	data=cursor.fetchall()
	data = reversed(data)
	return render(request,"student_view_cnotification.html",{'cdata':data})

def stud_view_department(request):
	cursor = connection.cursor()
	stud = request.session['studid']
	cursor.execute("select department_id from student where register_number= '"+str(stud)+"' ")
	depid=cursor.fetchone()
	depid=list(depid)
	depid=depid[0]
	cursor.execute("select * from department where iddepartment = '"+str(depid)+"' ")
	data=cursor.fetchone()
	return render(request,"student_view_department.html",{'cdata':data})


def stud_view_course(request, id):
	request.session['studdepid']=id
	stud = request.session['studid']
	cursor = connection.cursor()
	cursor.execute("select course_id from student where register_number= '" + str(stud) + "' ")
	depid = cursor.fetchone()
	depid = list(depid)
	courseid = depid[0]
	cursor.execute("select * from course where iddepartment='"+str(id)+"' and idcourse='"+str(courseid)+"' ")
	data=cursor.fetchone()
	return render(request,"student_view_course.html",{'cdata':data})

def stud_view_subject(request, id):
	did = request.session['studdepid']
	stud = request.session['studid']
	cursor = connection.cursor()
	cursor.execute("select semester from student where register_number= '" + str(stud) + "' ")
	sem = cursor.fetchone()
	sem = list(sem)
	sem = sem[0]
	cursor.execute("select * from subject where idcourse='"+str(id)+"' and iddepartment='"+str(did)+"' and semester='"+str(sem)+"' ")
	data=cursor.fetchall()
	return render(request,"stud_view_subject.html",{'cdata':data,'did':did})

def stud_view_notification(request, id):
	stud = request.session['studid']
	cursor = connection.cursor()
	cursor.execute("select semester from student where register_number= '" + str(stud) + "' ")
	sem = cursor.fetchone()
	sem = list(sem)
	sem = sem[0]
	did = request.session['studdepid']
	cursor.execute("select * from notification where course_id='"+str(id)+"' and depart_id='"+str(did)+"'  ")
	data=cursor.fetchall()
	print("fdsaf")
	print(data)
	data=reversed(data)
	print(data)
	return render(request,"stud_view_notification.html",{'cdata':data,'did':did})

def stud_view_timetable(request, id):
	stud = request.session['studid']
	cursor = connection.cursor()
	cursor.execute("select semester from student where register_number= '" + str(stud) + "' ")
	sem = cursor.fetchone()
	sem = list(sem)
	sem = sem[0]
	did = request.session['studdepid']
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='"+str(sem)+"' and time_table.day='monday' ")
	semmon=cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='"+str(sem)+"' and time_table.day='tuesday' ")
	semtue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='"+str(sem)+"' and time_table.day='wednesday' ")
	semwed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='"+str(sem)+"' and time_table.day='thursday' ")
	semthu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='"+str(sem)+"' and time_table.day='friday' ")
	semfri = cursor.fetchone()

	return render(request,"stud_view_timetable.html",{'semmon':semmon,'semtue':semtue,'semwed':semwed,'semthu':semthu,'semfri':semfri,'sem':sem,'did':did})




def stud_leave_status(request):
	cursor = connection.cursor()
	stud=request.session['studid']
	cursor.execute("select * from attendance where roll_no='"+str(stud)+"' ")
	attendence=cursor.fetchall()

	cursor.execute("select * from attendance where roll_no='" + str(stud) + "' and status='absent'")
	absent = cursor.fetchall()
	absent=list(absent)
	abs=int(0)
	for i in absent:
		abs=abs+1

	cursor.execute("select * from attendance where roll_no='" + str(stud) + "' and status='half'")
	half = cursor.fetchall()
	half=list(half)
	hal=int(0)
	for i in half:
		hal=hal+1

	total_absents=abs+(hal/2)
	return render(request,'student_leave_status.html',{'attendence':attendence,'total':total_absents})

def send_feedback(request):
	return render(request,"student_send_feedback.html")


def sendfb(request):
    cursor = connection.cursor()
    if request.method == "POST":
        fbdetails = request.POST['fbdetails']
        stud = request.session['studid']
        cursor.execute("insert into feedback values( null,'" + str(stud) + "', '" + str(fbdetails) + "',curdate() )")
        messages.info(request, "done")
        return redirect("view_fb")

def view_fb(request):
	stud = request.session['studid']
	cursor = connection.cursor()
	cursor.execute("select * from feedback where roll_no='" + stud + "' ")
	feeds=cursor.fetchall()
	return render(request, "student_view_fb.html",{'feeds':feeds})

def apply_leaves(request):
	cursor = connection.cursor()
	cursor.execute("select * from staff_details where staff_type='mentor' ")
	mentors = cursor.fetchall()
	return render(request, "student_apply_leave.html",{'mentors':mentors})
def sendleave(request):
	cursor = connection.cursor()
	if request.method == "POST":
		count=request.POST['count']
		mentor=request.POST['ment']
		date = request.POST['start_date']
		reason = request.POST['reason']
		stud = request.session['studid']
		cursor.execute("insert into leaves values(null, '" + str(stud) + "', '" + str(date) + "','" + str(count) + "','" + str(mentor) + "','pending','"+str(reason)+"' )")
		return redirect('view_leaves')

def view_leaves(request):
	stud = request.session['studid']
	cursor = connection.cursor()
	cursor.execute("select * from leaves where roll_no='" + stud + "' ")
	leaves = cursor.fetchall()
	return render(request, "student_view_leaves.html", {'leaves': leaves})

def mentor_view_leaves(request):
	mentor = request.session['staffid']
	cursor = connection.cursor()
	cursor.execute("select * from leaves where staff_id='" + mentor + "' and status ='pending' ")
	leaves = cursor.fetchall()
	cursor.execute("select * from leaves where staff_id='" + mentor + "' and status ='approved' ")
	aleaves = cursor.fetchall()
	cursor.execute("select * from leaves where staff_id='" + mentor + "' and status ='rejected' ")
	rleaves = cursor.fetchall()
	return render(request, "mentor_view_leaves.html", {'leaves': leaves,'aleaves':aleaves,'rleaves':rleaves})

def approve_pending_leave(request,id):
	cursor =connection.cursor()
	cursor.execute("update leaves set status = 'approved' where idleave ='"+str(id)+"' ")
	return redirect('mentor_view_leaves')
def reject_pending_leave(request,id):
	cursor =connection.cursor()
	cursor.execute("update leaves set status = 'rejected' where idleave ='"+str(id)+"' ")
	return redirect('mentor_view_leaves')



def reg_dep(request):
	return render(request, "admin_reg_dep.html")

def add_dep(request):
	if request.method == "POST":
		name = request.POST['name']
		cursor = connection.cursor()
		cursor.execute("insert into department values(null,'" + name + "')")
		return redirect("view_dapartment")

def view_department(request):
	cursor = connection.cursor()
	cursor.execute("select * from department")
	data=cursor.fetchall()
	return render(request,"admin_view_department.html",{'cdata':data})

def reg_course(request, id):
	return render(request, "admin_reg_course.html",{'id':id})

def add_course(request,id):
	if request.method == "POST":
		name = request.POST['name']
		cursor = connection.cursor()
		cursor.execute("insert into course values(null,'" + str(id) + "','"+str(name)+"') ")
		return redirect("view_course", id=int(id))

def view_course(request, id):
	request.session['depid']=id
	cursor = connection.cursor()
	cursor.execute("select * from course where iddepartment='"+str(id)+"'")
	data=cursor.fetchall()
	return render(request,"admin_view_course.html",{'cdata':data})

def reg_subject(request, id):
	return render(request, "admin_reg_sub.html",{'id':id})

def add_subject(request,id):
	if request.method == "POST":
		did=request.session['depid']
		name = request.POST['name']
		semester=request.POST['semester']
		cursor = connection.cursor()
		cursor.execute("insert into subject values(null,'"+str(did)+"','"+str(semester)+"','"+str(name)+"','"+str(id)+"') ")
		return redirect("admin_view_semester",id=int(id))

def view_subject(request, id):
	did = request.session['depid']
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='"+str(id)+"' and iddepartment='"+str(did)+"' ")
	data=cursor.fetchall()
	return render(request,"admin_view_subject.html",{'cdata':data})

def upload_notification(request, id):
	return render(request, "admin_upload_notification.html", {'id':id})

def add_notification(request,id):
	if request.method == "POST" and request.FILES['pdf_file']:
		did = request.session['depid']
		details = request.POST['details']
		upload = request.FILES['pdf_file']
		cart = FileSystemStorage(location='../studpro/media/unotification')
		file = cart.save(upload.name, upload)
		file_url = cart.url(file)
		semester=request.POST['txtsemester']
		cursor = connection.cursor()
		cursor.execute("insert into notification values(null,'"+str(semester)+"','"+str(details)+"',curdate(),'" + str(id) + "','"+str(upload)+"','"+str(did)+"'  ) ")
		return redirect("view_notification", id=int(id))

def view_notification(request, id):
	cursor = connection.cursor()
	did = request.session['depid']
	cursor.execute("select * from notification where course_id='"+str(id)+"' and depart_id='"+str(did)+"'  ")
	data=cursor.fetchall()
	data=reversed(data)
	return render(request,"admin_view_notification.html",{'cdata':data})

def reg_timetable(request, id,sem):
	did = request.session['depid']
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and iddepartment='" + str(did) + "' and semester ='"+str(sem)+"'  ")
	adata = cursor.fetchall()
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and iddepartment='" + str(did) + "' and semester ='"+str(sem)+"'   ")
	bdata = cursor.fetchall()
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and iddepartment='" + str(did) + "' and semester ='"+str(sem)+"'   ")
	cdata = cursor.fetchall()
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and iddepartment='" + str(did) + "' and semester ='"+str(sem)+"'   ")
	ddata = cursor.fetchall()
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and iddepartment='" + str(did) + "' and semester ='"+str(sem)+"'   ")
	edata = cursor.fetchall()
	return render(request, "admin_upload_timetable.html", {'id': id, 'adata':adata, 'bdata':bdata, 'cdata':cdata, 'ddata':ddata, 'edata':edata,'sem':sem})

def add_timetable(request, id):
	if request.method == "POST":
		semester = request.POST['semester']
		day = request.POST['day']
		p1 = request.POST['period1']
		p2 = request.POST['period2']
		p3 = request.POST['period3']
		p4 = request.POST['period4']
		p5 = request.POST['period5']
		cursor = connection.cursor()
		cursor.execute("select idtime_table from time_table where semester='"+str(semester)+"' and  course_id='"+str(id)+"' and day='"+str(day)+"' ")
		data=cursor.fetchone()
		if data == None:
			cursor.execute("insert into time_table values(null,'"+str(semester)+"','"+str(id)+"','"+str(p1)+"','"+str(p2)+"','"+str(p3)+"','"+str(p4)+"','"+str(p5)+"','"+str(day)+"') ")
			return redirect("view_timetable",id=int(id))
		else:
			data=list(data)
			data=data[0]
			cursor.execute("update time_table set period1='" + str(p1) + "' where idtime_table= '" + str(data) + "' ")
			cursor.execute("update time_table set period2='" + str(p2) + "' where idtime_table= '" + str(data) + "' ")
			cursor.execute("update time_table set period3='" + str(p3) + "' where idtime_table= '" + str(data) + "' ")
			cursor.execute("update time_table set period4='" + str(p4) + "' where idtime_table= '" + str(data) + "' ")
			cursor.execute("update time_table set period5='" + str(p5) + "' where idtime_table= '" + str(data) + "' ")
			return redirect("view_timetable", id=int(id))

def admin_view_semester(request, id):
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='1' ")
	sem1 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='1' ")
	stud1 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='2' ")
	sem2 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='2' ")
	stud2 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='3' ")
	sem3 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='3' ")
	stud3 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='4' ")
	sem4 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='4' ")
	stud4 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='5' ")
	sem5 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='5' ")
	stud5 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='6' ")
	sem6 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='6' ")
	stud6 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='7' ")
	sem7 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='7' ")
	stud7 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='8' ")
	sem8 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='8' ")
	stud8 = cursor.fetchall()
	return render(request, 'admin_view_semester.html',{'sem1': sem1, 'stud1': stud1, 'sem2': sem2, 'stud2': stud2, 'sem3': sem3, 'stud3': stud3,'sem4': sem4, 'stud4': stud4, 'sem5': sem5, 'stud5': stud5, 'sem6': sem6, 'stud6': stud6,'sem7': sem7, 'stud7': stud7, 'sem8': sem8, 'stud8': stud8})

def view_timetable(request, id):
	cursor = connection.cursor()
	# did = request.session['sdepid']
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='1' and time_table.day='monday' ")
	sem1mon = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='1' and time_table.day='tuesday' ")
	sem1tue = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='1' and time_table.day='wednesday' ")
	sem1wed = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='1' and time_table.day='thursday' ")
	sem1thu = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='1' and time_table.day='friday' ")
	sem1fri = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='2' and time_table.day='monday'  ")
	sem2mon = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='2' and time_table.day='tuesday'  ")
	sem2tue = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='2' and time_table.day='wednesday'  ")
	sem2wed = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='2' and time_table.day='thursday'  ")
	sem2thu = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='2' and time_table.day='friday'  ")
	sem2fri = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='3' and time_table.day='monday'  ")
	sem3mon = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='3' and time_table.day='tuesday'  ")
	sem3tue = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='3' and time_table.day='wednesday'  ")
	sem3wed = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='3' and time_table.day='thursday'  ")
	sem3thu = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='3' and time_table.day='friday'  ")
	sem3fri = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='4' and time_table.day='monday'  ")
	sem4mon = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='4' and time_table.day='tuesday'  ")
	sem4tue = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='4' and time_table.day='wednesday'  ")
	sem4wed = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='4' and time_table.day='thursday'  ")
	sem4thu = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='4' and time_table.day='friday'  ")
	sem4fri = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='5' and time_table.day='monday'  ")
	sem5mon = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='5' and time_table.day='tuesday'  ")
	sem5tue = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='5' and time_table.day='wednesday'  ")
	sem5wed = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='5' and time_table.day='thursday'  ")
	sem5thu = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='5' and time_table.day='friday'  ")
	sem5fri = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='6' and time_table.day='monday'  ")
	sem6mon = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='6' and time_table.day='tuesday'  ")
	sem6tue = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='6' and time_table.day='wednesday'  ")
	sem6wed = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='6' and time_table.day='thursday'  ")
	sem6thu = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='6' and time_table.day='friday'  ")
	sem6fri = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='7' and time_table.day='monday'  ")
	sem7mon = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='7' and time_table.day='tuesday'  ")
	sem7tue = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='7' and time_table.day='wednesday'  ")
	sem7wed = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='7' and time_table.day='thursday'  ")
	sem7thu = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='7' and time_table.day='friday'  ")
	sem7fri = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='8' and time_table.day='monday' ")
	sem8mon = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='8' and time_table.day='tuesday' ")
	sem8tue = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='8' and time_table.day='wednesday' ")
	sem8wed = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='8' and time_table.day='thursday' ")
	sem8thu = cursor.fetchone()
	cursor.execute(
		"select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(
			id) + "' and time_table.semester='8' and time_table.day='friday' ")
	sem8fri = cursor.fetchone()
	return render(request,"admin_view_time_table.html",{'sem11':sem1mon,'sem12':sem1tue,'sem13':sem1wed,'sem14':sem1thu,'sem15':sem1fri,'sem21':sem2mon,'sem22':sem2tue,'sem23':sem2wed,'sem24':sem2thu,'sem25':sem2fri,'sem31':sem3mon,'sem32':sem3tue,'sem33':sem3wed,'sem34':sem3thu,'sem35':sem3fri,'sem41':sem4mon,'sem42':sem4tue,'sem43':sem4wed,'sem44':sem4thu,'sem45':sem4fri,'sem51':sem5mon,'sem52':sem5tue,'sem53':sem5wed,'sem54':sem5thu,'sem55':sem5fri,'sem61':sem6mon,'sem62':sem6tue,'sem63':sem6wed,'sem64':sem6thu,'sem65':sem6fri,'sem71':sem7mon,'sem72':sem7tue,'sem73':sem7wed,'sem74':sem7thu,'sem75':sem7fri,'sem81':sem8mon,'sem82':sem8tue,'sem83':sem8wed,'sem84':sem8thu,'sem85':sem8fri,'cid':id})

def upload_cnotification(request):
	return render(request, "admin_upload_cnotification.html", {'id':id})

def add_cnotification(request):
	if request.method == "POST":
		details = request.POST['details']
		cursor = connection.cursor()
		cursor.execute("insert into college_notification values(null,'"+str(details)+"',curdate() ) ")
		return redirect("view_cnotification")

def view_cnotification(request):
	cursor = connection.cursor()
	cursor.execute("select * from college_notification  ")
	data=cursor.fetchall()
	data = reversed(data)
	return render(request,"admin_view_cnotification.html",{'cdata':data})

def add_staff(request):
	return render(request,'admin_staffreg.html')
def staff_register(request):
	if request.method == "POST":
		stid = request.POST['txtstaffid']
		name = request.POST['txtname']
		address = request.POST['txtaddress']
		phnum = request.POST['txtphnum']
		email = request.POST['txtemail']
		dept = request.POST['txtdepartment']
		type = request.POST['txttype']
		semester=request.POST['txtsemester']
		qualification = request.POST['txtqualification']
		password=request.POST['txtpassword']
		cursor = connection.cursor()
		cursor.execute("insert into staff_details values('" + stid + "','" + name + "','" + address + "','" + phnum + "','" + email + "','" + type + "','" + dept + "','" + qualification + "','" + password + "','" + semester + "')")
	return redirect('admin_home')

def view_staffreg_(request):
	cursor = connection.cursor()
	cursor.execute("select * from staff_details")
	data = cursor.fetchall()
	return render(request, "admin_viewstaffreg.html", {'data': data})


def staff_view_cnotification(request):
	cursor = connection.cursor()
	cursor.execute("select * from college_notification  ")
	data=cursor.fetchall()
	data = reversed(data)
	return render(request,"teacher_view_cnotification.html",{'cdata':data})

def mentor_view_cnotification(request):
	cursor = connection.cursor()
	cursor.execute("select * from college_notification  ")
	data=cursor.fetchall()
	data = reversed(data)
	return render(request,"mentor_view_cnotification.html",{'cdata':data})

def staff_view_department(request):
	cursor = connection.cursor()
	cursor.execute("select * from department")
	data = cursor.fetchall()
	return render(request,'teacher_view_department.html',{'cdata':data})

def mentor_view_department(request):
	cursor = connection.cursor()
	cursor.execute("select * from department")
	data = cursor.fetchall()
	return render(request,'mentor_view_department.html',{'cdata':data})

def manager_view_department(request):
	cursor = connection.cursor()
	cursor.execute("select * from department")
	data = cursor.fetchall()
	return render(request,'manager_view_department.html',{'cdata':data})

def staff_view_course(request, id):
	request.session['sdepid']=id
	cursor = connection.cursor()
	cursor.execute("select * from course where iddepartment='"+str(id)+"' ")
	data = cursor.fetchall()
	return render(request, 'teacher_view_course.html',{'cdata':data})

def mentor_view_course(request, id):
	request.session['mentordepid']=id
	cursor = connection.cursor()
	cursor.execute("select * from course where iddepartment='"+str(id)+"' ")
	data = cursor.fetchall()
	return render(request, 'mentor_view_course.html',{'cdata':data})

def manager_view_course(request, id):
	request.session['managerdepid']=id
	cursor = connection.cursor()
	cursor.execute("select * from course where iddepartment='"+str(id)+"' ")
	data = cursor.fetchall()
	return render(request, 'manager_view_course.html',{'cdata':data})

def staff_view_semester(request, id):
	did = request.session['sdepid']
	request.session['scid'] = id
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='"+str(id)+"' and semester ='1' ")
	sem1 = cursor.fetchall()
	cursor.execute("select * from student where course_id='"+str(id)+"' and semester ='1' ")
	stud1 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='2' ")
	sem2 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='2' ")
	stud2 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='3' ")
	sem3 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='3' ")
	stud3 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='4' ")
	sem4 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='4' ")
	stud4 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='5' ")
	sem5 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='5' ")
	stud5 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='6' ")
	sem6 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='6' ")
	stud6 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='7' ")
	sem7 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='7' ")
	stud7 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='8' ")
	sem8 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='8' ")
	stud8 = cursor.fetchall()
	return render(request, 'teacher_view_semester.html', {'sem1': sem1,'stud1': stud1,'sem2': sem2,'stud2': stud2,'sem3': sem3,'stud3': stud3,'sem4': sem4,'stud4': stud4,'sem5': sem5,'stud5': stud5,'sem6': sem6,'stud6': stud6,'sem7': sem7,'stud7': stud7,'sem8': sem8,'stud8': stud8,'did':did})
def mentor_view_semester(request, id):
	did = request.session['mentordepid']
	request.session['mentorcourid'] = id
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='"+str(id)+"' and semester ='1' ")
	sem1 = cursor.fetchall()
	cursor.execute("select * from student where course_id='"+str(id)+"' and semester ='1' ")
	stud1 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='2' ")
	sem2 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='2' ")
	stud2 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='3' ")
	sem3 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='3' ")
	stud3 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='4' ")
	sem4 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='4' ")
	stud4 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='5' ")
	sem5 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='5' ")
	stud5 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='6' ")
	sem6 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='6' ")
	stud6 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='7' ")
	sem7 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='7' ")
	stud7 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='8' ")
	sem8 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='8' ")
	stud8 = cursor.fetchall()
	return render(request, 'mentor_view_semester.html', {'sem1': sem1,'stud1': stud1,'sem2': sem2,'stud2': stud2,'sem3': sem3,'stud3': stud3,'sem4': sem4,'stud4': stud4,'sem5': sem5,'stud5': stud5,'sem6': sem6,'stud6': stud6,'sem7': sem7,'stud7': stud7,'sem8': sem8,'stud8': stud8,'did':did})

def manager_view_semester(request, id):
	did = request.session['managerdepid']
	request.session['managercourid'] = id
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='"+str(id)+"' and semester ='1' ")
	sem1 = cursor.fetchall()
	cursor.execute("select * from student where course_id='"+str(id)+"' and semester ='1' ")
	stud1 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='2' ")
	sem2 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='2' ")
	stud2 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='3' ")
	sem3 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='3' ")
	stud3 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='4' ")
	sem4 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='4' ")
	stud4 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='5' ")
	sem5 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='5' ")
	stud5 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='6' ")
	sem6 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='6' ")
	stud6 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='7' ")
	sem7 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='7' ")
	stud7 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='8' ")
	sem8 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='8' ")
	stud8 = cursor.fetchall()
	return render(request, 'manager_view_semester.html', {'sem1': sem1,'stud1': stud1,'sem2': sem2,'stud2': stud2,'sem3': sem3,'stud3': stud3,'sem4': sem4,'stud4': stud4,'sem5': sem5,'stud5': stud5,'sem6': sem6,'stud6': stud6,'sem7': sem7,'stud7': stud7,'sem8': sem8,'stud8': stud8,'did':did})



def teacher_view_feedback(request):
	cursor = connection.cursor()
	cursor.execute("select feedback.*, student.name from feedback join student where feedback.roll_no = student.register_number")
	data = cursor.fetchall()
	return render(request,'teacher_view_feedback.html',{'data':data})

def internals(request,id):
	did = request.session['sdepid']
	request.session['scourseidinternals'] = id
	cursor = connection.cursor()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='1' ")
	sem1 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='1' ")
	stud1 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='2' ")
	sem2 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='2' ")
	stud2 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='3' ")
	sem3 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='3' ")
	stud3 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='4' ")
	sem4 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='4' ")
	stud4 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='5' ")
	sem5 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='5' ")
	stud5 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='6' ")
	sem6 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='6' ")
	stud6 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='7' ")
	sem7 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='7' ")
	stud7 = cursor.fetchall()
	cursor.execute("select * from subject where idcourse='" + str(id) + "' and semester ='8' ")
	sem8 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='8' ")
	stud8 = cursor.fetchall()
	return render(request, 'teacher_internal.html',{'id':id,'sem1': sem1, 'stud1': stud1, 'sem2': sem2, 'stud2': stud2, 'sem3': sem3, 'stud3': stud3,'sem4': sem4, 'stud4': stud4, 'sem5': sem5, 'stud5': stud5, 'sem6': sem6, 'stud6': stud6,'sem7': sem7, 'stud7': stud7, 'sem8': sem8, 'stud8': stud8, 'did': did})

def attendence(request,id):
	cursor = connection.cursor()
	did = request.session['sdepid']
	request.session['scourseidattendence'] = id
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='1' ")
	stud1 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='2' ")
	stud2 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='3' ")
	stud3 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='4' ")
	stud4 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='5' ")
	stud5 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='6' ")
	stud6 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='7' ")
	stud7 = cursor.fetchall()
	cursor.execute("select * from student where course_id='" + str(id) + "' and semester ='8' ")
	stud8 = cursor.fetchall()
	return render(request, 'teacher_attendance.html',{'id':id,'stud1': stud1,'stud2': stud2,'stud3': stud3,'stud4': stud4,'stud5': stud5,'stud6': stud6,'stud7': stud7,'stud8': stud8,'did':did})


def make_internal(request):
	if request.method == "POST":
		reg_no = request.POST['roll_no']
		semester = request.POST['cur_semester']
		mark = request.POST['mark']
		subid = request.POST['txtsemester']
		user = request.session['staffid']
		id = request.POST['id']
		cursor = connection.cursor()
		cursor.execute("select * from internal_mark where roll_no ='"+str(reg_no)+"' and semester='"+str(semester)+"' and idsubject='"+str(subid)+"' ")
		state = cursor.fetchone()
		if state == None:
			cursor.execute("insert into internal_mark values(null,'"+str(reg_no)+"','"+str(subid)+"','"+str(semester)+"','"+str(mark)+"','"+str(user)+"')")
		else:
			cursor.execute("delete from internal_mark where roll_no ='"+str(reg_no)+"' and semester='"+str(semester)+"' and idsubject='"+str(subid)+"' ")
			cursor.execute("insert into internal_mark values(null,'" + str(reg_no) + "','" + str(subid) + "','" + str(semester) + "','" + str(mark) + "','" + str(user) + "')")
		return redirect('internals', id=int(id))

def make_attendence(request):
	if request.method == "POST":
		reg_no = request.POST['roll_no']
		semester = request.POST['cur_semester']
		status= request.POST['optradio']
		user=request.session['staffid']
		id= request.POST['id']
		cursor = connection.cursor()
		cursor.execute("select * from attendance where roll_no ='"+str(reg_no)+"' and absent_date =curdate() and current_semester ='"+str(semester)+"' " )
		state = cursor.fetchone()
		if state ==None:
			if status =='absent':

				cursor.execute("insert into attendance values(null,'" + reg_no + "',curdate(),'" + user + "','" + str(semester) + "','absent')")
				return redirect('attendence',id=int(id))
			else:
				cursor.execute("insert into attendance values(null,'" + reg_no + "',curdate(),'" + user + "','" + str(semester) + "','late')")
				return redirect('attendence', id=int(id))
		else:
			cursor.execute("select * from attendance where roll_no ='" + str(reg_no) + "' and absent_date =curdate() and current_semester ='" + str(semester) + "'and status ='absent' ")
			state1 = cursor.fetchone()
			if state1 ==None:
				if status =='late':
					cursor.execute("select * from attendance where roll_no='" + str(reg_no) + "' and absent_date=curdate() and status='late' and current_semester ='" + str(semester) + "' ")
					check = cursor.fetchall()
					check = list(check)
					count = int(0)
					for i in check:
						count = count + 1
					if (count < 2):
						cursor.execute("insert into attendance values(null,'" + reg_no + "',curdate(),'" + user + "','" + str(semester) + "','late')")
						return redirect('attendence', id=int(id))
					else:
						cursor.execute("insert into attendance values(null,'" + reg_no + "',curdate(),'" + user + "','" + str(semester) + "','absent')")
						cursor.execute("delete from attendance where roll_no ='"+str(reg_no)+"' and absent_date = curdate() and current_semester='"+str(semester)+"' and status ='late' ")
						return redirect('attendence', id=int(id))
				else:
					cursor.execute("insert into attendance values(null,'" + reg_no + "',curdate(),'" + user + "','" + str(semester) + "','absent')")
					cursor.execute("delete from attendance where roll_no ='" + str(reg_no) + "' and absent_date = curdate() and current_semester='" + str(semester) + "' and status ='late' ")
					return redirect('attendence', id=int(id))


			else:
				if status == 'late':
					cursor.execute("update attendance set status ='late' where roll_no ='"+str(reg_no)+"' and absent_date = curdate() and current_semester ='"+str(semester)+"' ")
				return redirect('attendence', id=int(id))

def view_internal(request,id):
	request.session['studentinternalid'] = id
	cursor = connection.cursor()
	cid =request.session['scourseidinternals']
	cursor.execute("select register_number,semester from student where student_id='" + str(id) + "' ")
	data = cursor.fetchone()
	data = list(data)
	semester = data[1]
	print(data)
	data = data[0]
	cursor.execute("select internal_mark.*,subject.subject_name from internal_mark join subject where internal_mark.roll_no='" + str(data) + "' and internal_mark.semester = '" + str(semester) + "' and internal_mark.idsubject = subject.idsubject ")
	attendence = cursor.fetchall()
	return render(request,'teacher_view_internal.html',{'attendence':attendence,'cid':cid})

def stud_view_internals(request,id):
	stud = request.session['studid']
	cursor = connection.cursor()
	cursor.execute("select semester from student where register_number= '" + str(stud) + "' ")
	sem = cursor.fetchone()
	sem = list(sem)
	sem = sem[0]
	did = request.session['studdepid']
	cursor.execute("select internal_mark.*,subject.subject_name from internal_mark join subject where internal_mark.roll_no='" + str(stud) + "' and internal_mark.semester = '" + str(sem) + "' and internal_mark.idsubject = subject.idsubject ")
	data = cursor.fetchall()
	return render(request,'stud_view_internal.html',{'data':data,'did':did})

def stud_view_attendance(request,id):
	stud = request.session['studid']
	cursor = connection.cursor()
	cursor.execute("select semester from student where register_number= '" + str(stud) + "' ")
	sem = cursor.fetchone()
	sem = list(sem)
	sem = sem[0]
	did = request.session['studdepid']
	cursor.execute("select * from attendance where roll_no='" + str(stud) + "' and current_semester = '" + str(sem) + "' ")
	attendence = cursor.fetchall()
	print(attendence)
	cursor.execute("select * from attendance where roll_no='" + str(stud) + "' and status='absent' and current_semester='" + str(sem) + "' ")
	absent = cursor.fetchall()
	absent = list(absent)
	abs = int(0)
	for i in absent:
		abs = abs + 1

	total_absents = abs
	return render(request,'stud_view_attendence.html',{'attendence':attendence,'total':total_absents,'did':did})

def mentor_view_attendance(request,id):
	cid = request.session['mentorcourid']
	cursor = connection.cursor()
	cursor.execute("select semester from student where register_number='" + str(id) + "' ")
	data = cursor.fetchone()
	data = list(data)
	semester = data[0]
	cursor.execute("select * from attendance where roll_no='" + str(id) + "' and current_semester = '" + str(semester) + "' ")
	attendence = cursor.fetchall()
	print(attendence)
	cursor.execute("select * from attendance where roll_no='" + str(id) + "' and status='absent' and current_semester='" + str(semester) + "' ")
	absent = cursor.fetchall()
	absent = list(absent)
	abs = int(0)
	for i in absent:
		abs = abs + 1

	total_absents = abs
	return render(request,'mentor_view_attendence.html',{'attendence':attendence,'total':total_absents,'cid':cid})

def manager_view_attendance(request,id):
	cid = request.session['managercourid']
	cursor = connection.cursor()
	cursor.execute("select semester from student where register_number='" + str(id) + "' ")
	data = cursor.fetchone()
	data = list(data)
	semester = data[0]
	cursor.execute("select * from attendance where roll_no='" + str(id) + "' and current_semester = '" + str(semester) + "' ")
	attendence = cursor.fetchall()
	print(attendence)
	cursor.execute("select * from attendance where roll_no='" + str(id) + "' and status='absent' and current_semester='" + str(semester) + "' ")
	absent = cursor.fetchall()
	absent = list(absent)
	abs = int(0)
	for i in absent:
		abs = abs + 1

	total_absents = abs
	return render(request,'manager_view_attendence.html',{'attendence':attendence,'total':total_absents,'cid':cid})


def view_attendence(request, id):
	request.session['studattendid'] = id
	cursor = connection.cursor()
	cid = request.session['scourseidattendence']
	cursor.execute("select register_number,semester from student where student_id='"+str(id)+"' ")
	data=cursor.fetchone()
	data=list(data)
	semester = data[1]
	print(data)
	data=data[0]

	print(data)
	print('semester')
	print(semester)
	cursor.execute("select * from attendance where roll_no='"+str(data)+"' and current_semester = '"+str(semester)+"' ")
	attendence = cursor.fetchall()
	print(attendence)
	cursor.execute("select * from attendance where roll_no='" + str(data) + "' and status='absent' and current_semester='"+str(semester)+"' ")
	absent = cursor.fetchall()
	absent=list(absent)
	abs=int(0)
	for i in absent:
		abs=abs+1

	total_absents=abs
	return render(request,'teacher_view_attendence.html',{'attendence':attendence,'total':total_absents,'cid':cid})

def remove_internal(request,id):
	studid = request.session['studentinternalid']
	cursor = connection.cursor()
	cursor.execute("delete from internal_mark where idinternal_mark = '" + str(id) + "' ")
	return redirect('view_internal', id=int(studid))

def remove_attendence(request,id):
	studid = request.session['studattendid']
	cursor = connection.cursor()
	cursor.execute("delete from attendance where idattendance = '"+str(id)+"' ")
	return redirect('view_attendence', id=int(studid))

def staff_view_notification(request, id):
	cursor = connection.cursor()
	did = request.session['sdepid']
	cursor.execute("select * from notification where course_id='"+str(id)+"' ")
	data=cursor.fetchall()
	data=reversed(data)
	return render(request,"teacher_view_notification.html",{'cdata':data,'did':did})

def manager_add_fees(request,id):
	did = request.session['managerdepid']
	return render(request, "manager_add_fees.html", {'cid': id, 'did': did})

def add_fees_type(request,id):
	if request.method == "POST":
		cid = id
		mentor = request.session['staffid']
		fee_type = request.POST['name']
		amount= request.POST['amount']
		user =request.session['staffid']
		cursor = connection.cursor()
		cursor.execute("insert into fees values(null ,'"+str(fee_type)+"','"+str(cid)+"', '"+str(amount)+"','"+str(mentor)+"','active')")
		return redirect('manager_add_fees',id=id)

def manager_view_fees(request,id):
	cursor = connection.cursor()
	did = request.session['managerdepid']
	cursor.execute("select * from fees where courseid ='"+str(id)+"' and status ='active' ")
	data=cursor.fetchall()
	return render(request,'manager_view_fees.html',{'data':data,'did':did})

def stud_view_fees(request,id):
	cursor = connection.cursor()
	did = request.session['studdepid']
	stud = request.session['studid']
	cursor.execute("select fees_payment.*,fees.fees_type, fees.courseid,fees.amount from  fees_payment join fees where fees.idfees = fees_payment.fees_type and fees_payment.roll_no ='"+str(stud)+"' ")
	data = cursor.fetchall()
	return render(request,'stud_view_fees.html',{'data':data,'did':did})

def stud_add_fees(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from fees where courseid ='"+str(id)+"' and status ='active' ")
	data = cursor.fetchall()
	did = request.session['studdepid']
	return render(request,'stud_make_fees.html',{'data':data,'cid':id,'did':did})

def proceed_payment_details(request,id):
	cursor = connection.cursor()
	if request.method == "POST":
		fees_des = request.POST['desc']
		sem = request.POST['semester']
		image= request.FILES['image']
		stud = request.session['studid']
		fee_type = request.POST['type']
		upload = request.FILES['image']
		fss = FileSystemStorage()
		file = fss.save( upload.name, upload)
		file_url = fss.url(file)
		cursor.execute("insert into fees_payment values(null,'"+stud+"','"+str(sem)+"', '"+str(fees_des)+"', curdate(),'"+str(image)+"','"+str(fee_type)+"' ,'pending')")
		return redirect('stud_view_fees', id=id)




def mentor_view_notification(request, id):
	cursor = connection.cursor()
	did = request.session['mentordepid']
	cursor.execute("select * from notification where course_id='"+str(id)+"' ")
	data=cursor.fetchall()
	data=reversed(data)
	return render(request,"mentor_view_notification.html",{'cdata':data,'did':did})

def manager_view_notification(request, id):
	cursor = connection.cursor()
	did = request.session['managerdepid']
	cursor.execute("select * from notification where course_id='"+str(id)+"' ")
	data=cursor.fetchall()
	data=reversed(data)
	return render(request,"manager_view_notification.html",{'cdata':data,'did':did})

def staff_view_timetable(request, id):
	cursor = connection.cursor()
	did = request.session['sdepid']
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='monday' ")
	sem1mon=cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='tuesday' ")
	sem1tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='wednesday' ")
	sem1wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='thursday' ")
	sem1thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='friday' ")
	sem1fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='monday'  ")
	sem2mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='tuesday'  ")
	sem2tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='wednesday'  ")
	sem2wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='thursday'  ")
	sem2thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='friday'  ")
	sem2fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='monday'  ")
	sem3mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='tuesday'  ")
	sem3tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='wednesday'  ")
	sem3wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='thursday'  ")
	sem3thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='friday'  ")
	sem3fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='monday'  ")
	sem4mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='tuesday'  ")
	sem4tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='wednesday'  ")
	sem4wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='thursday'  ")
	sem4thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='friday'  ")
	sem4fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='monday'  ")
	sem5mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='tuesday'  ")
	sem5tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='wednesday'  ")
	sem5wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='thursday'  ")
	sem5thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='friday'  ")
	sem5fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='monday'  ")
	sem6mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='tuesday'  ")
	sem6tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='wednesday'  ")
	sem6wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='thursday'  ")
	sem6thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='friday'  ")
	sem6fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='monday'  ")
	sem7mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='tuesday'  ")
	sem7tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='wednesday'  ")
	sem7wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='thursday'  ")
	sem7thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='friday'  ")
	sem7fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='monday' ")
	sem8mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='tuesday' ")
	sem8tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='wednesday' ")
	sem8wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='thursday' ")
	sem8thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='friday' ")
	sem8fri = cursor.fetchone()
	return render(request,"teacher_view_time_table.html",{'sem11':sem1mon,'sem12':sem1tue,'sem13':sem1wed,'sem14':sem1thu,'sem15':sem1fri,'sem21':sem2mon,'sem22':sem2tue,'sem23':sem2wed,'sem24':sem2thu,'sem25':sem2fri,'sem31':sem3mon,'sem32':sem3tue,'sem33':sem3wed,'sem34':sem3thu,'sem35':sem3fri,'sem41':sem4mon,'sem42':sem4tue,'sem43':sem4wed,'sem44':sem4thu,'sem45':sem4fri,'sem51':sem5mon,'sem52':sem5tue,'sem53':sem5wed,'sem54':sem5thu,'sem55':sem5fri,'sem61':sem6mon,'sem62':sem6tue,'sem63':sem6wed,'sem64':sem6thu,'sem65':sem6fri,'sem71':sem7mon,'sem72':sem7tue,'sem73':sem7wed,'sem74':sem7thu,'sem75':sem7fri,'sem81':sem8mon,'sem82':sem8tue,'sem83':sem8wed,'sem84':sem8thu,'sem85':sem8fri,'did':did})


def manager_view_timetable(request, id):
	cursor = connection.cursor()
	did = request.session['managerdepid']
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='monday' ")
	sem1mon=cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='tuesday' ")
	sem1tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='wednesday' ")
	sem1wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='thursday' ")
	sem1thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='friday' ")
	sem1fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='monday'  ")
	sem2mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='tuesday'  ")
	sem2tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='wednesday'  ")
	sem2wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='thursday'  ")
	sem2thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='friday'  ")
	sem2fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='monday'  ")
	sem3mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='tuesday'  ")
	sem3tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='wednesday'  ")
	sem3wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='thursday'  ")
	sem3thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='friday'  ")
	sem3fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='monday'  ")
	sem4mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='tuesday'  ")
	sem4tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='wednesday'  ")
	sem4wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='thursday'  ")
	sem4thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='friday'  ")
	sem4fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='monday'  ")
	sem5mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='tuesday'  ")
	sem5tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='wednesday'  ")
	sem5wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='thursday'  ")
	sem5thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='friday'  ")
	sem5fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='monday'  ")
	sem6mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='tuesday'  ")
	sem6tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='wednesday'  ")
	sem6wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='thursday'  ")
	sem6thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='friday'  ")
	sem6fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='monday'  ")
	sem7mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='tuesday'  ")
	sem7tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='wednesday'  ")
	sem7wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='thursday'  ")
	sem7thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='friday'  ")
	sem7fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='monday' ")
	sem8mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='tuesday' ")
	sem8tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='wednesday' ")
	sem8wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='thursday' ")
	sem8thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='friday' ")
	sem8fri = cursor.fetchone()
	return render(request,"manager_view_time_table.html",{'sem11':sem1mon,'sem12':sem1tue,'sem13':sem1wed,'sem14':sem1thu,'sem15':sem1fri,'sem21':sem2mon,'sem22':sem2tue,'sem23':sem2wed,'sem24':sem2thu,'sem25':sem2fri,'sem31':sem3mon,'sem32':sem3tue,'sem33':sem3wed,'sem34':sem3thu,'sem35':sem3fri,'sem41':sem4mon,'sem42':sem4tue,'sem43':sem4wed,'sem44':sem4thu,'sem45':sem4fri,'sem51':sem5mon,'sem52':sem5tue,'sem53':sem5wed,'sem54':sem5thu,'sem55':sem5fri,'sem61':sem6mon,'sem62':sem6tue,'sem63':sem6wed,'sem64':sem6thu,'sem65':sem6fri,'sem71':sem7mon,'sem72':sem7tue,'sem73':sem7wed,'sem74':sem7thu,'sem75':sem7fri,'sem81':sem8mon,'sem82':sem8tue,'sem83':sem8wed,'sem84':sem8thu,'sem85':sem8fri,'did':did})


def mentor_view_timetable(request, id):
	cursor = connection.cursor()
	did = request.session['mentordepid']
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='monday' ")
	sem1mon=cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='tuesday' ")
	sem1tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='wednesday' ")
	sem1wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='thursday' ")
	sem1thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='1' and time_table.day='friday' ")
	sem1fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='monday'  ")
	sem2mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='tuesday'  ")
	sem2tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='wednesday'  ")
	sem2wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='thursday'  ")
	sem2thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='2' and time_table.day='friday'  ")
	sem2fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='monday'  ")
	sem3mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='tuesday'  ")
	sem3tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='wednesday'  ")
	sem3wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='thursday'  ")
	sem3thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='3' and time_table.day='friday'  ")
	sem3fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='monday'  ")
	sem4mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='tuesday'  ")
	sem4tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='wednesday'  ")
	sem4wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='thursday'  ")
	sem4thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='4' and time_table.day='friday'  ")
	sem4fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='monday'  ")
	sem5mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='tuesday'  ")
	sem5tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='wednesday'  ")
	sem5wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='thursday'  ")
	sem5thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='5' and time_table.day='friday'  ")
	sem5fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='monday'  ")
	sem6mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='tuesday'  ")
	sem6tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='wednesday'  ")
	sem6wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='thursday'  ")
	sem6thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='6' and time_table.day='friday'  ")
	sem6fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='monday'  ")
	sem7mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='tuesday'  ")
	sem7tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='wednesday'  ")
	sem7wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='thursday'  ")
	sem7thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='7' and time_table.day='friday'  ")
	sem7fri = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='monday' ")
	sem8mon = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='tuesday' ")
	sem8tue = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='wednesday' ")
	sem8wed = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='thursday' ")
	sem8thu = cursor.fetchone()
	cursor.execute("select p1.subject_name,time_table.period1, p2.subject_name,time_table.period2,p3.subject_name,time_table.period3,p4.subject_name,time_table.period4,p5.subject_name,time_table.period5 from subject as p1 join subject as p2 join subject as p3 join subject as p4 join subject as p5 join time_table where p1.idsubject = time_table.period1 and p2.idsubject = time_table.period2 and p3.idsubject = time_table.period3 and p4.idsubject = time_table.period4 and p5.idsubject = time_table.period5 and time_table.course_id='" + str(id) + "' and time_table.semester='8' and time_table.day='friday' ")
	sem8fri = cursor.fetchone()
	return render(request,"mentor_view_time_table.html",{'sem11':sem1mon,'sem12':sem1tue,'sem13':sem1wed,'sem14':sem1thu,'sem15':sem1fri,'sem21':sem2mon,'sem22':sem2tue,'sem23':sem2wed,'sem24':sem2thu,'sem25':sem2fri,'sem31':sem3mon,'sem32':sem3tue,'sem33':sem3wed,'sem34':sem3thu,'sem35':sem3fri,'sem41':sem4mon,'sem42':sem4tue,'sem43':sem4wed,'sem44':sem4thu,'sem45':sem4fri,'sem51':sem5mon,'sem52':sem5tue,'sem53':sem5wed,'sem54':sem5thu,'sem55':sem5fri,'sem61':sem6mon,'sem62':sem6tue,'sem63':sem6wed,'sem64':sem6thu,'sem65':sem6fri,'sem71':sem7mon,'sem72':sem7tue,'sem73':sem7wed,'sem74':sem7thu,'sem75':sem7fri,'sem81':sem8mon,'sem82':sem8tue,'sem83':sem8wed,'sem84':sem8thu,'sem85':sem8fri,'did':did})


def register_student(request, id):
	did = request.session['sdepid']
	return render(request, "teacher_studreg.html",{'id':id,'did':did})
def stud_register(request):
	if request.method == "POST":
		dept=request.session['sdepid']
		rname=request.POST['rname']
		name = request.POST['name']
		course = request.POST['course']
		email = request.POST['email']
		address = request.POST['address']
		phnum = request.POST['phone']
		password= request.POST['password']
		pincode=request.POST['pincode']
		semester=request.POST['txtsemester']
		cursor = connection.cursor()
		cursor.execute("select * from student where register_number ='"+str(rname)+"' ")
		rollnum= cursor.fetchone()
		if rollnum == None:
			cursor.execute("insert into student values(null,'" + name + "','" + str(dept) + "','" + address + "','" + email + "','" + phnum + "','" + password + "','"+str(semester)+"','" + pincode + "','" + str(course) + "','"+str(rname)+"')")
		else:
			messages.error(request, 'Register Number Already Exists Please Add Unique Register Number')
			return HttpResponse("<script> alert('Register Number Already Exists Please Add Unique Register Number');window.location='../staff_view_department';</script>")

	return redirect("staff_view_department")

def stud_view_profile(request):
	student =request.session['studid']
	cursor = connection.cursor()
	cursor.execute("select student.student_id,student.register_number,student.name,department.name,course.course_name,student.semester,student.address,student.phone,student.email,student.pincode from student join department join course where student.course_id = course.idcourse and student.department_id = department.iddepartment and student.register_number ='"+str(student)+"' ")
	profile = cursor.fetchone()
	return render(request,'stud_view_profile.html',{'profile':profile})

def change_password(request,id):
	return render(request,'change_password.html',{'id':id})

def update_password(request):
	stud = request.session['studid']
	if request.method == "POST":
		id=request.POST['id']
		old=request.POST['old']
		new = request.POST['new']
		new1 = request.POST['new1']
		cursor=connection.cursor()
		cursor.execute("select * from student where student_id='"+str(id)+"' and register_number ='"+str(stud)+"' and password ='"+str(old)+"' ")
		data = cursor.fetchone()
		if data == None:
			return HttpResponse("<script> alert('Password Incorrect');window.location='../stud_view_profile';</script>")
		else:
			if new == new1:
				if new == old:
					return HttpResponse("<script> alert('you entered same password as new please enter new password ');window.location='../stud_view_profile';</script>")
				else:
					cursor.execute("update student set password ='"+str(new)+"' where student_id ='"+(id)+"' and register_number ='"+str(stud)+"' ")
					return HttpResponse("<script> alert('Password Updated Succesfully');window.location='../stud_view_profile';</script>")

			else:
				return HttpResponse("<script> alert('New Passwords Conformed Incorrectly ');window.location='../stud_view_profile';</script>")



def manager_view_profile(request):
	staff =request.session['staffid']
	cursor = connection.cursor()
	cursor.execute("select * from staff_details where staff_id ='"+str(staff)+"' ")
	profile = cursor.fetchone()
	return render(request,'manager_view_profile.html',{'profile':profile})

def manager_change_password(request,id):
	return render(request,'manager_change_password.html',{'id':id})


def manager_update_password(request):
	staff = request.session['staffid']
	if request.method == "POST":
		id =request.POST['id']
		old=request.POST['old']
		new = request.POST['new']
		new1 = request.POST['new1']
		cursor=connection.cursor()
		cursor.execute("select * from staff_details where staff_id='"+str(staff)+"' and password ='"+str(old)+"' ")
		data = cursor.fetchone()
		if data == None:
			return HttpResponse("<script> alert('Password Incorrect');window.location='../manager_view_profile';</script>")
		else:
			if new == new1:
				if new == old:
					return HttpResponse("<script> alert('you entered same password as new please enter new password ');window.location='../manager_view_profile';</script>")
				else:
					cursor.execute("update staff_details set password ='"+str(new)+"' where staff_id ='"+(staff)+"'")
					return HttpResponse("<script> alert('Password Updated Succesfully');window.location='../manager_view_profile';</script>")

			else:
				return HttpResponse("<script> alert('New Passwords Conformed Incorrectly ');window.location='../manager_view_profile';</script>")



def teacher_view_profile(request):
	staff =request.session['staffid']
	cursor = connection.cursor()
	cursor.execute("select * from staff_details where staff_id ='"+str(staff)+"' ")
	profile = cursor.fetchone()
	return render(request,'teacher_view_profile.html',{'profile':profile})

def teacher_change_password(request,id):
	return render(request,'teacher_change_password.html',{'id':id})


def teacher_update_password(request):
	staff = request.session['staffid']
	if request.method == "POST":
		id=request.POST['id']
		old=request.POST['old']
		new = request.POST['new']
		new1 = request.POST['new1']
		cursor=connection.cursor()
		cursor.execute("select * from staff_details where staff_id='"+str(staff)+"' and password ='"+str(old)+"' ")
		data = cursor.fetchone()
		if data == None:
			return HttpResponse("<script> alert('Password Incorrect');window.location='../teacher_view_profile';</script>")
		else:
			if new == new1:
				if new == old:
					return HttpResponse("<script> alert('you entered same password as new please enter new password ');window.location='../teacher_view_profile';</script>")
				else:
					cursor.execute("update staff_details set password ='"+str(new)+"' where staff_id ='"+(staff)+"'")
					return HttpResponse("<script> alert('Password Updated Succesfully');window.location='../teacher_view_profile';</script>")

			else:
				return HttpResponse("<script> alert('New Passwords Conformed Incorrectly ');window.location='../teacher_view_profile';</script>")



def mentor_view_profile(request):
	staff =request.session['staffid']
	cursor = connection.cursor()
	cursor.execute("select * from staff_details where staff_id ='"+str(staff)+"' ")
	profile = cursor.fetchone()
	return render(request,'mentor_view_profile.html',{'profile':profile})



def mentor_change_password(request,id):
	return render(request,'mentor_change_password.html',{'id':id})

def mentor_update_password(request):
	staff = request.session['staffid']
	if request.method == "POST":
		id=request.POST['id']
		old=request.POST['old']
		new = request.POST['new']
		new1 = request.POST['new1']
		cursor=connection.cursor()
		cursor.execute("select * from staff_details where staff_id='"+str(staff)+"' and password ='"+str(old)+"' ")
		data = cursor.fetchone()
		if data == None:
			return HttpResponse("<script> alert('Password Incorrect');window.location='../mentor_view_profile';</script>")
		else:
			if new == new1:
				if new == old:
					return HttpResponse("<script> alert('you entered same password as new please enter new password ');window.location='../mentor_view_profile';</script>")
				else:
					cursor.execute("update staff_details set password ='"+str(new)+"' where staff_id ='"+(staff)+"'")
					return HttpResponse("<script> alert('Password Updated Succesfully');window.location='../mentor_view_profile';</script>")

			else:
				return HttpResponse("<script> alert('New Passwords Conformed Incorrectly ');window.location='../mentor_view_profile';</script>")


def pending_student_registration(request):
	cursor = connection.cursor()
	cursor.execute("select * from student where status ='pending' ")
	data = cursor.fetchall()
	return render(request, "pending_student_reg.html")


def stud_attend(request):
	if request.method == "POST":
		studid = request.POST['txtstudentid']
		name = request.POST['txtname']
		date = request.POST['txtdate']
		semester = request.POST['txtsemester']
		hour = request.POST['txthour']
		status = request.POST['txtstatus']
		cursor = connection.cursor()
		cursor.execute("insert into stud_attend values('" + studid + "','" + name + "','" + date + "','" + semester + "','" + hour + "','" + status + "')")
		return HttpResponse( "<script> alert('Registered').window.location='/login',</script>")
	return render(request, "login.html")


def stud_course(request):
	if request.method == "POST":
		courses = request.POST['txtselect']
		coursefee = requet.POST['txtcoursesfee']

		cursor = connection.cursor()
		cursor.execute("insert into stud_course values('" + courses + "','" + coursefee + "')")
		return HttpResponse("< script > alert('Registered').window.location='/login',</script>")
	return render(request, "login.html")


def stud_feedback(request):
	if request.method == "POST":
		studid = request.POST['txtstudentid']
		department = requet.POST['txtdepartment']
		semester = requet.POST['txtsemester']
		feedback = request.POST['txtfeedback']
		cursor = connection.cursor()
		cursor.execute("insert into stud_feedback values('" + studid + "','" + department + "','" + semester + "','" + feedback + "')")
		return HttpResponse("< script > alert('Registered').window.location='/login',</script>")
	return render(request, "login.html")


def stud_leave(request):
	if request.method == "POST":
		studid = request.POST['txtstudentid']
		date = requet.POST['txtdate']
		no_of_days = requet.POST['txtnoofdays']
		reason = request.POST['txtreason']
		status = request.POST['txtstatus']

		cursor = connection.cursor()
		cursor.execute("insert into stud_leave values('" + studid + "','" + date + "','" + no_of_days + "','" + reason + "','" + status + "')")
		return HttpResponse( "<script> alert('Registered').window.location='/login',</script>")
	return render(request, "login.html")


def sub_entre(request):
	if request.method == "POST":
		courses = request.POST['txtcourses']
		sem = requet.POST['txtsem']
		sub = requet.POST['txtsub']

		cursor = connection.cursor()
		cursor.execute("insert into subject values('" + courses + "','" + sem + "','" + sub + "')")
		return HttpResponse( "<script> alert('Registered').window.location='/login',</script>")
	return render(request, "login.html")






# view.text
def view_attend_(request):
	cursor = connection.cursor()
	cursor.execute("select * from attendance")
	data = cursor.fetchall()
	return render(request, "viewattend.html", {'data': data})



def edit_attend_(request, sid):
	cursor = connection.cursor()
	cursor.execute("select * from attend where student_id ='" + str(sid) + "'")
	data = cursor.fetchall()
	return render(request, "Admin/editattend.html", {'data': data})


def view_course_(request):
	cursor = connection.cursor()
	cursor.execute("select * from course")
	data = cursor.fetchall()
	return render(request, "Admin/viewcourse.html", {'data': data})



def edit_coursedetails_(request, sid):
	cursor = connection.cursor()
	cursor.execute("select * from attend where course_id ='" + str(sid) + "'")
	data = cursor.fetchall()
	return render(request, "Admin/edit_coursedetails.html", {'data': data})

def view_feedback_(request):
	cursor = connection.cursor()
	cursor.execute("select * from feedback")
	data = cursor.fetchall()
	return render(request, "Admin/viewfeedback.html", {'data': data})



def edit_feedback_(request, sid):
	cursor = connection.cursor()
	cursor.execute("select * from feedback where feedback_id ='" + str(sid) + "'")
	data = cursor.fetchall()
	return render(request, "Admin/feedback_id.html", {'data': data})


def view_leave_(request):
	cursor = connection.cursor()
	cursor.execute("select * from leave")
	data = cursor.fetchall()
	return render(request, "Admin/viewleave.html", {'data': data})



def edit_leave_(request, sid):
	cursor = connection.cursor()
	cursor.execute("select * from leave where leave_id ='" + str(sid) + "'")
	data = cursor.fetchall()
	return render(request, "Admin/editleave.html",{'data': data})



def edit_staffreg_(request, sid):
	cursor = connection.cursor()
	cursor.execute("select * from staffreg where reg_id ='" + str(sid) + "'")
	data = cursor.fetchall()
	return render(request, "Admin/admin_staffreg.html", {'data': data})

def view_studreg_(request):
	cursor = connection.cursor()
	cursor.execute("select * from studreg")
	data = cursor.fetchall()
	return render(request, "Admin/teacher_studreg.html", {'data': data})



def edit_studreg_(request, sid):
	cursor = connection.cursor()
	cursor.execute("select * from studreg where reg_id ='" + str(sid) + "'")
	data = cursor.fetchall()
	return render(request, "Admin/editstudreg.html", {'data': data})

def view_sub_(request):
	cursor = connection.cursor()
	cursor.execute("select * from subject")
	data = cursor.fetchall()
	return render(request, "Admin/viewsub.html", {'data': data})



def edit_sub_(request, sid):
	cursor = connection.cursor()
	cursor.execute("select * from subject where sub_id ='" + str(sid) + "'")
	data = cursor.fetchall()
	return render(request, "Admin/editsub.html", {'data': data})



# delete.text

def delete_attendence(request, id):
	cursor = connection.cursor()
	q = "delete from attendence where idattendence='" + roll_number + "','" + absent_date + '",'" + staff_id +'", '" + current semester +'" '" + str(id) + "'"
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewattendence';</scipt>")



def delete_course(request, aid):
	cursor = connection.cursor()
	q = " delete from course where idcourse='" + iddepartment + "','" + course_name + "','" +str(aid)+"'"
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewcourse';</scipt>")




def delete_feedback(request, fid):
	cursor = connection.cursor()
	q = " delete from feedback where idfeedback='"+fid +"' "
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewfeedback';</scipt>")




def delete_fees_payment(request, feid):
	cursor = connection.cursor()
	q = " delete from fees_payment where idfees_payment='" + feid + "' "
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewfeedback';</scipt>")




def delete_internal_mark(request, imid):
	cursor = connection.cursor()
	q = " delete from internal_mark where idinternal_mark='" + imid + "' "
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewinternal_mark';</scipt>")




def delete_late_attendence(request, laid):
	cursor = connection.cursor()
	q = " delete from late_attendence where idlate_attendence='" + laid + "' "
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewlate_attendence';</scipt>")




def delete_leave(request, leaveid):
	cursor = connection.cursor()
	q = " delete from leave where idleave='" + leaveid + "' "
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewleave';</scipt>")




def delete_notification(request, nid):
	cursor = connection.cursor()
	q = " delete from unotification where idnotification='" + nid + "' "
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewnotification';</scipt>")




def delete_staff_details(request, sdid):
	cursor = connection.cursor()
	q = " delete from staff_details where staffid='" + str(sdid) + "' "
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewstaff_details';</scipt>")




def delete_sudent(request, sid):
	cursor = connection.cursor()
	q = " delete from sudent where roll_no='" + str(sid) + "'"
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewstudent';</scipt>")


def delete_subject(request, suid):
	cursor = connection.cursor()
	q = " delete from subject where idsubject='" + suid + "' "
	cursor.execute(q)
	return HttpResponse("<script>alert('deleted...');window.location='/viewsubject';</scipt>")



def manager_stud_fees(request,id):
	cid = request.session['managercourid']
	request.session['managestudid'] = id
	cursor = connection.cursor()
	cursor.execute("select fees_payment.*,fees.fees_type, fees.courseid,fees.amount from  fees_payment join fees where fees.idfees = fees_payment.fees_type and fees_payment.roll_no ='"+str(id)+"' ")
	data = cursor.fetchall()
	return render(request,'manager_stud_fees.html',{'data':data,'cid':cid})

def approve_stud_fees(request,id):
      stud = request.session['managestudid']
      cursor = connection.cursor()
      cursor.execute("update fees_payment set status ='approved' where idfees_payment ='"+str(id)+"' ")
      return redirect('manager_stud_fees', id =stud)


def reject_stud_fees(request,id):
      stud = request.session['managestudid']
      cursor = connection.cursor()
      cursor.execute("update fees_payment set status ='rejected' where idfees_payment ='"+str(id)+"' ")
      return redirect('manager_stud_fees', id =stud)

def teacher_stud_fees(request,id):
    cid = request.session['scid']
    cursor = connection.cursor()
    cursor.execute("select fees_payment.*,fees.fees_type, fees.courseid,fees.amount from  fees_payment join fees where fees.idfees = fees_payment.fees_type and fees_payment.roll_no ='"+str(id)+"' ")
    data = cursor.fetchall()
    return render(request,'teacher_stud_fees.html',{'data':data,'cid':cid})

def update_to_next_sem(request,id):
    cid = request.session['scid']
    cursor = connection.cursor()
    cursor.execute("select semester from student where register_number ='"+str(id)+"' ")
    data = cursor.fetchone()
    data = list(data)
    semester=data[0]
    semester =int(semester) + 1
    cursor.execute("update student set semester='"+str(semester)+"' where register_number ='"+str(id)+"' ")
    return redirect('staff_view_semester',id= int(cid))