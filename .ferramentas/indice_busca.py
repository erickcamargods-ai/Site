"""Refaz o índice da busca (assets/busca.js) a partir das páginas. Uso: python3 indice_busca.py PASTA_DO_SITE"""
import sys,os,glob,re,json,html
d=sys.argv[1];os.chdir(d)
idx=[]
for f in sorted(glob.glob('**/index.html',recursive=True),key=lambda x:(x.count('/'),x)):
    s=open(f).read()
    t=re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S)
    titulo='Início' if f=='index.html' else html.unescape(re.sub(r'<[^>]+>','',t.group(1))).strip()
    main=re.search(r'<main>(.*?)</main>',s,re.S).group(1)
    main=re.sub(r'<p class="nota">.*?</p>|<details.*?</details>|<aside>.*?</aside>|<script.*?</script>','',main,flags=re.S)
    idx.append({'u':f,'t':titulo,'x':html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',main))).strip()})
js=open('assets/busca.js').read()
js=re.sub(r'var IDX=.*?;\n','var IDX='+json.dumps(idx,ensure_ascii=False).replace('\\','\\\\')+';\n',js,count=1,flags=re.S)
open('assets/busca.js','w').write(js)
print(len(idx),'páginas no índice')
