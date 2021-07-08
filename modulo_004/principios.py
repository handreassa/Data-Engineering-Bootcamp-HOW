#%%
import datetime
import math
from typing import List


class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor(
            (datetime.date.today() - self.data_de_nascimento).days / 365.2425
        )

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"


herivelton = Pessoa(
    nome="Herivelton",
    sobrenome="Andreassa",
    data_de_nascimento=datetime.date(1992, 8, 20),
)
# %%
print(herivelton)
# %%
class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]):
        self.pessoa = pessoa
        self.experiencias = experiencias

    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)

    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]

    def adiciona_experiencia(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)

    def __str__(self):
        return (
            f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e já "
            f"trabalhou em {self.quantidade_de_experiencias} empresas e atualmente trabalha na empresa {self.empresa_atual}."
        )


curriculo_herivelton = Curriculo(
    pessoa=herivelton, experiencias=["GVT", "Stefanini", "HSBC"]
)
print(curriculo_herivelton.pessoa)
# %%
print(curriculo_herivelton.pessoa.idade)

# %%
print(curriculo_herivelton)
# %%
curriculo_herivelton.adiciona_experiencia("Bradesco")
# %%
class Vivente:
    def __init__(self, nome: str, data_de_nascimento: datetime.date) -> None:
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor(
            (datetime.date.today() - self.data_de_nascimento).days / 365.2425
        )

    def emite_ruido(self, ruido: str):
        print(f"{self.nome} fez ruído: {ruido}")


class PessoaHeranca(Vivente):
    def __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos"

    def fala(self, frase):
        return self.emite_ruido(frase)


herivelton2 = PessoaHeranca(
    nome="Herivelton", data_de_nascimento=datetime.date(1992, 8, 20)
)
print(herivelton2)
# %%
class Cachorro(Vivente):
    def __init__(self, nome: str, data_de_nascimento: datetime.date, raca: str):
        super().__init__(nome, data_de_nascimento)
        self.raca = raca

    def __str__(self):
        return f"{self.nome} é da raça {self.raca} e tem {self.idade} anos"

    def late(self):
        return self.emite_ruido("Au! Au!")


dog = Cachorro(
    nome="Sirius", data_de_nascimento=datetime.date(2021, 3, 4), raca="Spitz"
)
print(dog)

# %%
dog.late()
dog.late()
dog.late()
herivelton2.fala("Para de latir")
dog.late()
dog.late()
