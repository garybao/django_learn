from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
#Import the Category model
from rango.models import Category
from rango.models import Page

def index(request):
	context_dict = {}
	#query the Category table order by likes in descending order.
	#retrieve the top 5 only
	category_list = Category.objects.order_by('-likes')[:5]
	#context_dict = {'categories':category_list}
	context_dict['categories']=category_list
	page_list = Page.objects.order_by('views')[:5]
	context_dict['pages'] = page_list
	#context_dict = {'boldmessage': "I am bold font from the context"}
	return render(request,'rango/index.html',context_dict)
	#return HttpResponse("Rango says hey there world! <br/> <a href='/rango/about'>about</a>")
	

def about(request):
	contex_para = {'boldmessage': "This is about page"}
	return render(request, 'rango/about.html',contex_para)
	#return HttpResponse("Rango says hey is the about page. <br/> <a href='/rango'>index</a>")

def category(request, category_name_slug):
	#Create a context dictionary which we can pass to the template rendering engine.
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name']=category.name
		pages = Page.objects.filter(category=category)
		#context_dict['pages_title'] = pages.title
		context_dict['pages'] = pages
		context_dict['category']=category
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html',context_dict)
