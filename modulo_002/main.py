#%%
#Imports
import requests
import json

# %%
url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
ret = requests.get(url)

# %%
if ret:
    print(ret)
else:
    print("Erro")

# %%
dolar = json.loads(ret.text)['USDBRL']

# %%
print(f" 20 Dólares hoje custam {float(dolar['bid']) *20} reais")

# %%
def cotacao(valor, moeda):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"
    # url = "https://economia.awesomeapi.com.br/json/last/{}".format(moeda)
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) *20} {moeda[-3:]}")

#%%
cotacao(20, 'USD-BRL')

# %%
cotacao(20, 'JPY-BRL')

# %%
#tratamento de erros simples:
try:
    cotacao(20, 'JPY-BTC')
except:
    pass

# %%
try:
    cotacao(20, 'JPY-BTC')
except Exception as e:
    print(e)
else:
    print("Ok")



# %%

# Forma simplificada sem uso de decorador:

def multi_moeda(valor):
    lst_ccy = ["USD-BRL","EUR-USD", "BTC-BRL", "JPY-BRL", "RPL-USD"]

    for item in lst_ccy:
        try:
            url = f"https://economia.awesomeapi.com.br/json/last/{item}"
            ret = requests.get(url)
            dolar = json.loads(ret.text)[item.replace('-', '')]
            print(
                f"{valor} {item[:3]} hoje custam {float(dolar['bid']) *20} {item[-3:]}"
            )
        except:
            print(f"Falha na moeda: {item}")

# %%
multi_moeda(20)

#%%
def error_check(func):
    def inner_func(*ars, **kargs):
        try:
            func(*ars, *kargs)
        except:
            print(f"{func.__name__} falhou!")
    return inner_func
# Usando decorador:
@error_check    
def cotacao(valor, moeda):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"
    # url = "https://economia.awesomeapi.com.br/json/last/{}".format(moeda)
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) *20} {moeda[-3:]}")

cotacao(20, "BRL-USD")
cotacao(20, "EUR-BRL")
cotacao(20, "JPY-BRL")
cotacao(20, "ERRADO")

# %%
#Lib para usar em validações de APIs (decoradores pré construídos): backoff
import backoff
import random

#Usando o decorador do backoff
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f"""
            RND: {rnd}
            args: {args if args else 'sem args'}
            kargs: {kargs if kargs else 'sem kargs'}
            """)
    if rnd < .2:
        raise ConnectionAbortedError("Conexão foi finalizada")
    if rnd < .4:
        raise ConnectionRefusedError("Conexão foi recusada.")
    elif rnd < .6:
        raise TimeoutError("Tempo de espera excedido.")
    else:
         return "Ok!"
# %%
test_func()

# %%
test_func(42)
# %%
test_func(42, 51, nome='Herivelton')
# %%

# %%
#Pacote para criação de logs
import logging

# %%
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)
# %%
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kargs):
    rnd = random.random()
    log.debug(f"RND: {rnd}")
    log.info(f"args: {args if args else 'sem args'}")
    log.info(f"kargs: {kargs if kargs else 'sem kargs'}")
    if rnd < .2:
        log.error("Conexão foi finalizada")
        raise ConnectionAbortedError("Conexão foi finalizada")
    if rnd < .4:
        log.error("Conexão foi recusada.")
        raise ConnectionRefusedError("Conexão foi recusada.")
    elif rnd < .6:
        log.error("Tempo de espera excedido.")
        raise TimeoutError("Tempo de espera excedido.")
    else:
         return "Ok!"

# %%
test_func()
# %%
