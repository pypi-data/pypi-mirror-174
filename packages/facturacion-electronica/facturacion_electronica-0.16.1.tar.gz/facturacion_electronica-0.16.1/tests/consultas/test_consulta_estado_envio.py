# -#- coding: utf-8 -#-
from facturacion_electronica import facturacion_electronica as fe
from facturacion_electronica.firma import Firma
import json
from lxml import etree
import unittest


class TestEjemploEstadoEnvio39(unittest.TestCase):
    """
    Test Consulta Envío
    """
    def test_consulta_certificado_vencido(self):
        """
        Test Consulta de estado  con certificado vencido
        """
        print("Se inicia test consulta estado envío")
        f = open("facturacion_electronica/ejemplos/ejemplo_estado_envio.json")
        txt_json = f.read()
        f.close()
        ejemplo_33 = json.loads(txt_json)
        firma_electronica = ejemplo_33['firma_electronica'].copy()
        result = fe.consulta_estado_envio(ejemplo_33)
        self.assertEqual(result.get('glosa', ''), 'TOKEN NO EXISTE')

if __name__ == '__main__':
    unittest.main()
