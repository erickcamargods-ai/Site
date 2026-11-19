"""Deixa os links internos do site com endereço absoluto e limpo ("/sobre/", nunca
"sobre/index.html") e põe em cada página o redirecionamento de "/x/index.html" para "/x/".
Uso: python3 limpar_links.py PASTA_DO_SITE [URL_BASE]"""
import sys, os, re, glob, posixpath

raiz = sys.argv[1]
base = (sys.argv[2] if len(sys.argv) > 2 else 'https://erickcamargo.adv.br/').rstrip('/') + '/'
host = re.sub(r'^https?://', '', base).rstrip('/')

# O GitHub Pages não permite configurar redirecionamento 301. O mais próximo possível:
# a página, aberta por ".../index.html", troca o endereço pelo limpo antes de desenhar
# (o Google trata como redirecionamento), e o <link rel="canonical"> já aponta para o limpo.
REDIR = ('<script>if(/\\/index\\.html$/.test(location.pathname))'
         'location.replace(location.pathname.replace(/index\\.html$/,"")+location.search+location.hash)</script>')

def limpo(caminho):
    """'/sobre/index.html' -> '/sobre/'; '/index.html' -> '/'."""
    if caminho.endswith('/index.html'):
        caminho = caminho[:-len('index.html')]
    elif caminho == 'index.html':
        caminho = '/'
    return caminho

def trocar(pagina_rel):
    pasta = '/' + posixpath.dirname(pagina_rel)
    def f(m):
        href = m.group(2)
        if href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
            return m.group(0)
        absoluto = re.match(r'https?://' + re.escape(host) + r'(/.*)?$', href)
        if absoluto:
            href = absoluto.group(1) or '/'
        elif re.match(r'[a-z]+:', href) or href.startswith('//'):
            return m.group(0)  # outro site
        caminho, sep, resto = re.match(r'([^?#]*)([?#]?)(.*)', href).groups()
        if not caminho.endswith(('.html', '/')) and caminho not in ('', '.', '..'):
            return m.group(0)  # arquivo (css, js, imagem): não é link de página
        if not caminho.startswith('/'):
            caminho = posixpath.normpath(posixpath.join(pasta, caminho or '.'))
            if not caminho.endswith('.html'):
                caminho = caminho.rstrip('/') + '/'
        return m.group(1) + limpo(caminho) + sep + resto + m.group(3)
    return f

for arq in sorted(glob.glob(os.path.join(raiz, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(arq, raiz).replace(os.sep, '/')
    s = open(arq, encoding='utf-8').read()
    novo = re.sub(r'(<a\b[^>]*?\bhref=")([^"]*)(")', trocar(rel), s)
    if rel.endswith('index.html') and 'location.replace(location.pathname.replace(/index' not in novo:
        novo = novo.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + REDIR, 1)
    if novo != s:
        open(arq, 'w', encoding='utf-8').write(novo)

# índice da busca: "artigos/index.html" -> "artigos/"
b = os.path.join(raiz, 'assets', 'busca.js')
if os.path.exists(b):
    s = open(b, encoding='utf-8').read()
    novo = re.sub(r'"u": "((?:[^"]*/)?)index\.html"', r'"u": "\1"', s)
    if novo != s:
        open(b, 'w', encoding='utf-8').write(novo)
