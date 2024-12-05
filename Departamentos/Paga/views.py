from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import GastoComun
from django.utils import timezone
from .models import Gasto
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Gasto
from .forms import CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.conf import settings
from .models import Residente
from .models import GastoComún


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:  # Verifica si es administrador
                return redirect('generate_expenses')  # Redirige a la página de administración
            else:
                return redirect('generate_expenses')  # Redirige al dashboard del residente
        else:
            messages.error(request, "Credenciales incorrectas")
            return redirect('login')  # Redirige al login si la autenticación falla
        
        
        
        

    return render(request, 'login.html')


# Vista para la página de gastos pendientes (requiere autenticación)
@login_required
def pending_expenses(request):
    return render(request, 'pending_expenses.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def generate_expenses_view(request):
    if request.method == "POST":
        try:
            # Recuperar datos del formulario
            descripcion = request.POST.get('description')
            monto = request.POST.get('amount')

            if not descripcion or not monto:
                return JsonResponse({'error': 'Faltan datos'}, status=400)

            # Crear un nuevo gasto
            nuevo_gasto = Gasto.objects.create(descripcion=descripcion, monto=monto)

            return JsonResponse({
                'id': nuevo_gasto.id,
                'descripcion': nuevo_gasto.descripcion,
                'monto': str(nuevo_gasto.monto),  # Convertir Decimal a string
                'fecha_creacion': nuevo_gasto.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Renderizar la plantilla en caso de un GET
    gastos = Gasto.objects.all()
    return render(request, 'generate_expenses.html', {'gastos': gastos})



def pending_expenses_view(request):
    gastos_pendientes = GastoComun.objects.filter(pagado=False)  # Filtra los gastos pendientes
    return render(request, 'pending_expenses.html', {'gastos_pendientes': gastos_pendientes})


def mark_paid_view(request, gasto_id):
    gasto = GastoComun.objects.get(id=gasto_id)
    gasto.pagado = True
    gasto.fecha_pago = timezone.now()  # Marca la fecha actual como la fecha de pago
    gasto.save()
    return redirect('pending_expenses')  # Redirige a la vista de gastos pendientes


def index_view(request):
    return render(request, 'index.html')  # Suponiendo que tienes un archivo 'index.html'


def mark_paid(request, gasto_id):
    # Obtener el gasto usando el ID
    gasto = get_object_or_404(Gasto, id=gasto_id)

    # Marcar el gasto como pagado
    gasto.pagado = True
    gasto.save()

    # Redirigir a una página de éxito o donde desees
    return render(request, 'paga/gasto_pagado.html', {'gasto': gasto})

def residente_view(request):
    # Aquí puedes obtener información relevante para los residentes, como los pagos pendientes
    # Vamos a suponer que los residentes tienen alguna información almacenada en el modelo Gasto o GastoComun
    gastos_pendientes = GastoComun.objects.filter(pagado=False)  # Filtrar gastos no pagados
    return render(request, 'residente.html', {'gastos_pendientes': gastos_pendientes})


def mark_paid_view(request, id):
    gasto = get_object_or_404(GastoComun, id=id)
    gasto.pagado = True
    gasto.save()
    return redirect('residente')  # Redirige de nuevo a la página de residente


def enviar_notificacion_pago(residente_email, periodo, monto):
    asunto = 'Notificación de Gasto Común Pendiente'
    mensaje = f'Hola, se ha generado un gasto común pendiente para el período {periodo}. El monto adeudado es ${monto}.'
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [residente_email])


def formulario_residente(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST.get('telefono', '')  # El teléfono es opcional
        direccion = request.POST['direccion']

        # Guardar la información del residente
        residente = Residente(nombre=nombre, email=email, telefono=telefono, direccion=direccion)
        residente.save()

        # Mensaje de éxito
        messages.success(request, 'La información del residente se ha guardado correctamente.')

        return redirect('pagina_de_exito')  # Redirigir a una página de éxito, por ejemplo

    return render(request, 'residente.html')


def pendientes(request):
    # Lógica para mostrar los gastos pendientes
    return render(request, 'pendientes.html')

def marcar_como_pagado(request):
    if request.method == 'POST':
        try:
            # Obtener los IDs de los gastos marcados como pagados
            gasto_ids = request.POST.getlist('gasto_ids[]')
            gastos = Gasto.objects.filter(id__in=gasto_ids)

            # Marcar todos los gastos como pagados
            for gasto in gastos:
                gasto.estado = 'pagado'  # Asegúrate de que 'estado' exista en tu modelo
                gasto.save()

            return JsonResponse({
                'success': True,
                'message': 'Gastos marcados como pagados',
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al marcar los gastos como pagados: {str(e)}',
            })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Método no permitido',
        })


def pagar_gasto_comun(request, gasto_id):
    gasto = GastoComun.objects.get(id=gasto_id)
    gasto.estado = 'pagado'
    gasto.notificado = True
    gasto.save()

    # Notificar al administrador por correo
    send_mail(
        'Pago Realizado',
        f'El gasto común "{gasto.descripcion}" ha sido pagado.',
        'tu_correo@example.com',  # Remitente
        ['admin@example.com'],   # Destinatario
        fail_silently=False,
    )

    messages.success(request, f"Gasto común '{gasto.descripcion}' pagado con éxito.")
    return redirect('residente_pago')



def registrar_residente(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST.get('telefono', '')
        direccion = request.POST['direccion']
        
        # Crear el residente en la base de datos
        Residente.objects.create(nombre=nombre, email=email, telefono=telefono, direccion=direccion)
        
        messages.success(request, "Residente registrado exitosamente.")
        return redirect('residente_pago')  # Redirigir a la página de pago

    return render(request, 'residente.html')



def residente_pago(request):
    gastos_pendientes = GastoComun.objects.filter(estado='pendiente')
    return render(request, 'residente_pago.html', {'gastos': gastos_pendientes})

def pagar_gasto_comun(request, gasto_id):
    gasto = GastoComun.objects.get(id=gasto_id)
    gasto.estado = 'pagado'
    gasto.save()

    messages.success(request, f"Gasto común '{gasto.descripcion}' pagado con éxito.")
    return redirect('residente_pago')



def marcar_gastos_pagados(request):
    if request.method == 'POST':
        try:
            # Obtener los IDs de los gastos a marcar como pagados desde el cuerpo de la solicitud
            gasto_ids = request.POST.getlist('gasto_ids')  # Asegúrate de que esto coincida con el nombre del campo en el cuerpo de la solicitud
            gastos = Gasto.objects.filter(id__in=gasto_ids)

            # Marcar los gastos como pagados
            for gasto in gastos:
                gasto.pagado = True  # Asume que tienes un campo "pagado" en tu modelo
                gasto.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)






def residente_form(request):
    if request.method == 'POST':
        # Aquí puedes manejar los datos del formulario
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST.get('telefono', '')  # Teléfono es opcional
        direccion = request.POST['direccion']
        
        # Lógica para guardar los datos o hacer algo más
        
        return render(request, 'residente_success.html', {'nombre': nombre})
    return render(request, 'residente_form.html')



def eliminar_gasto(request, gasto_id):
    try:
        gasto = GastoComun.objects.get(id=gasto_id)
        gasto.delete()  # Eliminar el gasto
        messages.success(request, "Gasto eliminado correctamente.")
    except GastoComun.DoesNotExist:
        messages.error(request, "El gasto no existe.")
    return redirect('generate_expenses')  # Redirigir a la página donde se muestran los gastos