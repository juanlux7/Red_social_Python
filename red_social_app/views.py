from django.shortcuts import render, redirect, HttpResponse, reverse
from . import models, forms
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login as inicio_sesion
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.views.generic import View
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def login(request):

	if request.method == 'POST':

		usuario = request.POST['username']
		password = request.POST['password']


		intento_logueo = authenticate(username=usuario, password=password)

		if intento_logueo is not None:

			inicio_sesion(request, intento_logueo)


			return redirect(reverse('menu'))

			
		else:

			return render(request, 'base.html', {'error': 'el usuairo y/o contrasena son incorrectos'});



	return render(request, 'login.html')


def desloguear(request):
	logout(request)
	return redirect(reverse('login'))



def menu(request):

	usuarios_seguidos = models.Usuarios_seguidos.objects.values('usuario_seguido_id').filter(usuario_id=request.user.id) 

	posts = models.Posts.objects.select_related('user_post').select_related('user_post_extra').filter(Q(user_post_id__in=usuarios_seguidos) | Q(user_post_id=request.user.id)).order_by('-post_date')


	#variable que en base a los usuarios seguidos, ejecuta una consulta sobre los post e info extra de los usuarios
	page = request.GET.get('page', 1)
	paginator = Paginator(posts, 2)
	try:
		numbers = paginator.page(page)
	except PageNotAnInteger:
		numbers = paginator.page(1)
	except EmptyPage:
		numbers = paginator.page(paginator.num_pages)

	if not request.user.is_authenticated():

		return redirect('/')


	
	return render(request, 'menu.html', {'posts' : numbers, 'usuarios_seguidos': usuarios_seguidos})


def crearcuenta(request):

	form = forms.formularioregistro()


	if request.method == 'POST':

		form = forms.formularioregistro(request.POST)

		if form.is_valid():

			usuario = User() #creacion nuevo objeto tipo User

			usuario_extra = models.Usuario_extra()

			usuario.username = form.cleaned_data['username'] #se limpian los datos para prevenir cualquier codigo malicioso
			usuario.first_name = form.cleaned_data['first_name']
			usuario.last_name = form.cleaned_data['last_name']
			usuario.email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			usuario.password=make_password(password) #modulo de encriptacion

			usuario.save()

			usuario_extra.user_id = usuario.id

			usuario_extra.save() #es necesario crear un registro en la tabla de informacion extra con el nuevo usuario registrado

			
			return redirect(reverse('menu'))



	return render(request, 'crearcuenta.html', {'form': form})

def actualizarcuenta(request):

	form = forms.formularioactualizar(instance=request.user)

	return render(request, 'actualizar.html', {'form': form})

def paginacioninfinita(request): #ejemplo de view para crear contenido paginado que se carga al hacer scroll

	numbers_list = range(1, 1000)
	page = request.GET.get('page', 1)
	paginator = Paginator(numbers_list, 20)
	try:
		numbers = paginator.page(page)
	except PageNotAnInteger:
		numbers = paginator.page(1)
	except EmptyPage:
		numbers = paginator.page(paginator.num_pages)

	return render(request, 'paginator.html', {'numbers': numbers})


	







