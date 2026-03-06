from django import forms
from .models import Cliente, Usuario, Proveedor, Ingreso, Producto, Venta, Rol, Equipo, ProductoVenta
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'proveedorNit','telefono','direccion' ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'proveedorNit': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del Proveedor',
            'proveedorNit': 'NIT del Proveedor',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }
        help_texts = {
            'nombre': 'Ingrese el nombre del proveedor.',
            'proveedorNit': 'Ingrese el NIT del proveedor.',
            'telefono': 'Ingrese el número de teléfono del proveedor.',
            'direccion': 'Ingrese la dirección del proveedor.',
        }
        error_messages = {
            'nombre': {
                'required': 'El nombre del proveedor es obligatorio.',
            },
            'proveedorNit': {
                'required': 'El NIT es obligatorio.',
                'unique': 'Este NIT ya está registrado.',
            },
            'telefono': {
                'required': 'El teléfono es obligatorio.',
            },
            'direccion': {
                'required': 'La dirección es obligatoria.',
        },
}


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        # Fields in the desired order
        fields = ['usuCedula', 'proveedorNit', 'ingresoValor', 'ingresoCantidad']
        # More user-friendly labels
        labels = {
            'usuCedula': 'Nombre Usuario',
            'proveedorNit': 'Proveedor',
            'ingresoValor': 'Valor',
            'ingresoCantidad': 'Cantidad',
        }
        widgets = {
            'usuCedula': forms.Select(attrs={'class': 'form-control'}),
            'proveedorNit': forms.Select(attrs={'class': 'form-control'}),
            'ingresoValor': forms.NumberInput(attrs={'class': 'form-control'}),
            'ingresoCantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['clienteCedula', 'clienteNombre', 'clienteApellido', 'clienteUsuario',
        'clienteContrasena', 'clienteFoto', 'clienteCorreo', 'clienteTelefono',
        'clienteDireccion']
        widgets = {
            'clienteCedula': forms.TextInput(attrs={'class': 'form-control'}),
            'clienteNombre': forms.TextInput(attrs={'class': 'form-control'}),
            'clienteApellido': forms.TextInput(attrs={'class': 'form-control'}),
            'clienteUsuario': forms.TextInput(attrs={'class': 'form-control'}),
            'clienteContrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
            'clienteFoto': forms.FileInput(attrs={'class': 'form-control'}),
            'clienteCorreo': forms.EmailInput(attrs={'class': 'form-control'}),
            'clienteTelefono': forms.TextInput(attrs={'class': 'form-control'}),
            'clienteDireccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'clienteCedula': 'Cedula',
            'clienteNombre': 'Nombre',
            'clienteApellido': 'Apellido',
            'clienteUsuario': 'Usuario',
            'clienteContrasena': 'Contraseña',
            'clienteFoto': 'Foto de perfil',
            'clienteCorreo': 'Correo electrónico',
            'clienteTelefono': 'Número de teléfono',
            'clienteDireccion': 'Dirección',
        }
        error_messages = {
            'clienteCedula': {
                'required': 'La cédula es obligatoria.',
                'unique': 'Esta cédula ya está registrada.',
            },
            'clienteCorreo': {
                'required': 'El correo electrónico es obligatorio.',
                'invalid': 'Ingrese un correo electrónico válido.',
                'unique': 'Este correo ya está registrado.',
            },
            'clienteUsuario': {
                'unique': 'Este nombre de usuario ya está en uso.',
            },
            'clienteTelefono': {
                'required': 'El número de teléfono es obligatorio.',
            },
            'clienteDireccion': {
                'required': 'La dirección es obligatoria.',
            },
            'clienteContrasena': {
                'required': 'La contraseña es obligatoria.',
            },
            'clienteNombre': {
                'required': 'El nombre es obligatorio.',
            },
            'clienteApellido': {
                'required': 'El apellido es obligatorio.',
            },
            'clienteUsuario': {
                'required': 'El usuario es obligatorio.',
        },
}


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'usuCedula', 'usuUsuario', 'usuNombre', 'usuApellido', 'rolId',
            'usuContrasena', 'usuCorreo', 'usuTelefono',
            'usuDireccion', 'usuFoto'
        ]
        widgets = {
            'usuCedula': forms.TextInput(attrs={'class': 'form-control'}),
            'usuUsuario': forms.TextInput(attrs={'class': 'form-control'}),
            'usuNombre': forms.TextInput(attrs={'class': 'form-control'}),
            'usuApellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rolId': forms.Select(attrs={'class': 'form-control'}),
            'usuContrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
            'usuCorreo': forms.EmailInput(attrs={'class': 'form-control'}),
            'usuTelefono': forms.TextInput(attrs={'class': 'form-control'}),
            'usuDireccion': forms.TextInput(attrs={'class': 'form-control'}),
            'usuFoto': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'usuCedula': 'Cédula',
            'usuUsuario': 'Nombre de Usuario',
            'usuNombre': 'Nombre',
            'usuApellido': 'Apellido',
            'rolId': 'Rol',
            'usuContrasena': 'Contraseña',
            'usuCorreo': 'Correo Electrónico',
            'usuTelefono': 'Teléfono',
            'usuDireccion': 'Dirección',
            'usuFoto': 'Foto de Perfil (URL o archivo)',
        }
        error_messages = {
            'usuCedula': {
                'required': 'La cédula es obligatoria.',
                'unique': 'Esta cédula ya está registrada.',
            },
            'usuCorreo': {
                'required': 'El correo electrónico es obligatorio.',
                'invalid': 'Ingrese un correo electrónico válido.',
                'unique': 'Este correo ya está registrado.',
            },
            'usuUsuario': {
                'unique': 'Este nombre de usuario ya está en uso.',
                'required': 'El usuario es obligatorio.',
            },
            'usuTelefono': {
                'required': 'El número de teléfono es obligatorio.',
            },
            'usuDireccion': {
                'required': 'La dirección es obligatoria.',
            },
            'usuContrasena': {
                'required': 'La contraseña es obligatoria.',
            },
            'usuNombre': {
                'required': 'El nombre es obligatorio.',
            },
            'usuApellido': {
                'required': 'El apellido es obligatorio.',
         },
}

class RolForm (forms.ModelForm):
    class Meta:
        model = Rol
        fields = [ 
            'rolNombre', 'rolDescripcion',
        ]
        widgets = {
            'rolNombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rolDescripcion': forms.Textarea(attrs={'class': 'form-control'})
            }
        labels = {
            'rolNombre': 'Nombre del Rol',
            'rolDescripcion': 'Descripción del Rol',
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ['productoId', 'ingreso']
        labels = {
            'productoNombre': 'Nombre del Producto',
            'productoPrecioUnidad': 'Precio Unitario',
            'productoCantidad': 'Cantidad',
            'productoDescripcion': 'Descripción',
        }
        widgets = {
            'productoNombre': forms.TextInput(attrs={'class': 'form-control'}),
            'productoPrecioUnidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'productoCantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'productoDescripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']
        labels = {'cliente': 'Cliente'}
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductoVentaForm(forms.ModelForm):
    class Meta:
        model = ProductoVenta
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input'}),
            'precio_unitario': forms.HiddenInput(),
            'subtotal': forms.HiddenInput(),
        }
        
    class Meta:
        model = ProductoVenta
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
        }
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input'}),
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Show only products with available stock
        self.fields['producto'].queryset = Producto.objects.filter(productoCantidad__gt=0)
        self.fields['producto'].label_from_instance = lambda obj: f"{obj.productoNombre} (Stock: {obj.productoCantidad}, Precio: ${obj.productoPrecioUnidad})"

# Inline formset to manage multiple ProductoVenta rows linked to a Venta
ProductoVentaFormSet = inlineformset_factory(
    Venta,
    ProductoVenta,
    form=ProductoVentaForm,
    extra=1,
    can_delete=True
)

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['equipoRef', 'equipoNovedad', 'clienteNombre', 'usuNombre', 'equipoEstado']
        labels = {
            'equipoRef': 'Referencia del Equipo',
            'equipoNovedad': 'Novedad del Equipo',
            'clienteNombre': 'Cliente',
            'usuNombre': 'Usuario',
            'equipoEstado': 'Estado',
        }
        widgets = {
            'equipoRef': forms.TextInput(attrs={'class': 'form-control'}),
            'equipoNovedad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'clienteNombre': forms.Select(attrs={'class': 'form-control'}),
            'usuNombre': forms.Select(attrs={'class': 'form-control'}),
            'equipoEstado': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'equipoRef': {
                'required': 'La referencia del equipo es obligatoria.',
            },
            'equipoNovedad': {
                'required': 'La novedad del equipo es obligatoria.',
            },
            'clienteNombre': {
                'required': 'El cliente es obligatorio.',
            },
            'usuNombre': {
                'required': 'El usuario es obligatorio.',
            },
            'equipoEstado': {
                'required': 'El estado del equipo es obligatorio.',
        },
}
        

# Formset for products associated with an Ingreso
ProductoFormSet = inlineformset_factory(
    Ingreso,
    Producto,
    form=ProductoForm,
    extra=3,  # Number of additional empty forms  
    can_delete=True
)