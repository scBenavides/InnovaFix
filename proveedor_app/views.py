from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.template.loader import render_to_string
from .forms import IngresoForm, ProductoForm, VentaForm, ProductoVentaFormSet, EquipoForm, UsuarioForm, ProveedorForm, RolForm, ClienteForm
from .models import (
    Ingreso, Producto, Venta, Cliente, Usuario, Proveedor,
    Rol, VistaIngresoInfo, VistaCompraVenta, VistaProcesoIngreso, Equipo, ProductoVenta
)
from .forms import RolForm, ProveedorForm, ClienteForm, UsuarioForm, IngresoForm, ProductoForm, VentaForm, EquipoForm
from collections import Counter
from django.db.models import Count
import json, datetime
from django.db import transaction
from django.contrib import messages


# -------------------------------
# HOME PAGE
# -------------------------------
def homepage(request):
    return render(request, 'homepage.html')

# -------------------------------
# HOME (login required)
# -------------------------------
@login_required
def inicio(request):
    return render(request, 'inicio.html')

# -------------------------------
# LOGIN PERSONALIZADO
# Redirect to start page if already authenticated
# -------------------------------
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('inicio')
        return super().dispatch(request, *args, **kwargs)

#----------------------------
# REPORT VIEWS #----------------------------

@login_required
def vista_ingreso_info_listar(request):
    datos = _get_ingreso_info_data()
    return render(request, 'proveedor/reportes/vista_ingreso_info.html', {'datos': datos})


def _get_ingreso_info_data():
    ingresos = Ingreso.objects.select_related('proveedorNit', 'usuCedula').all()
    return [
        {
            'ingresoId': ingreso.ingresoId,
            'ingresoValor': ingreso.ingresoValor,
            'ingresoCantidad': ingreso.ingresoCantidad,
            'nombre': ingreso.proveedorNit.nombre,
            'proveedorNombre': ingreso.proveedorNit.nombre,
            'direccion': ingreso.proveedorNit.direccion,
            'usuNombre': ingreso.usuCedula.usuNombre,
            'usuApellido': ingreso.usuCedula.usuApellido,
            'usuCorreo': ingreso.usuCedula.usuCorreo,
        }
        for ingreso in ingresos
    ]

# Export to Excel
def exportar_ingreso_info_excel(request):
    from django.http import HttpResponse
    import pandas as pd

    datos = _get_ingreso_info_data()

    # Build a pandas DataFrame
    data = {
        'ID': [dato['ingresoId'] for dato in datos],
        'Valor': [dato['ingresoValor'] for dato in datos],
        'Cantidad': [dato['ingresoCantidad'] for dato in datos],
        'Nombre': [dato['nombre'] for dato in datos],
        'Dirección': [dato['direccion'] for dato in datos],
        'Usuario Nombre': [dato['usuNombre'] for dato in datos],
        'Usuario Apellido': [dato['usuApellido'] for dato in datos],
        'Usuario Correo': [dato['usuCorreo'] for dato in datos],
    }
    df = pd.DataFrame(data)

    # Build the HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ingreso_info.xlsx"'

    # Export to Excel
    df.to_excel(response, index=False)

    return response

# Export to PDF
def exportar_ingreso_info_pdf(request):
    from django.http import HttpResponse
    from django.template.loader import get_template
    from xhtml2pdf import pisa

    datos = _get_ingreso_info_data()

    # Cargar la plantilla HTML
    template = get_template('proveedor/reportes/reporte_ingresoInfo_pdf.html')
    context = {
        'datos': datos,
    }
    html = template.render(context)

    # Build the HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ingreso_info.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    
    return response

@login_required
def vista_compra_venta_listar(request):
    datos = _get_compra_venta_data()
    return render(request, 'proveedor/reportes/vista_compra_venta.html', {'datos': datos})


def _get_compra_venta_data():
    items = ProductoVenta.objects.select_related('venta__cliente', 'producto').all()
    return [
        {
            'clienteNombre': item.venta.cliente.clienteNombre,
            'ventaId': item.venta.ventaId,
            'ventaCantidad': item.cantidad,
            'productoNombre': item.producto.productoNombre,
            'productoPrecioUnidad': item.precio_unitario,
        }
        for item in items
    ]

# Export to Excel
def exportar_compra_venta_excel(request):
    from django.http import HttpResponse
    import pandas as pd

    datos = _get_compra_venta_data()

    # Build a pandas DataFrame
    data = {
        'Cliente Nombre': [dato['clienteNombre'] for dato in datos],
        'ID Venta': [dato['ventaId'] for dato in datos],
        'Cantidad': [dato['ventaCantidad'] for dato in datos],
        'Producto Nombre': [dato['productoNombre'] for dato in datos],
        'Producto Precio Unidad': [dato['productoPrecioUnidad'] for dato in datos],
    }
    df = pd.DataFrame(data)

    # Build the HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="compra_venta.xlsx"'

    # Export to Excel
    df.to_excel(response, index=False)

    return response

# Export to PDF
def exportar_compra_venta_pdf(request):
    from django.http import HttpResponse
    from django.template.loader import get_template
    from xhtml2pdf import pisa

    datos = _get_compra_venta_data()

    # Cargar la plantilla HTML
    template = get_template('proveedor/reportes/reporte_compraVenta_pdf.html')
    context = {
        'datos': datos,
    }
    html = template.render(context)

    # Build the HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="compra_venta.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    
    return response

@login_required
def vista_proceso_ingreso_listar(request):
    datos = _get_proceso_ingreso_data()
    return render(request, 'proveedor/reportes/vista_proceso_ingreso.html', {'datos': datos})


def _get_proceso_ingreso_data():
    ingresos = Ingreso.objects.select_related('proveedorNit', 'usuCedula').all()
    return [
        {
            'usuNombre': ingreso.usuCedula.usuNombre,
            'ingresoId': ingreso.ingresoId,
            'ingresoValor': ingreso.ingresoValor,
            'nombre': ingreso.proveedorNit.nombre,
            'proveedorNombre': ingreso.proveedorNit.nombre,
        }
        for ingreso in ingresos
    ]

# Export to Excel
def exportar_proceso_ingreso_excel(request):
    from django.http import HttpResponse
    import pandas as pd

    datos = _get_proceso_ingreso_data()

    # Build a pandas DataFrame
    data = {
        'Usuario Nombre': [dato['usuNombre'] for dato in datos],
        'ID Ingreso': [dato['ingresoId'] for dato in datos],
        'Valor': [dato['ingresoValor'] for dato in datos],
        'Nombre': [dato['nombre'] for dato in datos],
    }
    df = pd.DataFrame(data)

    # Build the HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="proceso_ingreso.xlsx"'

    # Export to Excel
    df.to_excel(response, index=False)

    return response

# Export to PDF
def exportar_proceso_ingreso_pdf(request):
    from django.http import HttpResponse
    from django.template.loader import get_template
    from xhtml2pdf import pisa

    datos = _get_proceso_ingreso_data()

    # Cargar la plantilla HTML
    template = get_template('proveedor/reportes/reporte_procesoIngreso_pdf.html')
    context = {
        'datos': datos,
    }
    html = template.render(context)

    # Build the HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="proceso_ingreso.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    
    return response

#----------------------------
# REGISTRATION VIEW
#----------------------------

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Or redirect anywhere you prefer after registration
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

#----------------------------
# SUPPLIER VIEW
#-----------------------------

@login_required
def proveedor_listar(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor agregado correctamente.", extra_tags='agregado')
            return redirect('proveedor_listar')
    else:
        form = ProveedorForm()

    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor/proveedor/proveedor.html', {
        'form': form,
        'proveedores': proveedores
    })

@login_required
def proveedor_editar(request, proveedorNit):
    proveedor = get_object_or_404(Proveedor, proveedorNit=proveedorNit)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor_listar')  # Redirect to the supplier list
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedor/proveedor/proveedor_editar.html', {'form': form, 'proveedor':proveedor})



@login_required
@require_POST
def proveedor_eliminar(request, id):
    proveedor = get_object_or_404(Proveedor, proveedorNit=id)
    proveedor.delete()
    messages.success(request, "Proveedor eliminado correctamente.", extra_tags='eliminado')
    return redirect('proveedor_listar')

#----------------------------
# ROLE VIEW
#-----------------------------

@login_required
def rol_listar(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol agregado correctamente.", extra_tags='agregado')
            return redirect('rol_listar')
    else:
        form = RolForm()

    roles = Rol.objects.all()
    return render(request, 'proveedor/rol/rol.html', {
        'form': form,
        'roles': roles
    })

@login_required
@require_POST
def rol_eliminar(request, rolId):
    rol = get_object_or_404(Rol, rolId=rolId)
    rol.delete()
    messages.success(request, "Rol eliminado correctamente.", extra_tags='eliminado')
    return redirect('rol_listar')

#----------------------------
# CLIENT VIEW
#-----------------------------

@login_required
def cliente_listar(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            cliente_obj = form.save(commit=False)
            cliente_obj.cliente = request.user
            cliente_obj.save()
            messages.success(request, "Cliente agregado correctamente.", extra_tags='agregado')
            return redirect('cliente_listar')
    else:
        form = ClienteForm()

    clientes = Cliente.objects.all()
    return render(request, 'proveedor/cliente/cliente.html', {
        'form': form,
        'clientes': clientes
    })

@login_required
@require_POST
def cliente_eliminar(request, clienteCedula):
    cliente = get_object_or_404(Cliente, clienteCedula=clienteCedula)
    cliente.delete()
    messages.success(request, "Cliente eliminado correctamente.", extra_tags='eliminado')
    return redirect('cliente_listar')

@login_required
def cliente_editar(request, clienteCedula):
    cliente = get_object_or_404(Cliente, clienteCedula=clienteCedula)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_listar')  # Redirect to the client list
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'proveedor/cliente/cliente_editar.html', {'form': form, 'cliente':cliente})

#----------------------------
# USER VIEW
#-----------------------------

@login_required
def usuario_listar(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            usuario_obj = form.save(commit=False)
            usuario_obj.usuario = request.user
            usuario_obj.save()
            messages.success(request, "Usuario agregado correctamente.", extra_tags='agregado')
            return redirect('usuario_listar')
    else:
        form = UsuarioForm()

    usuarios = Usuario.objects.all()
    usuarios_django = User.objects.all()
    usuarios_count = usuarios.count()
    roles = Rol.objects.all()
    labels = [rol.rolNombre for rol in roles]
    data = [usuarios.filter(rolId=rol).count() for rol in roles]

    return render(request, 'proveedor/usuario/usuario.html', {
        'form': form,
        'usuarios': usuarios,
        'usuarios_django': usuarios_django,
        'usuarios_count': usuarios_count,
        'roles_labels': labels,
        'roles_data': data,
    })


@login_required
@require_POST
def usuario_eliminar(request, usuCedula):
    usuario = get_object_or_404(Usuario, usuCedula=usuCedula)
    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.", extra_tags='eliminado')
    return redirect('usuario_listar')

@login_required
def usuario_editar(request, usuCedula):
    usuario = get_object_or_404(Usuario, usuCedula=usuCedula)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuario_listar')  # Redirect to the user list
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'proveedor/usuario/usuario_editar.html', {'form': form, 'usuario':usuario})

# ==============================
# LIST INTAKES
# ==============================
@login_required
def ingreso_listar(request):
    ProductoFormSet = inlineformset_factory(Ingreso, Producto, form=ProductoForm, extra=1, can_delete=True)
    form = IngresoForm()
    formset = ProductoFormSet()

    ingresos = Ingreso.objects.all().select_related('proveedorNit', 'usuCedula')

    return render(request, 'proveedor/ingreso/ingreso.html', {
        'ingresos': ingresos,
        'form': form,
        'formset': formset
    })


# ==============================
# CREATE INTAKE + PRODUCTS
# ==============================
@login_required
def ingreso_crear(request):
    ProductoFormSet = inlineformset_factory(Ingreso, Producto, form=ProductoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)
            formset = ProductoFormSet(request.POST, instance=ingreso)

            if formset.is_valid():
                ingreso.save()
                formset.save()
                messages.success(request, "Ingreso agregado correctamente.", extra_tags='agregado')
                return redirect('ingreso_listar')
            else:
                messages.error(request, "Error al registrar los productos.")
        else:
            messages.error(request, "Error al registrar el ingreso.")
            formset = ProductoFormSet(request.POST)
    else:
        form = IngresoForm()
        formset = ProductoFormSet()

    return render(request, 'proveedor/ingreso/ingreso_form.html', {
        'form': form,
        'formset': formset
    })


# ==============================
# EDIT INTAKE + PRODUCTS
# ==============================
@login_required
def ingreso_editar(request, id):
    ingreso = get_object_or_404(Ingreso, ingresoId=id)
    ProductoFormSet = inlineformset_factory(Ingreso, Producto, form=ProductoForm, extra=0, can_delete=True)

    if request.method == "POST":
        form = IngresoForm(request.POST, instance=ingreso)
        formset = ProductoFormSet(request.POST, instance=ingreso)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Ingreso actualizado correctamente.", extra_tags='agregado')
            return redirect("ingreso_listar")
        else:
            messages.error(request, "Error al actualizar el ingreso o los productos.")
    else:
        form = IngresoForm(instance=ingreso)
        formset = ProductoFormSet(instance=ingreso)

    return render(request, 'proveedor/ingreso/ingreso_editar.html', {
        "form": form,
        "formset": formset,
    })


# ==============================
# DELETE INTAKE
# ==============================
@login_required
def ingreso_eliminar(request, id):
    ingreso = get_object_or_404(Ingreso, pk=id)
    if request.method == 'POST':
        ingreso.delete()
        messages.success(request, "Ingreso eliminado correctamente.", extra_tags='eliminado')
        return redirect('ingreso_listar')
    return redirect('ingreso_listar')


# ==============================
# EXPORT INTAKES TO EXCEL
# ==============================
@login_required
def exportar_ingresos_excel(request):
    from django.http import HttpResponse
    import pandas as pd

    ingresos = Ingreso.objects.select_related('proveedorNit', 'usuCedula').all()

    data = {
        'ID': [ingreso.ingresoId for ingreso in ingresos],
        'Proveedor': [ingreso.proveedorNit.nombre for ingreso in ingresos],
        'Usuario': [ingreso.usuCedula.usuNombre for ingreso in ingresos],
        'Cantidad': [ingreso.ingresoCantidad for ingreso in ingresos],
        'Valor': [ingreso.ingresoValor for ingreso in ingresos],
    }
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ingresos.xlsx"'
    df.to_excel(response, index=False)

    return response


# ==============================
# EXPORT INTAKES TO PDF
# ==============================
@login_required
def exportar_ingresos_pdf(request):
    from django.http import HttpResponse
    from django.template.loader import get_template
    from xhtml2pdf import pisa

    ingresos = Ingreso.objects.select_related('proveedorNit', 'usuCedula').all()
    template = get_template('proveedor/ingreso/ingreso_pdf.html')
    context = {'ingresos': ingresos}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ingresos.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

#----------------------------
# PRODUCT VIEW
#-----------------------------

# Automatic productId generator
def generar_producto_id():
    ultimo = Producto.objects.order_by('-productoId').first()
    if ultimo and str(ultimo.productoId).startswith('PRD'):
        try:
            numero = int(str(ultimo.productoId).replace('PRD', '')) + 1
        except ValueError:
            numero = 1
    else:
        numero = 1
    return f"PRD{numero:03d}"

@login_required
def producto_listar(request):
    error_id = False

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto_obj = form.save(commit=False)
            producto_obj.productoId = generar_producto_id()

            # Check whether a product with that ID already exists
            if Producto.objects.filter(productoId=producto_obj.productoId).exists():
                error_id = True
                messages.error(request, "❌ El ID del producto ya existe.")
            else:
                producto_obj.save()
                messages.success(request, "Producto registrado exitosamente.", extra_tags='agregado')
                return redirect('producto_listar')
        else:
            messages.error(request, "❌ Formulario inválido. Revisa los campos.")
    else:
        form = ProductoForm()

    productos = Producto.objects.all()
    return render(request, 'proveedor/producto/producto.html', {
        'form': form,
        'productos': productos,
        'error_id': error_id
    })

#----------------------------
# DELETE PRODUCT
#-----------------------------
@login_required
@require_POST
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, productoId=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.", extra_tags='eliminado')
    return redirect('producto_listar')

#----------------------------
# SALES LIST VIEW
#-----------------------------

@login_required
def venta_listar(request):
    ventas = Venta.objects.all().order_by('-fecha')  # Descending order by date
    form = VentaForm()
    formset = ProductoVentaFormSet()
    productos = Producto.objects.all()

    response = render(request, 'venta/venta.html', {
        'ventas': ventas,
        'form': form,
        'formset': formset,
        'productos': productos
    })
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

#----------------------------
# SALES CREATION VIEW
#-----------------------------

@login_required
def registrar_venta(request):
    if request.method == "POST":
        venta_form = VentaForm(request.POST)
        formset = ProductoVentaFormSet(request.POST)

        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.total = 0
            venta.save()

            total = 0
            productos = formset.save(commit=False)
            for p in productos:
                p.venta = venta
                p.precio_unitario = p.producto.productoPrecioUnidad
                p.subtotal = p.cantidad * p.precio_unitario
                total += p.subtotal
                p.save()

                # Update product stock
                p.producto.productoCantidad -= p.cantidad
                p.producto.save()

            venta.total = total
            venta.save()

            messages.success(request, "Venta registrada con éxito.", extra_tags='agregado')
            return redirect("venta_listar")
        else:
            messages.error(request, "Error al registrar la venta. Revisa los campos.")
    else:
        venta_form = VentaForm()
        formset = ProductoVentaFormSet()

    ventas = Venta.objects.all().order_by('-fecha')
    productos = Producto.objects.all()

    return render(request, "venta/venta.html", {
        "ventas": ventas,
        "form": venta_form,
        "formset": formset,
        "productos": productos
    })

#----------------------------
# SALES DELETE VIEW
#-----------------------------

@login_required
@require_POST
def venta_eliminar(request, ventaId):
    venta = get_object_or_404(Venta, ventaId=ventaId)
    venta.delete()
    messages.success(request, "Venta eliminada correctamente.", extra_tags='eliminado')
    return redirect('venta_listar')

#----------------------------
# EXPORT TO EXCEL
#-----------------------------

def exportar_ventas_excel(request):
    from django.http import HttpResponse
    import pandas as pd

    ventas = Venta.objects.select_related('productoId', 'clienteCedula', 'usuCedula').all()

    data = {
        'ID Venta': [venta.ventaId for venta in ventas],
        'Cantidad': [venta.ventaCantidad for venta in ventas],
        'Tipo Producto': [venta.ventaTipoProducto for venta in ventas],
        'Método de Pago': [venta.ventaMetodoPago for venta in ventas],
        'Precio Total': [venta.ventaPrecio for venta in ventas],
        'Producto': [str(venta.productoId) for venta in ventas],
        'Cliente': [str(venta.clienteCedula) for venta in ventas],
        'Usuario': [str(venta.usuCedula) for venta in ventas],
    }
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ventas.xlsx"'
    df.to_excel(response, index=False)

    return response


#----------------------------
# EXPORT TO PDF
#-----------------------------

def exportar_ventas_pdf(request):
    from django.http import HttpResponse
    from django.template.loader import get_template
    from xhtml2pdf import pisa

    ventas = Venta.objects.select_related('productoId', 'clienteCedula', 'usuCedula').all()
    template = get_template('proveedor/venta/venta_pdf.html')
    context = {'ventas': ventas}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ventas.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response


#----------------------------
# EQUIPMENT VIEW
#-----------------------------

@login_required
def equipo_listar(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipo agregado correctamente.", extra_tags='agregado')
            return redirect('equipo_listar')
    else:
        form = EquipoForm()

    equipos = Equipo.objects.all()
    equipos_django = User.objects.all()
    equipos_count = equipos.count()

    estados = equipos.values_list('equipoEstado', flat=True)
    contador_estados = Counter(estados)
    estados_labels = list(contador_estados.keys())
    estados_data = list(contador_estados.values())

    colores_por_estado = {
        "Pendiente": "rgba(255, 99, 132, 0.7)",     # red
        "En Proceso": "rgba(255, 206, 86, 0.7)",   # yellow
        "Completado": "rgba(75, 192, 192, 0.7)",   # green
    }

    colores_barras = [colores_por_estado.get(estado, "rgba(201, 203, 207, 0.7)") for estado in estados_labels]

    return render(request, 'proveedor/equipos/equipos.html', {
        'form': form,
        'equipos': equipos,
        'equipos_count': equipos_count,
        'equipos_django': equipos_django,
        'estados_labels': json.dumps(estados_labels),
        'estados_data': json.dumps(estados_data),
        'colores_barras': json.dumps(colores_barras),
    })

@login_required
@require_POST
def equipo_eliminar(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    equipo.delete()
    messages.success(request, "Equipo eliminado correctamente.", extra_tags='eliminado')
    return redirect('equipo_listar')
@login_required
def equipo_editar(request, equipoId):
    equipo = get_object_or_404(Equipo, equipoId=equipoId)
    
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('equipo_listar')  # Redirect to the equipment list
    else:
        form = EquipoForm(instance=equipo)
    return render(request, 'proveedor/equipos/equipo_editar.html', {'form': form, 'equipo':equipo})
