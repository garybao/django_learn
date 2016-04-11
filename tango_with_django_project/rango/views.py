from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
#Import the Category model
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

def index(request):
	request.session.set_test_cookie()
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
	context_dict['result_list']=None
	context_dict['query']=None
	name_slug = category_name_slug
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			name_slug = query
	try:
		category = Category.objects.get(slug=name_slug)
		context_dict['category_name']=category.name
		pages = Page.objects.filter(category=category).order_by('-views')
		#context_dict['pages_title'] = pages.title
		context_dict['pages'] = pages
		context_dict['category']=category
		context_dict['category_name_slug']=name_slug
		context_dict['result_list'] = pages
		context_dict['query'] = name_slug

	except Category.DoesNotExist:
		pass
	if not context_dict['query']:
		context_dict['query'] = name_slug
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

def register(request):
	if request.session.test_cookie_worked():
		print ">>> TEST COOKIE WORKED!"
		request.session.delete_test_cookie()
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				profile.save()
				registered = True
			else:
				print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,
			'rango/register.html',
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your Rango account is disable.")
		else:
			print "Invalid login details:{0},{1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'rango/login.html',{})

@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')

def track_url(request):
	page_id =None
	url = '/rango/'
	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			try:
				page = Page.objects.get(id=page_id)
				page.views = page.views + 1
				page.save()
				url = page.url 
			except:
				pass
	return redirect(url)

@login_required
def like_category(request):
	cat_id = None
	if request.method == 'GET':
		cat_id = request.GET['category_id']
	likes = 0 
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1
			cat.likes = likes 
			cat.save()
	return HttpResponse(likes)