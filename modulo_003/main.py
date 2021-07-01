#%%
import pandas as pd
from selenium import webdriver

# %%
driver = webdriver.Chrome(r".\src\chromedriver.exe")

# %% Exemplo site da How Bootcamps
driver.get("https:\\howedu.com.br")
#driver.find_element_by_class_name("mc-closeModal").click()
driver.find_element_by_xpath('//*[@id="PopupSignupForm_0"]/div[2]/div[1]').click()
driver.find_element_by_xpath('/html/body/section[4]/div/div/div[2]/a').click()

#%% Exemplo utilização site dos correios
driver.get("https://buscacepinter.correios.com.br/app/endereco/index.php")
elem_cep = driver.find_element_by_name('endereco')


#%%
elem_cep.clear()
elem_cep.send_keys('80420130')

#%%
elem_cmb = driver.find_element_by_name("tipoCEP")
elem_cmb.click()
driver.find_element_by_xpath('//*[@id="formulario"]/div[2]/div/div[2]/select/option[6]').click()

#%%
driver.find_element_by_id("btn_pesquisar").click()

#%%
driver.close()


# %%
