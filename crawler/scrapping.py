import requests
from requests import exceptions
from bs4 import BeautifulSoup


def get_links(url):
    '''
    Obtém todos os links da página indicada pela url.
    Retorna None caso a url seja inválida ou a página não exista,
    ou uma lista com os links da página.
    '''
    # Padroniza a URL.
    url = standardize_url(url)

    # Cria a requisição.
    response = create_request(url)

    if not response:
        return None

    # Extrai os links da página.
    links = create_links_list(url, BeautifulSoup(
        response.content, 'html.parser'))

    if not links:
        return None

    return links


def get_notice_data(url):
    '''
    Obtém todos os links da página indicada pela url.
    Retorna None caso a url seja inválida ou a página não exista,
    ou uma lista com os links da página.
    '''
    # Padroniza a URL.
    url = standardize_url(url)

    # Cria a requisição.
    response = create_request(url)

    if not response:
        return None

    # Extrai os links da página.
    data = create_notice_data(url, BeautifulSoup(
        response.content, 'html.parser'))

    if not data:
        return None

    return data

# Padroniza a URL recebida pela API.


def standardize_url(url: str):
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "https://" + url  # Adiciona "https://" por padrão

    parsed_url = url.split("//")
    domain = parsed_url[1] if len(parsed_url) > 1 else parsed_url[0]

    if not domain.startswith("www."):
        url = url.replace(domain, "www." + domain)

    return url
#


def create_request(url, ssl_cert=True):
    """
    Cria uma requisição e retorna a resposta.
    Tenta criar uma requisição efetuando a verificação dos certificados SSL, 
    caso não consiga cria ignorando a verificação.
    """
    try:
        return requests.get(url)
    except (exceptions.SSLError):
        return requests.get(url, verify=False)
    except (exceptions.ConnectionError, exceptions.MissingSchema,
            exceptions.InvalidSchema, exceptions.InvalidURL):
        return None
    except Exception:
        return None
#

# Extrai os links da página.


def create_links_list(url: str, soup: BeautifulSoup):
    links = []
    td_tags = soup.find_all('td')
    for td in td_tags:
        for link_tag in td.find_all('a', class_='state-published'):
            link_href = link_tag.get('href')

            if (link_href):
                treated_link = treatLink(url, link_href)

                if link_href:
                    links.append(
                        treated_link
                    )

    return links


def create_notice_data(url: str, soup: BeautifulSoup):
    data = {
        'title': soup.find(class_='documentFirstHeading').text,
        'unity': soup.find(id='form-widgets-unidade_instituto').find(class_='selected-option').text,
        'modalidade': soup.find(id='form-widgets-modalidade_edital').find(class_='selected-option').text,
        'numero': soup.find(id='form-widgets-numero_edital').text,
        'ano': soup.find(id='form-widgets-ano_edital').text.replace('.', ''),
        'situacao': soup.find(id='form-widgets-situacao_edital').find(class_='selected-option').text,
        'pdfLink': ''
    }

    noticePdfPage = ''

    tbody_tag = soup.find('tbody')

    tr_tags = tbody_tag.find_all('tr')
    for tr in tr_tags:
        td_tags = tr.find_all('td')
        if (td_tags[1] and 'Arquivo' in td_tags[1].text):
            noticePdfPage = td_tags[0].find('a').get('href')
            break

    response = create_request(noticePdfPage)

    if not response:
        return None

    data['pdfLink'] = BeautifulSoup(response.content, 'html.parser').find(
        id='content-core').find('a').get('href')

    return data


# Trata o link de referência local da página. (ex.: '/favoritos')
# Retorna um link válido. (ex.: 'https://seusite.com/favoritos')
def treatLink(url_page: str, link: str):
    if link.startswith("/"):
        return f"{url_page}{link}"
    if link.startswith("#"):
        return url_page

    return link
