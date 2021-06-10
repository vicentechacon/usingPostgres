from django.db import models
import re

from django.db.models.fields import related
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UsuarioManager(models.Manager):
    def validacionesBasicas(self, usuario, confirmarPassword):
        errores = {}
        print('*'*50)
        print(usuario)
        validarLongitud('Nombre', usuario.nombre, 3, errores)
        validarLongitud('Apellido', usuario.apellido, 3, errores)
        validarLongitud('Email', usuario.email, 5, errores)
        validarLongitud('Fecha Nacimiento', usuario.fecha_nacimiento, 10, errores)

        if not EMAIL_REGEX.match(usuario.email):
            errores['email'] = 'El email no tiene un formato válido.'
        
        if confirmarPassword or usuario.password:
            validarLongitud('password', usuario.password, 1, errores)
            if usuario.password != confirmarPassword:
                errores['password'] = 'Las contraseñas no coinciden'
        return errores


class UsuarioFiltros(models.Manager):
    def buscarPorNombre(self, nombre):
        return super().get_queryset().filter(nombre__icontains=nombre)

    def buscarPorApellido(self, apellido):
        return super().get_queryset().filter(apellido__icontains=apellido)



class Rut(models.Model):
    rut = models.CharField(max_length=12)
    fechaExpedicion = models.DateField()
    created_at = models.DateTimeField(auto_now_add= True) #--> Fecha y Hora
    updated_at = models.DateTimeField(auto_now= True)


class Usuario(models.Model):

    class Meta: #permite ordenar los datos
        ordering = ['-nombre']
        unique_together = (("nombre" ,"apellido"))  #tupla --> como un arreglo que no se puede modificar. | No pueden repetirse dos nombres+apellidos iguales

    #django automaticamnte agrega ID a la tabla
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    email = models.EmailField(max_length=20, unique=True)
    password = models.CharField(max_length=70)
    fecha_nacimiento = models.DateField()  #---> FECHA
    codigo = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add= True) #--> Fecha y Hora
    updated_at = models.DateTimeField(auto_now= True)
    # rut = models.OneToOneField(Rut, related_name='usuario', on_delete=models.CASCADE, null = True, blank=True)
    # likes = models.ManyToManyField(Mensaje, )  
    objects = UsuarioManager()
    filtrar = UsuarioFiltros()


    def __str__(self):
        return str(self.__dict__)
    
    
def validarLongitud(campo, cadena, minLength, errores):
    if len(cadena) < minLength:
        errores[campo] = f"el {campo} no puede ser menor de {minLength} caracteres"

class MensajeManager(models.Manager):
    def validacionesBasicas(self, mensaje):
        errores = {}
        validarLongitud('mensaje', mensaje.mensaje, 10, errores)
        return errores    
    
class Mensaje(models.Model):
    mensaje = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario =models.ForeignKey(Usuario, related_name='mensajes', on_delete=models.CASCADE) #Uno a Muchos
    le_gusta_a = models.ManyToManyField(Usuario, related_name='likes')
    lista_comentarios = models.ManyToManyField(Usuario, through='Comentario')
    objects = MensajeManager()

    def __str__(self):
        return self.mensaje

class Comentario(models.Model):
    comenario = models.CharField(max_length=255)
    puntaje = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(Usuario, related_name='comentarios', on_delete=models.CASCADE)
    mensaje = models.ForeignKey(Mensaje, related_name='comentarios', on_delete=models.CASCADE)

