from django.db import models

class Agriculture_Officer_Detail(models.Model):
	officer_name = models.CharField(max_length=50)
	mobile = models.CharField(max_length=20)
	designation = models.CharField(max_length=100)
	username = models.CharField(max_length=50,unique=True)
	password = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	address = models.TextField(max_length=2000)
	def __str__(self):
		return self.officer_name
class Register_Detail(models.Model):
	name = models.CharField(max_length=50,unique=True)
	address = models.CharField(max_length=50)
	mobile = models.CharField(max_length=20)
	password = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	user_type = models.CharField(max_length=30,null=True)
	image = models.FileField('Upload Image',upload_to='documents/',null=True)
	def __str__(self):
		return self.name
class Category(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=1000,null=True)
	def __str__(self):
		return self.name
class Product(models.Model):
	p_name = models.CharField(max_length=50)
	p_price = models.CharField(max_length=50)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	note = models.TextField(max_length=2000)
	cmp_price = models.CharField(max_length=50,null=True)
	image = models.FileField('Upload Image',upload_to='documents/',null=True)
	user_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.p_name
class Forming_Detail(models.Model):
	name = models.CharField('Vegetable Name',max_length=100)
	water_contain = models.TextField('Water Level',max_length=3000)
	fertilizer = models.TextField('Fertilizer',max_length=3000)
	soil = models.TextField('Nature of Soli',max_length=3000)
	
	season = models.TextField('Fertilize season',max_length=3000)
	others = models.TextField(max_length=3000)
	image = models.FileField('Upload Image',upload_to='farmer/')
	month = models.CharField('Month',max_length=100,null=True)
	def __str__(self):
		return self.name
class Video_Detail(models.Model):
	user_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE,null=True)
	title = models.CharField(max_length=100)
	desc = models.TextField(max_length=3000)
	video = models.FileField('Upload Video',upload_to='documents/')
	def __str__(self):
		return self.title
class Officer_Video_Detail(models.Model):
	user_id = models.ForeignKey(Agriculture_Officer_Detail, on_delete=models.CASCADE,null=True)
	title = models.CharField(max_length=100)
	desc = models.TextField(max_length=3000)
	video = models.FileField('Upload Video',upload_to='documents/')
	def __str__(self):
		return self.title
class Event_Detail(models.Model):
	event_name = models.CharField('Event Name',max_length=100)
	type_of_event = models.CharField('Event Type', max_length=100)
	date = models.DateField('Event Date')
	place = models.TextField('Event Place',max_length=3000)
	about_event = models.TextField('About Event',max_length=3000)
	address = models.TextField('Address',max_length=3000)
	benefits = models.TextField('Event Benefit',max_length=3000)
	image = models.FileField('Upload Image',upload_to='documents/')
	def __str__(self):
		return self.event_name
class Insurance_Detail(models.Model):
	insurance_scheme = models.CharField('Insurance Scheme',max_length=100)
	year = models.CharField('Year of Insurance', max_length=100)
	insurance_type = models.CharField('Type of Insurance',max_length=100)
	amount = models.CharField('Insurance Amount',max_length=300)
	monthly_amount =models.CharField('Monthly Due Amount',max_length=300)
	insurance_detail = models.TextField('Insurance Detail',max_length=3000)
	company_detail = models.TextField('Insurance Company Detail',max_length=3000)
	documents = models.TextField('Documents need for Insurance',max_length=3000)
	last_date = models.DateField('Last Date to Enquiry')
	insurance_form = models.FileField('Insurance Form',upload_to='documents/')
	def __str__(self):
		return self.insurance_scheme
class Seeds_Stock(models.Model):
	seed_name = models.CharField('Seed Name',max_length=100)
	stock = models.CharField('Stock',max_length=3000)
	district = models.CharField('district',max_length=3000)
	area = models.CharField('Area',max_length=3000)
	image = models.FileField('Upload Image',upload_to='farmer/')
	def __str__(self):
		return self.seed_name
class Weather_Detail(models.Model):
	wind_speed = models.CharField('Wind Speed',max_length=100)
	temprature = models.CharField('Temprature',max_length=100)
	humutity = models.CharField('Humutity',max_length=100)
	rainfall = models.CharField('Rainfall',max_length=100)
	district = models.CharField('District', max_length=100)
	date = models.DateField('Date')
	chance_of_rain = models.CharField('Chance of Rain', max_length=100)
	image = models.FileField('Upload Image',upload_to='documents/')
	def __str__(self):
		return self.district
class Ask_Question(models.Model):
	expert_name = models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	farmer_name = models.IntegerField()
	question = models.TextField('Question',max_length=3000)
	answer = models.TextField('Answer',max_length=3000)
	def __str__(self):
		return self.expert_name.name
class Tractor_Detail(models.Model):
	user_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	amount = models.CharField(max_length=100)
	lease = models.CharField(max_length=50)
	feature = models.TextField(max_length=3000)
	image = models.FileField('Upload Image',upload_to='documents/')
	status = models.CharField('Status',max_length=100)
	def __str__(self):
		return self.lease
class Apply(models.Model):
	user_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	tractor_id = models.ForeignKey(Tractor_Detail, on_delete=models.CASCADE)
	status = models.CharField(max_length=100)
	def __str__(self):
		return self.tractor_id.lease
