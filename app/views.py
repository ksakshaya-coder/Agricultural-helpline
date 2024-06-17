from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
from django.db.models import Sum
import random 
from django.conf import settings
from django.utils import timezone
from django.db import connection
from django.db.models import Q
from django.core.mail import send_mail
from django.core.mail import EmailMessage
def home(request):
	return render(request,'home.html',{})
def officer_login(request):
	if request.method == 'POST':
		name=request.POST.get('username')
		pwd=request.POST.get('password')
		user_exist=Agriculture_Officer_Detail.objects.filter(username=name,password=pwd)
		if user_exist:
			request.session['officer_name']= request.POST.get('username')
			a = request.session['officer_name']
			sess = Agriculture_Officer_Detail.objects.only('id').get(username=a).id
			request.session['officer_id']= sess
			return redirect('officer_dashboard')
		else:
			messages.success(request,'Invalid username or Password')
	return render(request,'officer_login.html',{})
def officer_dashboard(request):
	if request.session.has_key('officer_name'):
		return render(request,'officer_dashboard.html',{})
	else:
		return render(request,'officer_login.html',{})
def officer_logout(request):
	try:
		del request.session['officer_name']
		del request.session['officer_id']
	except:
		pass
	return render(request, 'officer_login.html', {})
def register(request):
	if request.method == 'POST':
		Name = request.POST.get('uname')
		Adddress = request.POST.get('address')
		Mobile= request.POST.get('mobile')
		Email = request.POST.get('email')
		Password = request.POST.get('pwd')
		utype = request.POST.get('user_type')
		crt = Register_Detail.objects.create(name=Name,
		address=Adddress,mobile=Mobile,password=Password,email=Email,user_type=utype)
		if crt:
			messages.success(request,'Registered Successfully')
	return render(request,'register.html',{})
def user_login(request):
	if request.method == 'POST':
		name=request.POST.get('username')
		pwd=request.POST.get('password')
		user_type = request.POST.get('user_type')
		user_exist=Register_Detail.objects.filter(name=name,password=pwd,user_type=user_type)
		if user_exist:
			request.session['name']= request.POST.get('username')
			request.session['u_type']= request.POST.get('user_type')
			a = request.session['name']
			sess = Register_Detail.objects.only('id').get(name=a).id
			request.session['user_id']= sess
			return redirect('dashboard')
		else:
			messages.success(request,'Invalid username or Password')
	return render(request,'user_login.html',{})
def dashboard(request):
	if request.session.has_key('name'):
		return render(request,'dashboard.html',{})
	else:
		return render(request,'user_login.html',{})
def logout(request):
	try:
		del request.session['name']
		del request.session['user_id']
	except:
		pass
	return render(request, 'user_login.html', {})
def categories(request):
	if request.session.has_key('name'):
		a=Category.objects.all()
		return render(request,'categories.html',{'b':a})
	else:
		return render(request,'user_login.html',{})
def add_product(request):
	if request.session.has_key('name'):
		a=Category.objects.all()
		user_id = request.session['user_id']
		uid = Register_Detail.objects.get(id=int(user_id))
		if request.method == 'POST':
			a=request.POST.get('name')
			b=request.POST.get('price')
			c=request.POST.get('category')
			d=request.POST.get('con')
			f =request.FILES['pic']
			c_id=Category.objects.get(id=int(c))
			prt = Product.objects.create(p_name=a,p_price=b,category=c_id,note=d,cmp_price='',image=f,user_id=uid)
			if prt:
				messages.success(request,'Product Added Successfully')
		return render(request,'add_product.html',{'a':a})
	else:
		return render(request,'user_login.html',{})
def view_product(request):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		a=Product.objects.filter(user_id=int(user_id))
		return render(request,'view_product.html',{'b':a})
	else:
		return render(request,'user_login.html',{})
def product_edit(request,pk):
	if request.session.has_key('name'):
		a=Product.objects.filter(id=pk)
		b = Category.objects.all()
		if request.method == 'POST':
			a=request.POST.get('name')
			b=request.POST.get('price')
			c=request.POST.get('category')
			d=request.POST.get('con')
			e = request.POST.get('others')
			c_id=Category.objects.get(id=int(c))
			f = request.FILES['image']
			prt = Product.objects.filter(id=pk).update(image=f,p_name=a,p_price=b,category=c_id,note=d,cmp_price=e)
			if prt:
				return redirect('view_product')
				messages.success(request,'Product Updated Successfully')
		return render(request,'product_edit.html',{'value':a,'b':b})
	else:
		return render(request,'user_login.html',{})
def product_delete(request,pk):
	if request.session.has_key('name'):
		a=Product.objects.filter(id=pk).delete()
		return redirect('view_product')
	else:
		return render(request,'user_login.html',{})
def view_farmer(request):
	a=Register_Detail.objects.filter(user_type='farmer')
	return render(request,'farmer_info.html',{'b':a})
def veg_product(request):
	user_id = request.GET.get('fid')
	product = Product.objects.filter(user_id=int(user_id))
	return render(request,'veg_product.html',{'product':product})
def add_forming(request):
	if request.session.has_key('officer_name'):
		user_id = request.session['officer_id']
		uid = Agriculture_Officer_Detail.objects.get(id=int(user_id))
		if request.method == 'POST':
			a=request.POST.get('name')
			b=request.POST.get('water_contain')
			c=request.POST.get('fertilizer')
			d=request.POST.get('soil')
			f =request.FILES['image']
			g = request.POST.get('area')
			c_id=request.POST.get('season')
			h = request.POST.get('others')
			prt = Forming_Detail.objects.create(name=a,water_contain=b,fertilizer=c,soil=d,area=g,image=f,
			user_id=uid,season=c_id,others=h)
			if prt:
				messages.success(request,'Details Added Successfully')
		return render(request,'add_forming.html',{})
	else:
		return render(request,'officer_login.html',{})
def forming(request):
	if request.session.has_key('officer_name'):
		user_id = request.session['officer_id']
		a = Forming_Detail.objects.filter(user_id=int(user_id))
		return render(request,'forming.html',{'a':a})
	else:
		return render(request,'officer_login.html',{})
def delete(request,pk):
	if request.session.has_key('officer_name'):
		user_id = request.session['officer_id']
		a = Forming_Detail.objects.filter(id=pk).delete()
		return redirect('forming')
	else:
		return render(request,'officer_login.html',{})
def search(request):
	if request.method == 'POST':
		a = request.POST.get('search')
		b = request.POST.get('year')
		ids = Forming_Detail.objects.filter(name__istartswith=a,month__istartswith=b)
		return render(request,'search.html',{'ids':ids})
	else:
		return render(request,'search.html',{})
def contact(request):
	if request.method == 'POST':
		e_mail = request.GET.get('email')
		recipient_list = [e_mail]
		email_from = settings.EMAIL_HOST_USER
		name = request.POST.get('name')
		email_id = request.POST.get('mail')
		sub = request.POST.get('subject')
		msg = request.POST.get('msg')
		b = EmailMessage('Name:'+name,'Email:'+ email_id+ 'Subject:'+sub+ 'Message:' +msg,email_from,recipient_list).send()
		messages.success(request,'Your Message Send. We Get Back to You Soon.')
	return render(request,'contact.html',{})
def add_video(request):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		uid = Register_Detail.objects.get(id=int(user_id))
		if request.method == 'POST':
			a=request.POST.get('title')
			b=request.POST.get('desc')
			f =request.FILES['video']			
			prt = Video_Detail.objects.create(title=a,desc=b,video=f,
			user_id=uid)
			if prt:
				messages.success(request,'Video Added Successfully')
		return render(request,'add_video.html',{})
	else:
		return render(request,'user_login.html',{})
def videos(request):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		product = Video_Detail.objects.filter(user_id=int(user_id))
		return render(request,'videos.html',{'b':product})
	else:
		return render(request,'user_login.html',{})
def delete_video(request,pk):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		a = Video_Detail.objects.filter(id=pk).delete()
		return redirect('videos')
	else:
		return render(request,'user_login.html',{})
def video_list(request):
	a = Video_Detail.objects.all()
	return render(request,'video_list.html',{'a':a})
def add_officer_video(request):
	if request.session.has_key('officer_name'):
		user_id = request.session['officer_id']
		uid = Agriculture_Officer_Detail.objects.get(id=int(user_id))
		if request.method == 'POST':
			a=request.POST.get('title')
			b=request.POST.get('desc')
			f =request.FILES['video']			
			prt = Officer_Video_Detail.objects.create(title=a,desc=b,video=f,
			user_id=uid)
			if prt:
				messages.success(request,'Video Added Successfully')
		return render(request,'add_officer_video.html',{})
	else:
		return render(request,'officer_login.html',{})
def officer_video(request):
	if request.session.has_key('officer_name'):
		user_id = request.session['officer_id']
		product = Officer_Video_Detail.objects.filter(user_id=int(user_id))
		return render(request,'officer_video.html',{'b':product})
	else:
		return render(request,'officer_login.html',{})
def delete_officer_video(request,pk):
	if request.session.has_key('officer_name'):
		user_id = request.session['officer_id']
		a = Officer_Video_Detail.objects.filter(id=pk).delete()
		return redirect('officer_videos')
	else:
		return render(request,'officer_login.html',{})
def event_detail(request):
	a=Event_Detail.objects.all().order_by('-id')
	return render(request,'event_detail.html',{'b':a})
def insurance_detail(request):
	a=Insurance_Detail.objects.all().order_by('-id')
	return render(request,'insurance_detail.html',{'b':a})
def seeds_detail(request):
	if request.method == 'POST':
		a = request.POST.get('search')
		ids = Seeds_Stock.objects.filter(district__istartswith=a)
		return render(request,'seeds_detail.html',{'b':ids})
	else:
		return render(request,'seeds_detail.html',{})
def weather(request):
	if request.method == 'POST':
		a = request.POST.get('search')
		b = request.POST.get('date')
		ids = Weather_Detail.objects.filter(district__istartswith=a,date=b)
		return render(request,'weather.html',{'b':ids})
	else:
		return render(request,'weather.html',{})
def question(request):
	detail = Register_Detail.objects.filter(user_type='Consultant')
	if request.method == 'POST':
		expert_id = request.POST.get('name')
		question = request.POST.get('question')
		c = Register_Detail.objects.get(id=int(expert_id))
		user_id = request.session['user_id']
		ids = Ask_Question.objects.create(expert_name=c,farmer_name=int(user_id),question=question,answer='')
		if ids:
			messages.success(request,'We will answer you soon.')
		return render(request,'question.html',{'detail':detail})
	else:
		return render(request,'question.html',{'detail':detail})
def view_question(request):
	user_id = request.session['user_id']
	a = Ask_Question.objects.filter(farmer_name=int(user_id))
	return render(request,'view_question.html',{'b':a})
def view_answer(request,pk):
	user_id = request.session['user_id']
	a = Ask_Question.objects.filter(id=pk)
	return render(request,'view_answer.html',{'a':a})
def answer(request):
	user_id = request.session['user_id']
	cursor = connection.cursor()
	post = ''' SELECT r.name,a.question,a.id from app_register_detail as r INNER JOIN app_ask_question as a ON r.id=a.farmer_name
	where a.expert_name_id='%d' ''' % (int(user_id))
	sql = cursor.execute(post)
	row = cursor.fetchall()
	return render(request,'answer.html',{'row':row})
def reply(request,pk):
	user_id = request.session['user_id']
	a = Ask_Question.objects.filter(id=pk)
	if request.method == 'POST':
		answer = request.POST.get('answer')
		a = Ask_Question.objects.filter(id=pk).update(answer=answer)
		return redirect('answer')
	return render(request,'reply.html',{'a':a})
def add_tractor(request):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		uid = Register_Detail.objects.get(id=int(user_id))
		if request.method == 'POST':
			image=request.FILES['image']
			amount=request.POST.get('amount')
			lease=request.POST.get('lease')
			feature=request.POST.get('feature')
			status = request.POST.get('status')
			prt = Tractor_Detail.objects.create(image=image,amount=amount,lease=lease,
			feature=feature,status=status,user_id=uid)
			if prt:
				messages.success(request,' Added Successfully')
		return render(request,'add_tractor.html',{})
	else:
		return render(request,'user_login.html',{})
def view_tractor(request):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		a = Tractor_Detail.objects.filter(user_id=int(user_id))
		return render(request,'view_tractor.html',{'a':a})
	else:
		return render(request,'user_login.html',{})
def tractor_edit(request,pk):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		a = Tractor_Detail.objects.filter(id=pk)
		if request.method == 'POST':
			amount=request.POST.get('amount')
			lease=request.POST.get('lease')
			feature=request.POST.get('feature')
			status = request.POST.get('status')
			prt = Tractor_Detail.objects.filter(id=pk).update(amount=amount,lease=lease,
			feature=feature,status=status)
			if prt:
				messages.success(request,' Updated Successfully')
		return render(request,'tractor_edit.html',{'a':a})
	else:
		return render(request,'user_login.html',{})
def tractor_delete(request,pk):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		a = Tractor_Detail.objects.filter(id=pk).delete()
		return redirect('view_tractor')
	else:
		return render(request,'user_login.html',{})
def tractors(request):
	if request.session.has_key('name'):
		a = Tractor_Detail.objects.filter(status='Open')
		return render(request,'tractors.html',{'a':a})
	else:
		return render(request,'user_login.html',{})
def enquiry(request,pk):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		a = Tractor_Detail.objects.get(id=pk)
		farmer_id = Register_Detail.objects.get(id=int(user_id))
		crt = Apply.objects.create(user_id=farmer_id,tractor_id=a,status='pending')
		if crt:
			messages.success(request,'We Will Contact You Soon.')
		return render(request,'enquiry.html',{})
	else:
		return render(request,'user_login.html',{})
def enquiry_details(request):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		a = Apply.objects.filter(tractor_id__in=Tractor_Detail.objects.filter(user_id=int(user_id)))
		return render(request,'enquiry_details.html',{'a':a})
	else:
		return render(request,'user_login.html',{})

def accept(request,pk):
	if request.session.has_key('name'):
		a = Apply.objects.filter(id=pk).update(status='accept')
		return redirect('enquiry_details')
	else:
		return render(request,'user_login.html',{})

def reject(request,pk):
	if request.session.has_key('name'):
		a = Apply.objects.filter(id=pk).update(status='reject')
		return redirect('enquiry_details')
	else:
		return render(request,'user_login.html',{})
def tractor_enquiry(request):
	if request.session.has_key('name'):
		user_id = request.session['user_id']
		a = Apply.objects.filter(user_id=int(user_id))
		return render(request,'tractor_enquiry.html',{'a':a})
	else:
		return render(request,'user_login.html',{})

