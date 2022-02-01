from time import sleep
import requests
import pandas as pd
from bs4 import BeautifulSoup
from unicodedata import name
from matplotlib.pyplot import table
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

########### Acima #################
#Importa as bibliotecas necessárias

########### Abaixo ################

#Escolhe o site da americanas
#abre o navegador firefox
#e conecta ao site da americanas

url = 'https://www.americanas.com.br/'

drive = webdriver.Firefox()
drive.get(url)

#Aguarda o carregamento total da página
#e coloca em tela cheia o navegador

sleep(1)

drive.maximize_window()

#Procura no HTML o primeiro elemento input
#clica nele
#escreve no input o nome do produto que deseja buscar
#procura no HTML o primeiro botão que é um elemento button
#e clica nele para que busque o termo escrito anteriormente
#após aguardar o carregamento dos resultados fecha o navegador, encerrando o processo

sleep(2)
busca = drive.find_element_by_tag_name('input')
busca.click()


busca.send_keys('lápis hb')

busca = drive.find_element_by_tag_name('button')

busca.click()

menor_preco = drive.find_element_by_xpath("//form[@class='src__SortBar-sc-1oc11r-0 hEjDBT']")
menor_preco.click()

menor_preco = drive.find_element_by_xpath("//option[@value='lowerPrice']")
menor_preco.click()

produto = drive.find_element_by_xpath("//h3[@class='product-name__Name-sc-1shovj0-0 gUjFDF']")

html_content = produto.get_attribute('outherHTML')


soup = BeautifulSoup(html_content,'html.parser')
table = soup.find(name=['table'])

df_full = pd.read_html(str(table))[0].head(10)

print(df_full)


sleep(6)

drive.quit()