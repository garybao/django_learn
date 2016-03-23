from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
	context_dict = {'boldmessage': "I am bold font from the context"}
	return render(request,'rango/index.html',context_dict)
	#return HttpResponse("Rango says hey there world! <br/> <a href='/rango/about'>about</a>")
	

def about(request):
	contex_para = {'boldmessage': "This is about page"}
	return render(request, 'rango/about.html',contex_para)
	#return HttpResponse("Rango says hey is the about page. <br/> <a href='/rango'>index</a>")
