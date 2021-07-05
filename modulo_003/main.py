import pandas as pd
from selenium import webdriver
import sys
import time

cep = sys.argv[1]

if cep:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        options=options, executable_path=r".\src\chromedriver.exe"
    )
    time.sleep(5)
    # %% Exemplo site da How Bootcamps
    # driver.get("https:\\howedu.com.br")
    # driver.find_element_by_class_name("mc-closeModal").click()
    # driver.find_element_by_xpath('//*[@id="PopupSignupForm_0"]/div[2]/div[1]').click()
    # driver.find_element_by_xpath("/html/body/section[4]/div/div/div[2]/a").click()

    # Exemplo utilização site dos correios
    driver.get("https://buscacepinter.correios.com.br/app/endereco/index.php")
    time.sleep(5)
    elem_cep = driver.find_element_by_name("endereco")
    elem_cep.clear()
    elem_cep.send_keys(cep)

    elem_cmb = driver.find_element_by_name("tipoCEP")
    elem_cmb.click()
    driver.find_element_by_xpath(
        '//*[@id="formulario"]/div[2]/div/div[2]/select/option[6]'
    ).click()

    driver.find_element_by_id("btn_pesquisar").click()

    time.sleep(5)
    #%% Captura dos dados
    logradouro = driver.find_element_by_xpath(
        "/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr/td[1]"
    ).text
    bairro = driver.find_element_by_xpath(
        "/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr/td[2]"
    ).text
    localidade = driver.find_element_by_xpath(
        "/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr/td[3]"
    ).text
    print(
        f"""Dados para o CEP: {cep}
    Logradouro: {logradouro.split(' - ')[0]}
    Bairro: {bairro}
    Localidade: {localidade}
    """
    )

    driver.close()
