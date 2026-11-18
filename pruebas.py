"""Pruebas automáticas básicas del modelo y servicios. Ejecutar: python pruebas.py"""
import unittest
from enums import Rol, FormaPago, Estado
from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio
from excepciones import DuplicadoError, StockInsuficienteError, OperacionNoPermitidaError

class FoodStoreTests(unittest.TestCase):
    def setUp(self):
        self.cs=CategoriaServicio(); self.ps=ProductoServicio(); self.us=UsuarioServicio(); self.peds=PedidoServicio()
        self.cat=self.cs.crear("Comidas","Comidas principales")
        self.prod=self.ps.crear("Hamburguesa",1000,"Clásica",5,"",True,self.cat)
        self.user=self.us.crear("Juan","Pérez","juan@mail.com","123","clave123",Rol.USUARIO)

    def test_categoria_duplicada(self):
        with self.assertRaises(DuplicadoError): self.cs.crear("COMIDAS","Otra")

    def test_pedido_descuenta_stock_y_calcula_total(self):
        pedido=self.peds.crear(self.user,FormaPago.EFECTIVO,[(self.prod,2)])
        self.assertEqual(pedido.total,2000)
        self.assertEqual(self.prod.stock,3)

    def test_stock_insuficiente_no_crea_pedido_ni_descuenta(self):
        with self.assertRaises(StockInsuficienteError): self.peds.crear(self.user,FormaPago.EFECTIVO,[(self.prod,8)])
        self.assertEqual(self.prod.stock,5)
        self.assertEqual(len(self.peds.listar()),0)

    def test_cancelar_devuelve_stock(self):
        pedido=self.peds.crear(self.user,FormaPago.EFECTIVO,[(self.prod,2)])
        self.peds.actualizar_estado(pedido.id,Estado.CANCELADO)
        self.assertEqual(self.prod.stock,5)

    def test_transicion_invalida(self):
        pedido=self.peds.crear(self.user,FormaPago.EFECTIVO,[(self.prod,1)])
        with self.assertRaises(OperacionNoPermitidaError): self.peds.actualizar_estado(pedido.id,Estado.TERMINADO)

    def test_autenticacion(self):
        self.assertEqual(self.us.autenticar("juan@mail.com","clave123"),self.user)

if __name__ == "__main__":
    unittest.main(verbosity=2)
