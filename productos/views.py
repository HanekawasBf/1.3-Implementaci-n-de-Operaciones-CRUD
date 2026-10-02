from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm


# READ (lista)
def lista(request):
    productos = Producto.objects.all().order_by('-creado')
    return render(request, 'productos/lista.html', {'productos': productos})


# READ (detalle)
def detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto})


# CREATE
def crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos:lista')
    else:
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Nuevo producto'})


# UPDATE
def editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos:lista')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Editar producto'})


# DELETE
def eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:lista')
    return render(request, 'productos/eliminar.html', {'producto': producto})