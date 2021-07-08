#%%
import datetime
import math


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


#%%
herivelton = Pessoa(
    nome="Herivelton",
    sobrenome="Andreassa",
    data_de_nascimento=datetime.date(1992, 8, 20),
)

print(herivelton)
# %%
print(herivelton.nome)

# %%
print(herivelton.sobrenome)
#%%
herivelton.idade
# %%
