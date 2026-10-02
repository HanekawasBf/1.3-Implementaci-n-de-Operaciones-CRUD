from django.test import TestCase
from django.urls import reverse
from .models import Producto


class ProductoTests(TestCase):

    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Teclado',
            descripcion='Teclado mecánico',
            precio='599.90',
            stock=10,
        )

    # MODELO
    def test_str_devuelve_nombre(self):
        self.assertEqual(str(self.producto), 'Teclado')

    # READ
    def test_lista_muestra_productos(self):
        respuesta = self.client.get(reverse('productos:lista'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Teclado')

    def test_detalle_muestra_producto(self):
        respuesta = self.client.get(reverse('productos:detalle', args=[self.producto.pk]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Teclado mecánico')

    def test_detalle_inexistente_da_404(self):
        respuesta = self.client.get(reverse('productos:detalle', args=[999]))
        self.assertEqual(respuesta.status_code, 404)

    # CREATE
    def test_crear_producto(self):
        datos = {'nombre': 'Mouse', 'descripcion': 'Inalámbrico', 'precio': '250.00', 'stock': 5}
        respuesta = self.client.post(reverse('productos:crear'), datos)
        self.assertRedirects(respuesta, reverse('productos:lista'))
        self.assertTrue(Producto.objects.filter(nombre='Mouse').exists())

    def test_crear_producto_invalido_no_guarda(self):
        datos = {'nombre': '', 'precio': 'abc', 'stock': 5}
        respuesta = self.client.post(reverse('productos:crear'), datos)
        self.assertEqual(respuesta.status_code, 200)  # vuelve a mostrar el form
        self.assertEqual(Producto.objects.count(), 1)

    # UPDATE
    def test_editar_producto(self):
        datos = {'nombre': 'Teclado RGB', 'descripcion': 'Con luces', 'precio': '699.00', 'stock': 8}
        respuesta = self.client.post(reverse('productos:editar', args=[self.producto.pk]), datos)
        self.assertRedirects(respuesta, reverse('productos:lista'))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Teclado RGB')
        self.assertEqual(self.producto.stock, 8)

    # DELETE
    def test_eliminar_producto(self):
        respuesta = self.client.post(reverse('productos:eliminar', args=[self.producto.pk]))
        self.assertRedirects(respuesta, reverse('productos:lista'))
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())