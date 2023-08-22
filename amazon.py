import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import pandas as pd

# a lista de produtos que eu quero saber os preços no site da Amazon
produtos_buscados = ["caderno 10 materias","lapis de cor 12 cores", "caneta BIC azul", "lapis grafite hb", "estojo escolar", "borracha branca", "apontador", "regua 20cm", "tesoura sem ponta", "mochila escolar"]

# ["caderno 10 materias", "lapis de cor 12 cores", "caneta BIC azul", "lapis grafite hb", "estojo escolar", "borracha branca", "apontador", "regua 20cm", "tesoura sem ponta", "mochila escolar"]

# a data do dia em que esse código vai rodar
data = datetime.today().date()

# o nome do site onde obteremos os dados
site = "Amazon"

# então o código vai rodar a quantidade de vezes igual a quantidade de produtos a ser buscado no site
# são 10 produtos de papelaria que quero saber os preços
# então por 10 vezes ele vai criar um webdrive do firefox
# entrar no site da Amazon, digitar o nome do produto da vez que esta na lista, clicar na lupa para buscar
# ao aparecer os produtos, o código clica na ordenação, e clica para aparecer primeiro os menores preços
# na ordem do menor para o maior
# a partir daí coletamos os nomes e preços dos produtos que aparecem na primeira página
# ainda precisamos fazer um tratamento no texto, ou nao, só ver se esta a palavra buscada dentro
# e talvez só fazer a limpeza dos dados depois, mas por que nao fazer logo agora?!

for produtos in range(len(produtos_buscados)):

    # site que queremos abrir
    amazon = 'https://www.amazon.com.br/'

    # criamos uma máquina do mozzila firefox
    maquina = webdriver.Firefox()

    # caso a maquina nao tenha sido aberta, o codigo se conecta a minha conta do twilio
    # e manda um sms para o meu telefone

    maquina.maximize_window()

    # dizemos pra máquina qual site queremos acessar
    # e aqui a mesma coisa, se não acessar vai me avisar por sms
    maquina.get(amazon)

    # esperamos o site abrir
    WebDriverWait(maquina, timeout=2)

    # buscamos a barra onde iremos escrever o objetivo da busca e clicamos nela
    # 3 clicks para que outros quadrados de mensagem no site possam fechar ao clicar
    maquina.find_element(By.CLASS_NAME, 'nav-search-field ').click()

    WebDriverWait(maquina, timeout=2)

    maquina.find_element(By.CLASS_NAME, 'nav-search-field ').click()

    WebDriverWait(maquina, timeout=2)

    maquina.find_element(By.CLASS_NAME, 'nav-search-field ').click()

    WebDriverWait(maquina, timeout=2)

    # aqui esta o que vamos procurar, que é um dos elementos da lista lá de cima
    # depois do click já podemos escrever o que estamos procurando no site
    maquina.find_element(By.ID, 'twotabsearchtextbox').send_keys(
        f"{produtos_buscados[produtos]}")

    # agora busco o botão de pesquisa, aquela lupa, e clico nele para
    # executar a busca do que acabei de escrever na barra de busca
    maquina.find_element(
        By.ID, 'nav-search-submit-button').click()

    WebDriverWait(maquina, timeout=10)

    # faz a busca pelo elemento de ordenação dos produtos no site
    # se não conseguir achar espera, pois deve estar carregando a página, e tenta de novo
    try:
        maquina.find_element(
            By.CSS_SELECTOR, 'select[id="a-autoid-0-announce"]').click()

    except:
        maquina.implicitly_wait(10)
        try:
            maquina.find_element(
                By.CSS_SELECTOR, 'select[id="a-autoid-0-announce"]').click()

        except:
            WebDriverWait(maquina, timeout=2)

    # tem um objeto por cima do seguinte, o erro diz que este esta obscurecendo o próximo, impedindo de clicar no próximo
    # então primeiro clicaremos nesse objeto para que ele desapareça e o código não ter dificuldade em clicar
    # no próximo, que é onde desejamos
    maquina.find_element(
        By.CSS_SELECTOR, 'span[class="a-dropdown-prompt"]').click()

    WebDriverWait(maquina, timeout=2)

    # ordena para iniciar nos menores preços
    try:
        maquina.find_element(
            By.CSS_SELECTOR, 'a[id="s-result-sort-select_1"]').click()

    except:
        maquina.find_element(
            By.CSS_SELECTOR, 'a[id="s-result-sort-select_1"]').click()

    # esperando o site carregar

    maquina.implicitly_wait(10)

    maquina.implicitly_wait(10)

    maquina.implicitly_wait(10)

    maquina.implicitly_wait(10)

    maquina.implicitly_wait(10)

    maquina.implicitly_wait(10)

    # tenta a primeira vez e verifica quantos itens pegou dos que carregaram
    lista_nomes_pagina_1 = maquina.find_elements(
        By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')
    print(len(lista_nomes_pagina_1))

    # espera mais uma vez pra carregar o restante

    maquina.implicitly_wait(10)

    maquina.implicitly_wait(10)

    maquina.implicitly_wait(10)

    maquina.implicitly_wait(10)

    maquina.implicitly_wait(10)

    # tenta novamente pois agora já devem ter carregado mais elementos, e verifica novamente
    lista_nomes_pagina_1 = maquina.find_elements(
        By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]')

    print(len(lista_nomes_pagina_1))

    # não estou conseguindo pegar separadamente cada nome e preço de cada item que ele nos retorna
    # então eu pego os vários blocos que correspondem a cada produto
    # e dentro de cada bloco procuro o nome e preço daquele produto específico
    # porém alguns produtos não tem preço, já verifiquei no site, e isso pode retornar um erro
    # então precisamos tratar essa condição, caso o código encontre um produto sem preço

    produto_texto = []
    preco_texto = []

    for item in range(len(lista_nomes_pagina_1)):
        try:
            lista_nomes_pagina_1[item].find_element(
                By.CSS_SELECTOR, 'span[aria-hidden="true"]')
            produto_texto.append(
                lista_nomes_pagina_1[item].find_element(By.TAG_NAME, 'h2').text)
            preco_texto.append(lista_nomes_pagina_1[item].find_element(
                By.CSS_SELECTOR, 'span[aria-hidden="true"]').text)
        except:
            continue

    # precisamos verificar a quantidade de nomes e preços que foram coletados do site
    # pois as vezes ele coleta mais nomes que preços ou o contrário
    # então necessitamos que os nomes e os preços sejam os seus respectivos
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

    # cria o dataframe e tambem as listas respectivas que serao os itens das colunas do nosso dataframe
    dataframe = pd.DataFrame()

    dataframe['Produto'] = produto_texto
    dataframe['Preco'] = preco_texto
    dataframe['Site'] = site
    dataframe['Dia'] = data.day
    dataframe['Mes'] = data.month
    dataframe['Ano'] = data.year

    # precisamos imprimir so pra ver se foi tudo correto
    print(dataframe)

    # colocamos o arquivo dentro de uma variavel para verificar se ele existe
    arquivo = "D:/Meus Documentos/Meus Projetos/Web-Scrapping-para-Data-Science/" + \
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
