import unittest

from xlsx_to_dict import xlsx_to_dict


class TestXlsxToDict(unittest.TestCase):
    def test_xlsx_to_dict(self):
        expected = [
            {"nome": "Fulano", "idade": 42, "patrimonio": 42, "data_nascimento": "01/01/01"},
            {"nome": "Ciclano", "idade": 84, "patrimonio": 84, "data_nascimento": "12/12/12"},
        ]
        self.assertEqual(expected, xlsx_to_dict('test.xlsx'))
