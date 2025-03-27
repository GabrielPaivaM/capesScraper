import math
import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import colorama
import sqlite3

init(autoreset=True)


# Verifique se o arquivo do banco de dados já existe
if os.path.exists('capesdb.db'):
    try:
        # Tentando conectar ao banco de dados
        database = sqlite3.connect('capesdb.db')
        cursor = database.cursor()
        print(f"{Fore.LIGHTGREEN_EX}Conexão bem-sucedida ao banco de dados.{Fore.LIGHTWHITE_EX}")

    except sqlite3.DatabaseError as e:
        print(f"{Fore.LIGHTRED_EX}Erro ao conectar ao banco de dados:{Fore.LIGHTWHITE_EX}", e)
        print(f"{Fore.LIGHTCYAN_EX}Criando um novo banco de dados...")
        os.remove('capesdb.db')  # Remove o arquivo existente
        database = sqlite3.connect('capesdb.db')
        cursor = database.cursor()
else:
    print(f"{Fore.LIGHTCYAN_EX}Criando um novo banco de dados...{Fore.LIGHTWHITE_EX}")
    database = sqlite3.connect('capesdb.db')
    cursor = database.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS registers (
        id TEXT PRIMARY KEY, 
        issn TEXT, 
        title TEXT NOT NULL, 
        language TEXT, 
        subject TEXT, 
        publisher TEXT, 
        open_access TEXT, 
        reviewed TEXT, 
        link Text,
        linkPublisher Text,
        date DATE
    );
""")
database.commit()

subjects = [
    "Administração",
    "Educação",
    "Sociologia",
    "Psicologia",
    "Clínica+Médica",
    "Letras",
    "Economia",
    "Ciência+da+Computação",
    "Ciência+Política",
    "História",
    "Física",
    "Química",
    "Geociências",
    "Linguística",
    "Engenharia+Química",
    "Biofísica",
    "Biologia+Geral",
    "Antropologia",
    "Direito",
    "Geografia",
    "Matemática",
    "Psiquiatria",
    "Artes",
    "Engenharia+Elétrica",
    "Saúde+Coletiva",
    "Engenharia+de+Materiais+e+Metalúrgica",
    "Neurologia",
    "Agronomia",
    "Farmacologia",
    "Genética",
    "Morfologia",
    "Filosofia",
    "Ciências+Ambientais",
    "Zoologia",
    "Engenharia+Biomédica",
    "Botânica",
    "Ecologia",
    "Cirurgia",
    "Engenharia+Mecânica",
    "Comunicação",
    "Teologia",
    "Cardiologia",
    "Cancerologia",
    "Microbiologia",
    "Interdisciplinar.+Sociais+e+Humanidades",
    "Saúde+e+Biológicas",
    "Oceanografia",
    "Doenças+Infecciosas+e+Parasitárias",
    "Farmácia",
    "Educação+Física",
    "Recursos+Florestais+e+Engenharia+Florestal",
    "Odontologia",
    "Medicina+Veterinária",
    "Arquitetura+e+Urbanismo",
    "Engenharia+Civil",
    "Interdisciplinar.+Engenharia%2FTecnologia%2FGestão",
    "Ciência+da+Informação",
    "Enfermagem",
    "Fisiologia",
    "Radiologia+Médica",
    "Gastroenterologia",
    "Nefrologia",
    "Endocrinologia",
    "Probabilidade+e+Estatística",
    "Engenharia+Sanitária",
    "Ginecologia+e+Obstetrícia",
    "Ciência+e+Tecnologia+de+Alimentos",
    "Engenharia+de+Produção",
    "Serviço+Social",
    "Saúde+Materno-Infantil",
    "Imunologia",
    "Ortopedia",
    "Alergologia+e+Imunologia",
    "Nutrição",
    "Ensino",
    "Anatomia+Patológica+e+Patologia+Clínica",
    "Planejamento+Urbano+e+Regional",
    "Pneumologia",
    "Recursos+Pesqueiros+e+Engenharia+de+Pesca",
    "Demografia",
    "Fisiatria",
    "Zootecnia",
    "Fisioterapia+e+Terapia+Ocupacional",
    "Interdisciplinar.+Meio+Ambiente+e+Agrárias",
    "Interdisciplinar.+Saúde+e+Biológicas",
    "Cirurgia+Otorrinolaringologia",
    "Hematologia",
    "Meio+Ambiente+e+Agrárias",
    "Oftalmologia",
    "Dermatologia",
    "Arqueologia",
    "Parasitologia",
    "Astronomia",
    "Bioquímica",
    "Engenharia+Nuclear",
    "Turismo",
    "Engenharia+Aeroespacial",
    "Engenharia+de+Transportes",
    "Engenharia+de+Minas",
    "Biotecnologia"
]
languages = [
    "Inglês",
    "Alemão",
    "Espanhol",
    "Português",
    "Coreano",
    "Catalão",
    "Indonésio",
    "Francês",
    "Italiano",
    "Japonês",
    "Romeno",
    "Tagalog",
    "Vietnamita",
    "Não+Identificado",
    "Russo",
    "Polonês",
    "Somali",
    "Turco",
    "Esloveno",
    "Suaíli",
    "Ucraniano",
    "Croata",
    "Finlandês",
    "Húngaro",
    "Estoniano",
    "Africâner",
    "Persa",
    "Norueguês",
    "Galês",
    "Holandês",
    "Lituano",
    "Letão",
    "Árabe",
    "Dinamarquês",
    "Eslovaco",
    "Sueco",
    "Búlgaro",
    "Tcheco",
    "Albanês",
    "Urdu",
    "Macedônio",
    "Grego",
    "Tailandês"
]

# Lista de User-Agents
user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

def configure_driver():
    user_agent = random.choice(user_agent_list)

    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Navegação anônima
    chrome_options.add_argument("--disable-infobars")  # Desabilitar barras de informação
    chrome_options.add_argument("--disable-extensions")  # Desabilitar extensões
    chrome_options.add_argument(f"user-agent={user_agent}")  # Usar o User-Agent aleatório

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def getCookies():
    c = 0
    print(f"{Fore.LIGHTCYAN_EX}Abrindo o chrome para a obtenção dos cookies")
    driver = configure_driver()
    url = f"https://www-periodicos-capes-gov-br.ez106.periodicos.capes.gov.br/"
    driver.get(url)

    url = f"https://www-periodicos-capes-gov-br.ez106.periodicos.capes.gov.br/index.php/acervo/lista-a-z-periodicos.html"
    driver.get(url)

    cookies = driver.get_cookies()

    print(f"{Fore.LIGHTCYAN_EX}Os seguintes cookies foram capturados: {Fore.LIGHTWHITE_EX}")
    for cookie in cookies:
        print(cookie)

    driver.quit()

    # Converter para o formato de string de cookies
    cookie_header = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    return cookie_header

def scrapeSite(subjectsList, languagesList):
    cookies = getCookies()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': cookies
    }
    variable_to_alter_languages_list = languagesList
    for subject in subjectsList:
        for language in variable_to_alter_languages_list:
            c = 0
            url = f"https://www-periodicos-capes-gov-br.ez106.periodicos.capes.gov.br/index.php/acervo/lista-a-z-periodicos.html?q=&source=resources&areas%5B%5D=areas%3D%3D{subject}&language%5B%5D=language%3D%3D{language}"
            site = requests.get(url, headers=headers)
            soup = BeautifulSoup(site.content, 'html.parser')
            print(Fore.LIGHTGREEN_EX + subject + " - " + language)

            divMaxResults = soup.find('div', class_='pagination-information d-none d-sm-flex')

            spanMaxResults = divMaxResults.find('span', class_='total')

            if spanMaxResults:
                spanMaxResults = spanMaxResults.get_text().strip()
                numberOfPages = spanMaxResults
                print(f"{Fore.LIGHTCYAN_EX}Numero de registros: {Fore.LIGHTWHITE_EX}{numberOfPages}")

                if int(numberOfPages) <= 30:
                    numberOfPages = 1
                else:
                    numberOfPages = math.ceil(int(numberOfPages)/30)

                print(f"{Fore.LIGHTCYAN_EX}Numero de paginas : {Fore.LIGHTWHITE_EX}" + str(numberOfPages) + "\n")
            else:
                numberOfPages = None
                print(f"{Fore.LIGHTRED_EX}A area {Fore.LIGHTWHITE_EX}{subject}{Fore.LIGHTRED_EX} no idioma {Fore.LIGHTWHITE_EX}{language}{Fore.LIGHTRED_EX} não existe\n")

            if spanMaxResults:
                for page in range(1, numberOfPages + 1):
                    url = f"https://www-periodicos-capes-gov-br.ez106.periodicos.capes.gov.br/index.php/acervo/lista-a-z-periodicos.html?q=&source=resources&areas%5B%5D=areas%3D%3D{subject}&language%5B%5D=language%3D%3D{language}&page={page}"
                    site = requests.get(url, headers=headers)
                    soup = BeautifulSoup(site.content, 'html.parser')

                    divsOfResults = soup.find_all("div", class_="col-md-12 br-item")
                    for div_ in divsOfResults:
                        # Codigo para pegar a informação de acesso aberto
                        openAccess = div_.find('span', title = 'Acesso aberto')
                        if openAccess:
                            openAccess = "Acesso aberto"
                        else:
                            openAccess = "null"

                        # Codigo para pegar a informação de revisado por partes
                        peerReviewed = div_.find('span', title = 'Revisado por pares')
                        if peerReviewed:
                            peerReviewed = "Revisado por pares"
                        else:
                            peerReviewed = "null"


                        # Codigo para pegar a informação de titulo, link e ID
                        title = div_.find('a', class_='titulo-busca')
                        if title:
                            link = title.get('href')
                            title = title.get_text().strip()
                            id = link.split('id=')[1]
                        else:
                            link = "null"
                            title = "null"
                            id = "null"

                        linkPublisher = div_.find('a', class_='br-button small link-default add-metrics mr-3')
                        if linkPublisher:
                            linkPublisher = linkPublisher.get('href')
                        else:
                            linkPublisher = "null"

                        # Codigo para pegar a informação de editora
                        publisher = div_.find_all('p', class_='text-down-01')
                        if publisher:
                            publisher = publisher[0].get_text().strip()
                        else:
                            publisher = "null"

                        # Pegando o ISSN dentro da pagina
                        url = f"https://www-periodicos-capes-gov-br.ez106.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=resources&id={id}"
                        site = requests.get(url, headers=headers)
                        soup = BeautifulSoup(site.content, 'html.parser')

                        issn = soup.find_all('p', class_='text-muted mb-3 block')
                        if issn:
                            issn = issn[0].get_text().strip()
                        c +=1
                        save_on_database(c, page, numberOfPages, id, issn, title, language, subject, publisher, openAccess, peerReviewed, link, linkPublisher)
                        variable_to_alter_languages_list = languages


def save_on_database(c, page, numberOfPages, id, issn, title, language, subject, publisher, open_access, reviewed, link, linkPublisher):
    if not id or id == '':
        id = 'null'

    if not issn or issn == '':
        issn = 'null'

    if not title or title == '':
        title = 'null'

    if not language or language == '':
        language = 'null'

    if not subject or subject == '':
        subject = 'null'

    if not publisher or publisher == '':
        publisher = 'null'

    if not open_access or open_access == '':
        open_access = 'null'

    if not reviewed or reviewed == '':
        reviewed = 'null'

    if not link or link == '':
        link = 'null'

    if not linkPublisher or linkPublisher == '':
        linkPublisher = 'null'

    subject = subject.replace('%2F', '/').replace('+', ' ')
    language = language.replace('+', ' ')

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("SELECT id, language, subject FROM registers WHERE id = ?", (id,))
    vef = cursor.fetchone()

    if vef:
        thereIsChange = False
        newLanguage = vef[1]
        newSubject = vef[2]

        if not language in vef[1]:
            newLanguage = vef[1] + f', {language}'
            thereIsChange = True

        if not subject in vef[2]:
            newSubject = vef[2] + f', {subject}'
            thereIsChange = True

        if thereIsChange == True:
            cursor.execute("UPDATE registers SET language = ?, subject = ? WHERE id = ?", (newLanguage, newSubject, id))
            database.commit()

            print(f"{Fore.LIGHTWHITE_EX}{c} Pagina {page}/{numberOfPages}: {Fore.LIGHTCYAN_EX}registro de id {Fore.LIGHTWHITE_EX}{id} {Fore.LIGHTCYAN_EX}ha um novo valor encontrado, atualizado para ({Fore.LIGHTWHITE_EX}{newSubject}{Fore.LIGHTCYAN_EX} : {Fore.LIGHTWHITE_EX}{newLanguage}{Fore.LIGHTCYAN_EX})")
        else:
            print(f"{Fore.LIGHTWHITE_EX}{c} Pagina {page}/{numberOfPages}: {Fore.LIGHTRED_EX}registro de id {Fore.LIGHTWHITE_EX}{id} {Fore.LIGHTRED_EX}ja esta salvo no banco ({Fore.LIGHTWHITE_EX}{subject}{Fore.LIGHTRED_EX} : {Fore.LIGHTWHITE_EX}{language}{Fore.LIGHTRED_EX})")

    else:
        cursor.execute('INSERT INTO registers VALUES (?,?,?,?,?,?,?,?,?,?,?)', (
            id,
            issn,
            title,
            language,
            subject,
            publisher,
            open_access,
            reviewed,
            link,
            linkPublisher,
            date
        ))
        database.commit()
        print(f"{Fore.LIGHTWHITE_EX}{c} Pagina {page}/{numberOfPages}: {Fore.LIGHTGREEN_EX}registro de id {Fore.LIGHTWHITE_EX}{id} {Fore.LIGHTGREEN_EX}foi salvo no banco ({Fore.LIGHTWHITE_EX}{subject}{Fore.LIGHTGREEN_EX} : {Fore.LIGHTWHITE_EX}{language}{Fore.LIGHTGREEN_EX})\n")

def show_menu(options, title):
    """
    Exibe um menu no terminal para o usuário selecionar uma opção.
    """
    print(f"\n{Fore.LIGHTCYAN_EX}{title}")
    for idx, option in enumerate(options):
        print(f"{Fore.LIGHTWHITE_EX}[{idx + 1}] {option}")

    while True:
        try:
            choice = int(input(f"{Fore.LIGHTGREEN_EX}Digite o número da sua escolha: {Fore.LIGHTWHITE_EX}"))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"{Fore.LIGHTRED_EX}Por favor, escolha um número válido entre 1 e {len(options)}.")
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Entrada inválida! Digite um número.")

# Mostrar o menu de escolha para o usuário
selected_subject = show_menu(subjects, "Escolha a área (subject):")
selected_language = show_menu(languages, "Escolha o idioma (language):")

subjects_list = list()
languages_list = list()
index_subject = -1
index_language = -1

for subject in subjects:
    index_subject += 1
    if subject == selected_subject:
        break

for language in languages:
    index_language += 1
    if language == selected_language:
        break

for i in range(index_subject, len(subjects) - 1):
    subjects_list.append(subjects[i])

for i in range(index_language, len(languages) - 1):
    languages_list.append(languages[i])

print(f"\n{Fore.LIGHTCYAN_EX}Você selecionou:")
print(f"{Fore.LIGHTWHITE_EX}Área: {Fore.LIGHTGREEN_EX}{selected_subject}")
print(f"{Fore.LIGHTWHITE_EX}Idioma: {Fore.LIGHTGREEN_EX}{selected_language}")

# Passar as escolhas para o restante do programa
scrapeSite(subjects_list, languages_list)
