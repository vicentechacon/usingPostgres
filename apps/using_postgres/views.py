from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    usuarios = Usuario.objects.all()
    # usuarios = Usuario.filtrar.buscarPorNombre(['Vicente'])
    print(usuarios.query)
    context = {
        'usuarios': usuarios
    }
    return render(request, 'index.html', context)

def nuevo(request):
    if request.method == 'GET':
        return render(request, 'usuario.html')
    elif request.method == 'POST':
        usuario = crearObjetoUsuario(request)
        mostrarErrores = validarUsuario(request, usuario, request.POST['confirmarPassword'])
        if mostrarErrores:
            return mostrarErrores
        else:
            hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()) 
            usuario.password = hash.decode()
            usuario.save()  #asi se guarda un usuario
    return redirect('/')


def info(request, idUsuario):
    usuario = getUsuario(idUsuario)
    print(usuario)
    if usuario:
        return crearContext(request, usuario, 'info.html')
    return redirect('/') 
    

def editar(request, idUsuario):   
    usuario = getUsuario(idUsuario)
    if usuario:
        if request.method == 'GET':
            return crearContext(request, usuario)
        elif request.method == 'POST':
            usuario = crearObjetoUsuario(request, usuario)
            mostrarErrores = validarUsuario(request, usuario, request.POST['confirmarPassword'])
            if mostrarErrores:
                return mostrarErrores
            else:
                usuario.save()

    return redirect('/') 


def eliminar(request, idUsuario):
    usuario = getUsuario(request, idUsuario)
    if usuario:
        usuario.delete()
    return redirect('/')

def getUsuario(idUsuario = None, email= None):
    try:   
        if idUsuario: 
            usuario = Usuario.objects.get(id=idUsuario)
        elif email:
            usuario = Usuario.objects.get(email = email)
        return usuario
    except:
        return None


def crearObjetoUsuario(request, usuario=None):
    if usuario:
        newUser = usuario
    else:
        newUser = Usuario()

    newUser.nombre = request.POST['nombre']
    newUser.apellido = request.POST['apellido']
    newUser.email = request.POST['email']
    newUser.fecha_nacimiento = request.POST['fecha_nacimiento']
    newUser.codigo = request.POST['codigo']
    
    if len(request.POST['password']) > 0 and len(request.POST['confirmarPassword']) > 0:
        newUser.password = request.POST['password']

    return newUser

def validarUsuario(request, usuario, confirmarPassword=None):
    errores = Usuario.objects.validacionesBasicas(usuario, confirmarPassword)
    if len(errores)>0:
        generarMensajeError(request, errores)
        usuario = getUsuario(usuario.id)
        return crearContext(request, usuario)
        

def generarMensajeError(request, errores):
    for key, value in errores.items():  
        messages.error(request, value, key)
    

def crearContext(request, usuario, pagina = 'usuario.html'):
    context = {
        'mensajes': Mensaje.objects.all(),
        'usuario' : usuario 
    }
    return render(request, pagina, context)

def nuevoMensaje(request):
    if 'id' in request.session:
        usuario = getUsuario(request.session['id'])
        if request.method == 'GET':
            if usuario:
                return crearContext(request, usuario, 'mensajes.html')
        elif request.method == 'POST':
            mensaje = crearObjetoMensaje(request)
            mostrarErrores = mensajeValido(request, mensaje)
            if mostrarErrores:
                return mostrarErrores
            else:
                mensaje.usuario = usuario
                mensaje.save()
            return redirect ('/mensajes') 

    return redirect('/login')

def crearObjetoMensaje(request, mensaje= None):
    if mensaje:
        newMensaje = mensaje
    else:
        newMensaje = Mensaje()
    newMensaje.mensaje = request.POST['mensaje']
    return newMensaje

def mensajeValido(request, mensaje):
    errores = Mensaje.objects.validacionesBasicas(mensaje)  
    if len(errores) > 0:
        generarMensajeError(request, errores)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        usuario = getUsuario(email=request.POST['email']) 
        if usuario:
            #1. Contraseña de Login
            #1. Contraseña de la base de datos
            if bcrypt.checkpw(request.POST['password'].encode(), usuario.password.encode()):
                request.session['id'] = usuario.id
                return redirect('/mensajes')
    return redirect('/')  

def cerrarSession(request):
    if 'id' in request.session:
        del request.session['id']
    return redirect('/')  
    

def like(request, idMensaje):
    if 'id' in request.session:
        usuario = getUsuario(request.session['id'])
        mensaje = Mensaje.objects.get(id=idMensaje)
        # mensaje = Mensaje()
        # mensaje.le_gusta_a.add(usuario)
        usuario.likes.add(mensaje)
    return redirect ('/mensajes')

def confirmarEliminacion(request, idUsuario):
    usuario = getUsuario(idUsuario)
    if usuario:
        context = {
            'usuario' : usuario
        }
        return render(request, 'eliminar.html', context)

def page_not_found(request, exception, template_name="404.html"):
    response = render("404.html")
    response.status_code=404
    return response