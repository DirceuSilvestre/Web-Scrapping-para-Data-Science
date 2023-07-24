from time import sleep
from numpy import product
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

sleep(2)
busca = drive.find_element_by_tag_name('input')
busca.click()


busca.send_keys('lapis preto hb n2')

busca = drive.find_element_by_tag_name('button')

busca.click()

#Vai até a barra de "Ordenar por:" e clica nela
#Seleciona para mostrar produtos a partir do menor preço

menor_preco = drive.find_element_by_xpath("//form[@class='src__SortBar-sc-1oc11r-0 hEjDBT']")
menor_preco.click()

menor_preco = drive.find_element_by_xpath("//option[@value='lowerPrice']")
menor_preco.click()

sleep(2)

#Obtem o nome de todos os produtos listados na página

produto = []
produto = drive.find_elements_by_xpath("//h3[@class='product-name__Name-sc-1shovj0-0 gUjFDF']")

#for i in range(24):
#    print(produto[i].text)

preco = []
preco = drive.find_elements_by_xpath("//span[@class='src__Text-sc-154pg0p-0 price__PromotionalPrice-sc-h6xgft-1 ctBJlj price-info__ListPriceWithMargin-sc-1xm1xzb-2 liXDNM']")

#for i in range(24):
#    print(preco[i].text)

#Falta encontrar a barra final e clicar para ir a próxima página

contador = 2
while (contador < 4):
    proximo = drive.find_elements_by_xpath("//button[@class='src__PageButton-sc-82ugau-3 fhogRv']")
    proximo[contador].click()

    produto.append(drive.find_elements_by_xpath("//h3[@class='product-name__Name-sc-1shovj0-0 gUjFDF']"))

    preco.append(drive.find_elements_by_xpath("//span[@class='src__Text-sc-154pg0p-0 price__PromotionalPrice-sc-h6xgft-1 ctBJlj price-info__ListPriceWithMargin-sc-1xm1xzb-2 liXDNM']"))

    contador+=1
    

numero = 3 * 24
for i in range(numero):
    print(produto[i].text)




sleep(6)

drive.quit()