from django.urls import path
from . import views
from django.http import HttpResponse
from django.urls import path 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Registration
    path('registro/', views.registro, name='registro'),

    # Home
    path('inicio/', views.inicio, name='inicio'),
        
    # Supplier
    path('proveedores/', views.proveedor_listar, name='proveedor_listar'),
    path('proveedor/eliminar/<str:id>/', views.proveedor_eliminar, name='proveedor_eliminar'),
    path('proveedores/<str:proveedorNit>/editar/', views.proveedor_editar, name='proveedor_editar'),

    # User
    path('usuarios/', views.usuario_listar, name='usuario_listar'),
    path('usuario/eliminar/<str:usuCedula>/', views.usuario_eliminar, name='usuario_eliminar'),
    path('usuarios/<str:usuCedula>/editar/', views.usuario_editar, name='usuario_editar'),

    # Intake
    path('ingresos/', views.ingreso_listar, name='ingreso_listar'),
    path('ingreso/editar/<int:id>/', views.ingreso_editar, name='ingreso_editar'),
    path('ingreso/crear/', views.ingreso_crear, name='ingreso_crear'),
    path('ingreso/eliminar/<int:id>/', views.ingreso_eliminar, name='ingreso_eliminar'),
    path('exportar_ingresos_excel/', views.exportar_ingresos_excel, name='exportar_ingresos_excel'),
    path('exportar_ingresos_pdf/', views.exportar_ingresos_pdf, name='exportar_ingresos_pdf'),
    
    # PRODUCTOS
    path('productos/', views.producto_listar, name='producto_listar'),
    path('producto/eliminar/<str:producto_id>/', views.producto_eliminar, name='producto_eliminar'),


    # ROLES
    path('roles/', views.rol_listar, name='rol_listar'),
    path('rol/eliminar/<int:rolId>/', views.rol_eliminar, name='rol_eliminar'),

    # VENTAS
    path('venta/crear/', views.registrar_venta, name='venta_crear'),
    path('venta/', views.venta_listar, name='venta_listar'),
    path('venta/eliminar/<int:ventaId>/', views.venta_eliminar, name='venta_eliminar'),
    path('exportar_ventas_excel/', views.exportar_ventas_excel, name='exportar_ventas_excel'),
    path('exportar_ventas_pdf/', views.exportar_ventas_pdf, name='exportar_ventas_pdf'),

    # Client
    path('clientes/', views.cliente_listar, name='cliente_listar'),
    path('cliente/eliminar/<str:clienteCedula>/', views.cliente_eliminar, name='cliente_eliminar'),
    path('clientes/<str:clienteCedula>/editar/', views.cliente_editar, name='cliente_editar'),

    # Equipment
    path('equipos/', views.equipo_listar, name='equipo_listar'),
    path('equipo/eliminar/<int:pk>/', views.equipo_eliminar, name='equipo_eliminar'),
    path('equipos/<int:equipoId>/editar/', views.equipo_editar, name='equipo_editar'),

    # Report views
    path('reportes/vista_ingreso_info/', views.vista_ingreso_info_listar, name='vista_ingreso_info_listar'),
    path('reportes/vista_compra_venta/', views.vista_compra_venta_listar, name='vista_compra_venta_listar'),
    path('reportes/vista_proceso_ingreso/', views.vista_proceso_ingreso_listar, name='vista_proceso_ingreso_listar'),
    path('exportar_ingreso_info_excel/', views.exportar_ingreso_info_excel, name='exportar_ingreso_info_excel'),
    path('exportar_ingreso_info_pdf/', views.exportar_ingreso_info_pdf, name='exportar_ingreso_info_pdf'),
    path('exportar_compra_venta_excel/', views.exportar_compra_venta_excel, name='exportar_compra_venta_excel'),
    path('exportar_compra_venta_pdf/', views.exportar_compra_venta_pdf, name='exportar_compra_venta_pdf'),
    path('exportar_proceso_ingreso_excel/', views.exportar_proceso_ingreso_excel, name='exportar_proceso_ingreso_excel'),
    path('exportar_proceso_ingreso_pdf/', views.exportar_proceso_ingreso_pdf, name='exportar_proceso_ingreso_pdf'),

]

# Media files configuration (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
