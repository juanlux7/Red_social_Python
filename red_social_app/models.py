from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


# Create your models here.



class Usuario_extra(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	direccion = models.CharField(max_length=50, null=True)
	descripcion = models.TextField(max_length=500, null=True)
	fecha_nacimiento = models.DateField(null=True)
	imagen_perfil = models.ImageField(null=True)


class Posts(models.Model):

	user_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
	user_post_extra = models.ForeignKey(Usuario_extra, on_delete=models.CASCADE, related_name="user_post_extra")
	post_content = models.CharField(max_length=200)
	post_date = models.DateField(null=True)

	def __unicode__(self):
		return self.post_content


class Usuarios_seguidos(models.Model):


	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario")
	usuario_seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_seguido")






