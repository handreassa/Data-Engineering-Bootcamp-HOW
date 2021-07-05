#%%
import pandas as pd
from selenium import webdriver
import time


#%%
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, executable_path=r".\src\chromedriver.exe")
driver.implicitly_wait(10)
time.sleep(5)
driver.get("https://pt.wikipedia.org/wiki/Nicolas_Cage")
tb_filmes = "/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[2]"


#%%
def tem_item(xpath, driver=driver):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


#%%
if tem_item(tb_filmes):
    print("OK")
i = 0
while not tem_item(tb_filmes):
    i += 1
    if i > 30:
        break
    pass

# %%
tabela = driver.find_element_by_xpath(tb_filmes)
# print(tabela.get_attribute('innerHTML'))
# %%
df = pd.read_html("<table>" + tabela.get_attribute("innerHTML") + "</table>")[0]
#%%
with open("print.png", 'wb') as f:
        f.write(driver.find_element_by_xpath('/html/body/div').screenshot_as_png)


# %%
#df
# %%
# df.columns

#%%
# df[df.Ano == 1984]

#%%
df.to_csv("movies_nicolas_cage.csv", sep=";", index=False)
print("Arquivo gerado com sucesso!")

#%%
driver.close()

