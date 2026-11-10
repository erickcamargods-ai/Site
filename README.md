# Érick Camargo Advogado

Site estático publicado pelo GitHub Pages.

A pasta raiz é o site pronto. `.ferramentas/publicar.py` gera esta versão a partir da cópia de trabalho, acrescentando endereço oficial das páginas, cartões de compartilhamento, dados estruturados, `sitemap.xml`, `robots.txt`, `llms.txt` e a página 404:

    python3 .ferramentas/publicar.py ORIGEM DESTINO URL_BASE

Ao trocar para o domínio próprio, rode de novo com a nova URL base e acrescente o arquivo `CNAME`.

© 2026 Érick Camargo. Todos os direitos reservados.
