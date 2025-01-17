from typing import List
from .BaseDoc import BaseDoc
from random import sample


class CPF(BaseDoc):
    """Classe referente ao Cadastro de Pessoas Físicas (CPF)."""

    def __init__(self, repeated_digits: bool = False, custom_regex_pattern: str = None):
        """
        Na maioria das vezes, esse contrutor será usado sem parâmetros.
        
        Args:
            repeated_digits (bool, optional): 
                Usado para aceitar CPFs com números repetidos. Defaults to False.
            
            custom_regex_pattern (str, optional): 
                Usado na função validate para garantir que o CPF digitado esteja
                de acordo com a formatação correta, esse parâmetro deve ser um regex 
                válido ou None. Defaults to None.
        """

        if custom_regex_pattern is not None:
            super().__init__(custom_regex_pattern)
        else:
            super().__init__(r"[0-9]{3}[\.][0-9]{3}[\.][0-9]{3}[-][0-9]{2}")

        self.digits = list(range(10))
        self.repeated_digits = repeated_digits

    def validate(self, doc: str = '') -> bool:
        """Validar CPF."""
        if not self.check_formatting(doc):
            return False

        doc = list(self._only_digits(doc))

        if len(doc) != 11:
            return False

        if not self.repeated_digits and self._check_repeated_digits(doc):
            return False

        return self._generate_first_digit(doc) == doc[9] \
               and self._generate_second_digit(doc) == doc[10]

    def generate(self, mask: bool = False) -> str:
        """Gerar CPF."""
        # Os nove primeiros dígitos
        cpf = [str(sample(self.digits, 1)[0]) for i in range(9)]

        # Gerar os dígitos verificadores
        cpf.append(self._generate_first_digit(cpf))
        cpf.append(self._generate_second_digit(cpf))

        cpf = "".join(cpf)

        return self.mask(cpf) if mask else cpf

    def mask(self, doc: str = '') -> str:
        """Coloca a máscara de CPF na variável doc.

        Args:
            doc (str, optional): [ATENÇÃO] O cpf deve conter somente números.

        Returns:
            str: Cpf formatado com máscara
        """
        return "{}.{}.{}-{}".format(doc[:3], doc[3:6], doc[6:9], doc[-2:])

    def _generate_first_digit(self, doc: list) -> str:
        """Gerar o primeiro dígito verificador do CPF."""
        sum = 0

        for i in range(10, 1, -1):
            sum += int(doc[10 - i]) * i

        sum = (sum * 10) % 11

        if sum == 10:
            sum = 0

        return str(sum)

    def _generate_second_digit(self, doc: list) -> str:
        """Gerar o segundo dígito verificador do CPF."""
        sum = 0

        for i in range(11, 1, -1):
            sum += int(doc[11 - i]) * i

        sum = (sum * 10) % 11

        if sum == 10:
            sum = 0

        return str(sum)

    def _check_repeated_digits(self, doc: List[str]) -> bool:
        """Verifica se é um CPF com números repetidos.
        Exemplo: 111.111.111-11"""
        return len(set(doc)) == 1
