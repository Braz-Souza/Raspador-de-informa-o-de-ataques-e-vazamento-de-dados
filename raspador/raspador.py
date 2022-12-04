from bs4 import BeautifulSoup
import requests

def raspador(url):
    """
    Função que recebe uma url e retorna um objeto BeautifulSoup

    Arguments:
        url: url da página que irá raspada
    
    Returns:
        objeto BeautifulSoup que irá ser raspado
    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except:
        print("Erro: Não foi possível acessar a página.")
        return None
    
def noticias(soup):
    """
    Função que recebe um objeto BeautifulSoup e retorna 4 listas:
    com os links, títulos, descrições e imagens das notícias.

    Arguments:
        soup: objeto BeautifulSoup da página a ser raspada

    Returns:
        4 listas com os links, títulos, descrições e imagens das notícias
    """
    try:
        noticias = soup.findAll('li', attrs={'class' : 'widget--card'})
        links_noticias = []
        titulos_noticias = []
        descricoes_noticias = []
        imagens_noticias = []
        
        for noticia in noticias:
            try:
                text_container = noticia.find('div', attrs={'class' : 'widget--info__text-container'})
                a = text_container.find('a')
                titulo = a.find('div', attrs={'class' : 'widget--info__title'})
                descricao = a.find('p', attrs={'class' : 'widget--info__description'})
            except: 
                continue

            links_noticias.append(a['href'])
            titulos_noticias.append(titulo.text)
            descricoes_noticias.append(descricao.text)

            try:
                media_container = noticia.find('div', attrs={'class' : 'widget--info__media-container'})
                media_container_a = media_container.find('a')
                imagem = media_container_a.find('img')['src']
            except:
                imagem = ""
            finally:
                imagens_noticias.append(imagem)
        return links_noticias, titulos_noticias, descricoes_noticias, imagens_noticias
    except:
        print("Erro: Não foi possível acessar as notícias.")
        return None

def salvar_noticias(Noticia, links, titulos, descricoes, imagens):
    """
    Função que salva as notícias no banco de dados.

    Arguments:
        Noticia: modelo de notícia
        links: lista com os links das notícias
        titulos: lista com os títulos das notícias
        descricoes: lista com as descrições das notícias
        imagens: lista com as imagens das notícias

    Returns:
        None
    """
    try:
        for i in range(len(links)):
            if not Noticia.objects.filter(link=links[i]).exists():
                noticia = Noticia(link=links[i], title=titulos[i], desc=descricoes[i], img=imagens[i])
                noticia.save()
    except:
        print("Erro: Não foi possível salvar as notícias.")

def salvar_noticias_g1(Noticia, palavra_chave):
    """
    Função que salva as notícias do g1 no banco de dados.
    
    Arguments:
        Noticia: modelo de notícia
        palavra_chave: palavra_chave que será pesquisada no g1

    Returns:
        None
    """
    url = f'https://g1.globo.com/busca/?q={palavra_chave}&page=1&order=recent&species=notícias'
    soup = raspador(url)
    if soup:
        links, titulos, descricoes, imagens = noticias(soup)
        salvar_noticias(Noticia, links, titulos, descricoes, imagens)

def salvar_noticias_techtudo(Noticia, palavra_chave):
    """
    Função que salva as notícias do techtudo no banco de dados.

    Arguments:
        Noticia: modelo de notícia
        palavra_chave: palavra_chave que será pesquisada no techtudo

    Returns:
        None
    """
    url = f'https://www.techtudo.com.br/busca/?q={palavra_chave}&page=1&order=recent&species=notícias'
    soup = raspador(url)
    if soup:
        links, titulos, descricoes, imagens = noticias(soup)
        salvar_noticias(Noticia, links, titulos, descricoes, imagens)

def pesquisar_por_palavra_chaves_e_depois_salvar_noticias(Noticia):
    """
    Função que pesquisa por notícias com as palavras chaves predefinidas
    e salva no banco de dados.

    Arguments:
        Noticia: modelo de notícia

    Returns:
        None
    """
    palavra_chaves = {'Invasão de dados', 'Ataque de dados', 'Vazamento de informações'}
    for palavra_chave in palavra_chaves:
        salvar_noticias_g1(Noticia, palavra_chave)
        salvar_noticias_techtudo(Noticia, palavra_chave)
    
    print("Notícias salvas com sucesso!")


