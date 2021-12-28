from abc import ABC
from typing import List
import re


class BaseDoc(ABC):
    """Classe base para todas as classes referentes a documentos."""

    def __init__(self, regex_pattern: str):
        """Construtor usado para compilar o Regex pattern.

        Args:
            regex_pattern (str): 
                Um regex pattern que será usado para validar a entrada do método validate.
        """
        super().__init__()
        self.regex = re.compile(regex_pattern)

    def validate(self, doc: str = '') -> bool:
        """Método para validar o documento desejado."""
        pass

    def validate_list(self, docs: List[str]) -> List[bool]:
        """Método para validar uma lista de documentos desejado."""
        return [self.validate(doc) for doc in docs]

    def generate(self, mask: bool = False) -> str:
        """Método para gerar um documento válido."""
        pass

    def generate_list(self, n: int = 1, mask: bool = False, repeat: bool = False) -> list:
        """Gerar uma lista do mesmo documento."""
        doc_list = []

        if n <= 0:
            return doc_list

        for i in range(n):
            doc_list.append(self.generate(mask))

        while not repeat:
            doc_set = set(doc_list)
            unique_values = len(doc_set)

            if unique_values < n:
                doc_list = list(doc_set) + self.generate_list((n - unique_values), mask, repeat)
            else:
                repeat = True

        return doc_list

    def mask(self, doc: str = '') -> str:
        """Mascara o documento enviado"""
        pass

    def _only_digits(self, doc: str = '') -> str:
        """Remove os outros caracteres que não sejam dígitos."""
        return "".join([x for x in doc if x.isdigit()])

    def _validate_input(self, input: str, valid_characters: List = None) -> bool:
        """Validar input.
        Caso ele possua apenas dígitos e caracteres válidos, retorna True.
        Caso possua algum caractere que não seja dígito ou caractere válido, retorna False."""
        if valid_characters is None:
            valid_characters = ['.', '-', '/', ' ']

        set_non_digit_characters = set([x for x in input if not x.isdigit()])
        set_valid_characters = set(valid_characters)

        return not (len(set_non_digit_characters.difference(set_valid_characters)) > 0)

    def check_formatting(self, doc: str) -> bool:
        """Confere se a formatação está correta, é necessário passar um regex válido para o construtor da classe BaseDoc.

        Args:
            doc (str): O número do documento para validar, numérico ou não.

        Returns:
            bool: Se é válido ou não
        """
        try:
            match = self.regex.fullmatch
        except AttributeError as ex:
            raise AttributeError('Regex pattern não foi passado ao construtor da classe, ' +
                                 'certifique-se de usar "super().__init__(regex_pattern: str)"'+
                                 'corretamente.\n' +
                                 str(ex))

        if doc.isnumeric():
            return True

        return match(doc) is not None
