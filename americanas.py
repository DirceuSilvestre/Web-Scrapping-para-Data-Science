import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import pandas as pd

# a lista de produtos que eu quero saber os preços no site da Americanas
produtos_buscados = ["lapis grafite hb", "estojo escolar", "borracha branca", "apontador", "regua 20cm", "tesoura sem ponta", "mochila escolar"]

# ["caderno 10 materias", "lapis de cor 12 cores", "caneta bic azul", "lapis grafite hb", "estojo escolar", "borracha branca", "apontador", "regua 20cm", "tesoura sem ponta", "mochila escolar"]

# a data do dia em que esse código vai rodar
data = datetime.today().date()

# o nome do site onde obteremos os dados
site = "Americanas"

# então o código vai rodar a quantidade de vezes igual a quantidade de produtos a ser buscado no site
# são 10 produtos de papelaria que quero saber os preços
# então por 10 vezes ele vai criar um webdrive do firefox
# entrar no site da Americanas, digitar o nome do produto da vez que esta na lista, clicar na lupa para buscar
# ao aparecer os produtos, o código clica na ordenação, e clica para aparecer primeiro os menores preços
# na ordem do menor para o maior
# a partir daí coletamos os nomes e preços dos produtos que aparecem na primeira página
# ainda precisamos fazer um tratamento no texto, ou nao, só ver se esta a palavra buscada dentro
# e talvez só fazer a limpeza dos dados depois, mas por que nao fazer logo agora?!

for produtos in range(len(produtos_buscados)):

    # site que queremos abrir
    americanas = 'https://www.americanas.com.br/'

    # criamos uma máquina do mozzila firefox
    maquina = webdriver.Firefox()

    # caso a maquina nao tenha sido aberta, o codigo se conecta a minha conta do twilio
    # e manda um sms para o meu telefone

    maquina.maximize_window()

    # dizemos pra máquina qual site queremos acessar
    # e aqui a mesma coisa, se não acessar vai me avisar por sms
    maquina.get(americanas)

    # esperamos o site abrir
    WebDriverWait(maquina, timeout=2)

    # buscamos a barra onde iremos escrever o objetivo da busca e clicamos nela
    # 3 clicks para que outros quadrados de mensagem no site possam fechar ao clicar
    maquina.find_element(By.TAG_NAME, 'input').click()

    WebDriverWait(maquina, timeout=2)

    maquina.find_element(By.TAG_NAME, 'input').click()

    WebDriverWait(maquina, timeout=2)

    maquina.find_element(By.TAG_NAME, 'input').click()

    # aqui esta o que vamos procurar, que é um dos elementos da lista lá de cima
    # depois do click já podemos escrever o que estamos procurando no site
    maquina.find_element(By.TAG_NAME, 'input').send_keys(
        f"{produtos_buscados[produtos]}")

    # agora busco o botão de pesquisa, aquela lupa, e clico nele para
    # executar a busca do que acabei de escrever na barra de busca
    maquina.find_element(
        By.TAG_NAME, 'button').click()

    WebDriverWait(maquina, timeout=10)

    # faz a busca pelo elemento de ordenação dos produtos no site
    # se não conseguir achar espera, pois deve estar carregando a página, e tenta de novo
    '''try:
        maquina.find_element(
            By.CSS_SELECTOR, 'select[id="sort-by"]').click()

    except:
        maquina.implicitly_wait(100)
        try:
            maquina.find_element(
                By.CSS_SELECTOR, 'select[id="sort-by"]').click()

        except:
            WebDriverWait(maquina, timeout=2)

    # tenta mais uma vez, porque estava dando muito problema de não encontrar
    # e queremos ter a certeza que vai encontrar
    maquina.find_element(
        By.CSS_SELECTOR, 'select[id="sort-by"]').click()

    # ordena para iniciar nos menores preços
    maquina.find_element(
        By.CSS_SELECTOR, 'option[value="lowerPriceRelevance"]').click()'''

    WebDriverWait(maquina, timeout=2)

    # essa parte estava impedindo de clicar em outra importante para a pesquisa
    # então eu tento clicar, se não conseguir ele espera um pouco e continua o código normalmente
    # pois se coloco na sequencia normal pode dar erro caso não esteja lá por conta de atualização do site
    try:
        maquina.find_element(
            By.CSS_SELECTOR, 'div[class="src__Wrapper-sc-bu6nft-0 eHIHza"]').click()

    except:
        WebDriverWait(maquina, timeout=2)

    maquina.implicitly_wait(60)

    # exceto no caso da mochila escolar que o resultado de menor preço nos retorna sacolas ao inves de mochilas
    # essa parte do código clica em um link escrito ordenar por menores preços, é a segunda forma de ordenação
    # quase como uma confirmação de que quer somente os menores preços, e não menores preços com os mais relevantes
    # caso nao funcione o codigo espera um pouco para tentar novamente
    '''try:
        if produtos_buscados[produtos] != "mochila escolar":
            maquina.find_element(
                By.LINK_TEXT, 'ordenar apenas por menores preços.').click()
    except:
        maquina.find_element(
            By.CSS_SELECTOR, 'button[class="lgpd-message-box__Button-sc-5cg4t9-3 isYUgc"]').click()
        if (produtos_buscados[produtos] != "mochila escolar") and (produtos_buscados[produtos] != "lapis de cor 12 cores"):
            maquina.implicitly_wait(100)
            maquina.find_element(
                By.LINK_TEXT, 'ordenar apenas por menores preços.').click()

    WebDriverWait(maquina, timeout=2)'''

    # coleta todos os nomes dos produtos
    lista_nomes_pagina_1 = maquina.find_elements(
        By.CSS_SELECTOR, "h3[class='product-name__Name-sc-1shovj0-0 gUjFDF']")

    # coleta todos os preços dos produtos
    lista_precos_pagina_1 = maquina.find_elements(
        By.CSS_SELECTOR, 'span[class="src__Text-sc-154pg0p-0 price__PromotionalPrice-sc-h6xgft-1 ctBJlj price-info__ListPriceWithMargin-sc-1xm1xzb-2 liXDNM"]')

    # precisamos verificar a quantidade de nomes e preços que foram coletados do site
    # pois as vezes ele coleta mais nomes que preços ou o contrário
    # então necessitamos que os nomes e os preços sejam os seus respectivos
    tamanho1 = len(lista_nomes_pagina_1)
    tamanho2 = len(lista_precos_pagina_1)

    # se tiver mais nomes que preços, elimina os ultimos nomes até ficarem só os respectivos, e a mesma quantidade
    if tamanho1 > tamanho2:
        while len(lista_nomes_pagina_1) > len(lista_precos_pagina_1):
            del lista_nomes_pagina_1[-1]
            print(len(lista_nomes_pagina_1))

    # se tiver mais preços que nomes, elimina os ultimos preços até ficarem só os respectivos, e a mesma quantidade
    elif tamanho2 > tamanho1:
        while len(lista_precos_pagina_1) > len(lista_nomes_pagina_1):
            del lista_precos_pagina_1[-1]
            print(len(lista_precos_pagina_1))

    # cria o dataframe e tambem as listas respectivas que serao os itens das colunas do nosso dataframe
    dataframe = pd.DataFrame()
    produto_texto = []
    preco_texto = []

    for elementos in range(len(lista_nomes_pagina_1)):
        dentro = all(
            string in lista_nomes_pagina_1[elementos].text for string in produtos_buscados[produtos].strip())
        if produtos != 1:
            if dentro:
                produto_texto.append(lista_nomes_pagina_1[elementos].text)
                preco_texto.append(
                    (lista_precos_pagina_1[elementos].text)[-5:])

        else:
            produto_texto.append(lista_nomes_pagina_1[elementos].text)
            preco_texto.append((lista_precos_pagina_1[elementos].text)[-5:])

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
