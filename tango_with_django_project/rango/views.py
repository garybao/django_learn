from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
#Import the Category model
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm

def index(request):
	context_dict = {}
	#query the Category table order by likes in descending order.
	#retrieve the top 5 only
	category_list = Category.objects.order_by('-likes')[:10]
	#context_dict = {'categories':category_list}
	context_dict['categories']=category_list
	page_list = Page.objects.order_by('views')[:10]
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

def add_category(request):
	if request.method =='POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()
	return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None 

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request,category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()
	context_dict = {'form':form, 'category': cat}
	return render(request, 'rango/add_page.html',context_dict)
