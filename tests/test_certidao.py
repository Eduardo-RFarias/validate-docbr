import unittest
import validate_docbr as docbr


class TestCertidao(unittest.TestCase):
    """Testar a classe Certidao."""

    def setUp(self):
        """Inicia novo objeto em todo os testes."""
        self.certidao = docbr.Certidao()

    def test_generate_validate(self):
        """Verifica os métodos de geração e validação de documento."""
        # generate_list
        certidoes = self.certidao.generate_list(5000) \
                    + self.certidao.generate_list(5000, mask=True)
        self.assertIsInstance(certidoes, list)
        self.assertTrue(len(certidoes) == 10000)

        # validate_list
        certidoes_validates = self.certidao.validate_list(certidoes)
        self.assertTrue(sum(certidoes_validates) == 10000)

    def test_mask(self):
        """Verifica se o método mask funciona corretamente."""

        masked_certidao = self.certidao.mask(
            '10453901552013100012021000012321')
        self.assertEqual(
            masked_certidao, '104539.01.55.2013.1.00012.021.0000123-21')

    def test_special_case(self):
        """ Verifica os casos especiais de Certidão """
        cases = [
            ('3467875434578764345789654', False),
            ('AAAAAAAAAAA', False),
            ('', False),
            ('27610201552018226521370659786633', True),
            ('27610201552018226521370659786630', False),
        ]
        for certidao, is_valid in cases:
            self.assertEqual(self.certidao.validate(certidao), is_valid)
