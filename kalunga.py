import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import pandas as pd

# a lista de produtos que eu quero saber os preços no site da Kalunga
produtos_buscados = ["caderno 10 materias", "lapis de cor 12 cores", "caneta bic azul", "lapis grafite hb", "estojo escolar", "borracha branca", "apontador", "regua 20cm", "tesoura sem ponta", "mochila escolar"]

# ["caderno 10 materias", "lapis de cor 12 cores", "caneta bic azul", "lapis grafite hb", "estojo escolar", "borracha branca", "apontador", "regua 20cm", "tesoura sem ponta", "mochila escolar"]

# a data do dia em que esse código vai rodar
data = datetime.today().date()

# o nome do site onde obteremos os dados
site = "Kalunga"

# então o código vai rodar a quantidade de vezes igual a quantidade de produtos a ser buscado no site
# são 10 produtos de papelaria que quero saber os preços
# então por 10 vezes ele vai criar um webdrive do firefox
# entrar no site da Kalunga, digitar o nome do produto da vez que esta na lista, clicar na lupa para buscar
# ao aparecer os produtos, o código clica na ordenação, e clica para aparecer primeiro os menores preços
# na ordem do menor para o maior
# a partir daí coletamos os nomes e preços dos produtos que aparecem na primeira página
# ainda precisamos fazer um tratamento no texto, ou nao, só ver se esta a palavra buscada dentro
# e talvez só fazer a limpeza dos dados depois, mas por que nao fazer logo agora?!
for produtos in range(len(produtos_buscados)):

    # site que queremos abrir
    kalunga = 'https://www.kalunga.com.br/'

    # criamos uma máquina do mozzila firefox
    maquina = webdriver.Firefox()

    # caso a maquina nao tenha sido aberta, o codigo se conecta a minha conta do twilio
    # e manda um sms para o meu telefone

    maquina.maximize_window()

    # dizemos pra máquina qual site queremos acessar
    # e aqui a mesma coisa, se não acessar vai me avisar por sms
    maquina.get(kalunga)

    # esperamos o site abrir
    WebDriverWait(maquina, timeout=2)

    # buscamos a barra onde iremos escrever o objetivo da busca e clicamos nela
    # 3 clicks para que outros quadrados de mensagem no site possam fechar ao clicar
    maquina.find_element(By.ID, 'txtBuscaProd').click()

    WebDriverWait(maquina, timeout=2)

    maquina.find_element(By.ID, 'txtBuscaProd').click()

    WebDriverWait(maquina, timeout=2)

    maquina.find_element(By.ID, 'txtBuscaProd').click()

    # aqui esta o que vamos procurar, que é um dos elementos da lista lá de cima
    # depois do click já podemos escrever o que estamos procurando no site
    maquina.find_element(By.ID, 'txtBuscaProd').send_keys(
        f"{produtos_buscados[produtos]}")

    # agora busco o botão de pesquisa, aquela lupa, e clico nele para
    # executar a busca do que acabei de escrever na barra de busca
    maquina.find_element(By.CSS_SELECTOR, 'div[class="block-geral"]').click()

    maquina.find_element(
        By.CSS_SELECTOR, 'button[class="btn btn-orange-ka px-3 py-2 rounded-end"]').click()

    WebDriverWait(maquina, timeout=10)

    maquina.find_element(
        By.ID, 'btnContinueClose').click()

    # faz a busca pelo elemento de ordenação dos produtos no site
    # se não conseguir achar espera, pois deve estar carregando a página, e tenta de novo
    try:
        maquina.find_element(
            By.ID, 'cboOrdenacao').click()

    except:
        maquina.implicitly_wait(100)
        try:
            maquina.find_element(
                By.ID, 'cboOrdenacao').click()

        except:
            WebDriverWait(maquina, timeout=2)

    # tenta mais uma vez, porque estava dando muito problema de não encontrar
    # e queremos ter a certeza que vai encontrar
    maquina.find_element(
        By.ID, 'cboOrdenacao').click()

    # ordena para iniciar nos menores preços
    maquina.find_element(
        By.CSS_SELECTOR, 'option[value="3"]').click()

    WebDriverWait(maquina, timeout=1000)

    # nos capturamos todas as caixas onde contem os produtos
    # dessas caixas iremos extrair os nomes dos produtos e seus respectivos preços
    blocos = maquina.find_elements(
        By.CSS_SELECTOR, 'div[class="blocoproduto   col-6 col-md-4 col-xl-3"]')

    # cria o dataframe e tambem as listas respectivas que serao os itens das colunas do nosso dataframe
    dataframe = pd.DataFrame()
    produto_texto = []
    preco_texto = []

    WebDriverWait(maquina, timeout=2)

    # vamos pegar cada bloco para extrair seu texto
    # e do texto extraido separamos o que é nome e o que é preço
    for item in blocos:
        texto = item.text
        '''dentro = all(
            string in texto for string in produtos_buscados[produtos].strip())
        if produtos != 1:
            if dentro:'''
        produto_texto.append(texto[:60])
        preco_texto.append(texto[-5:])

        '''else:
            produto_texto.append(texto[:60])
            preco_texto.append(texto[-5:])'''
        # produto_texto.append(texto[:60])
        # preco_texto.append(texto[-5:])

    tamanho1 = len(produto_texto)
    tamanho2 = len(preco_texto)

    # se tiver mais nomes que preços, elimina os ultimos nomes até ficarem só os respectivos, e a mesma quantidade
    if tamanho1 > tamanho2:
        while len(produto_texto) > len(preco_texto):
            del produto_texto[-1]
            print(len(produto_texto))

    # se tiver mais preços que nomes, elimina os ultimos preços até ficarem só os respectivos, e a mesma quantidade
    elif tamanho2 > tamanho1:
        while len(preco_texto) > len(produto_texto):
            del preco_texto[-1]
            print(len(preco_texto))

    dataframe['Produto'] = produto_texto
    dataframe['Preco'] = preco_texto
    dataframe['Site'] = site
    dataframe['Dia'] = data.day
    dataframe['Mes'] = data.month
    dataframe['Ano'] = data.year

    # precisamos imprimir so pra ver se foi tudo correto
    print(dataframe)

    arquivo = "C:/Users/dirce/OneDrive/Documentos/Meus Projetos/Web-Scrapping-para-Data-Science/" + \
        produtos_buscados[produtos] + '.csv'
    existe = os.path.exists(arquivo)

    # se o arquivo não existe a gente cria
    # se ele existe, nós pegamos suas informações e fazemos a concatenação com o que coletamos agora, linha por linha
    if existe == False:
        dataframe.to_csv(f"{produtos_buscados[produtos]}.csv", index=False)
    else:
        dataframe_existente = pd.read_csv(arquivo)
        dataframe_existente = pd.concat(
            [dataframe_existente, dataframe], axis=0, ignore_index=True)
        dataframe_existente.to_csv(
            f"{produtos_buscados[produtos]}.csv", index=False)

    # pedimos para a maquina aguardar um tempo curto, e fechamos para partir para a próxima coleta de dados
    WebDriverWait(maquina, timeout=2)

    maquina.close()
