"""Gera a versão de publicação do site: canonical, Open Graph, dados estruturados,
sitemap.xml, robots.txt, llms.txt e 404. Uso: python3 publicar.py ORIGEM DESTINO URL_BASE"""
import sys,os,re,json,shutil,html,glob
src,dst,base=sys.argv[1],sys.argv[2],sys.argv[3].rstrip('/')+'/'
if os.path.exists(dst):
    for n in os.listdir(dst):
        if n=='.git':continue
        p=os.path.join(dst,n);shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
else: os.makedirs(dst)
for n in os.listdir(src):
    p=os.path.join(src,n);(shutil.copytree if os.path.isdir(p) else shutil.copy2)(p,os.path.join(dst,n))
HOJE='2026-11-09'
PESSOA={"@type":"Person","@id":base+"#erick","name":"Érick Camargo","jobTitle":"Advogado","url":base+"sobre/",
 "image":base+"assets/erick-camargo.jpg","identifier":"OAB/MG 224.100",
 "alumniOf":{"@type":"CollegeOrUniversity","name":"Universidade Federal de Minas Gerais"},
 "knowsAbout":["Licitações","Contratos públicos","Lei 14.133/2021","Concessões","Parcerias público-privadas","Direito do consumidor","Serviços regulados","Pedágio free flow"],
 "address":{"@type":"PostalAddress","addressLocality":"Belo Horizonte","addressRegion":"MG","addressCountry":"BR"}}
paginas=[]
for f in sorted(glob.glob(dst+'/**/index.html',recursive=True)):
    rel=os.path.relpath(f,dst).replace('index.html','').replace(os.sep,'/')
    url=base+rel
    s=open(f).read()
    titulo=html.unescape(re.search(r'<title>(.*?)</title>',s).group(1))
    desc=html.unescape(re.search(r'<meta name="description" content="([^"]*)"',s).group(1))
    artigo='"@type": "Article"' in s or '"@type":"Article"' in s
    img=base+('assets/erick-camargo-perfil-lateral.jpg')
    extra=f'<link rel="canonical" href="{url}">\n'
    if 'og:title' not in s:
        extra+=f'<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(titulo)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:locale" content="pt_BR">\n'
    extra+=f'<meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:site_name" content="Érick Camargo Advogado"><meta name="twitter:card" content="summary_large_image">\n'
    if rel=='':
        ld={"@context":"https://schema.org","@graph":[{"@type":"WebSite","@id":base+"#site","url":base,"name":"Érick Camargo Advogado","inLanguage":"pt-BR","publisher":{"@id":base+"#erick"}},PESSOA]}
        extra+='<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>\n'
    if rel=='sobre/':
        ld={"@context":"https://schema.org","@type":"ProfilePage","url":url,"mainEntity":PESSOA}
        extra+='<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>\n'
    if artigo:
        def fix(m):
            d=json.loads(m.group(1));d["author"]={"@id":base+"#erick","@type":"Person","name":"Érick Camargo","url":base+"sobre/"}
            d["mainEntityOfPage"]=url;d["publisher"]={"@id":base+"#erick"};d["image"]=img
            return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'
        s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',fix,s,flags=re.S)
    s=s.replace('</head>',extra+'</head>',1)
    open(f,'w').write(s)
    paginas.append((rel,titulo,desc))
# sitemap
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for rel,t,d in paginas: sm+=f'<url><loc>{base}{rel}</loc><lastmod>{HOJE}</lastmod></url>\n'
open(dst+'/sitemap.xml','w').write(sm+'</urlset>\n')
# robots: aberto a buscadores e assistentes de IA
open(dst+'/robots.txt','w').write('''User-agent: *
Allow: /

User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: '''+base+'sitemap.xml\n')
# llms.txt: resumo do site para assistentes de IA
ll='# Érick Camargo Advogado\n\n> Artigos sobre licitações, contratos públicos e serviços regulados (pedágio, energia, plano de saúde), escritos por Érick Camargo, advogado (OAB/MG 224.100), sempre a partir do documento original: a lei, o contrato, o edital, a resolução ou a decisão, citados com número e data.\n\n## Artigos\n\n'
for rel,t,d in paginas:
    if rel.startswith('artigos/') and rel!='artigos/': ll+=f'- [{t}]({base}{rel}): {d}\n'
ll+='\n## Sobre o autor\n\n'
for rel,t,d in paginas:
    if rel in ('sobre/','atuacao/'): ll+=f'- [{t}]({base}{rel}): {d}\n'
open(dst+'/llms.txt','w').write(ll)
open(dst+'/.nojekyll','w').write('')
# 404
h=open(dst+'/contato/index.html').read()
a=h.index('<main>');b=h.index('</main>')
p404=h[:a]+'<main>\n<section class="container page-head"><span class="label">Erro 404</span><h1 style="margin-top:12px">Página não encontrada</h1><p>O endereço pode ter mudado. Use a busca no topo ou volte para a <a href="'+base+'">página inicial</a>.</p></section>\n'+h[b:]
p404=re.sub(r'(href|src)="\.\./',r'\1="'+base,p404)
p404=re.sub(r'<link rel="canonical"[^>]*>\n','',p404)
open(dst+'/404.html','w').write(p404.replace('<head>','<head>\n<meta name="robots" content="noindex">',1))
print(len(paginas),'páginas')
