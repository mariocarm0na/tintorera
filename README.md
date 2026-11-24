# lamejortintorera.com

Web personal de Nuria Chavarría y su CV.

- `index.html`, `robots.txt`, `sitemap.xml`, `llms.txt`, `og-image.png`: la web.
- `cv/`: CV en HTML (fuente) y PDF.
- `deploy/build.mjs`: genera `dist/worker.js`, el Worker de Cloudflare que sirve la web.

## Despliegue (Cloudflare)

- Worker `lamejortintorera` en la cuenta de Cloudflare, con un KV `lamejortintorera` que guarda `og-image.png`.
- Dominios del Worker: `lamejortintorera.com` y `www.` sirven la web; `latintoreradetodalavida.com` y `www.` redirigen con 301 al principal.
- La web se sirve con `X-Robots-Tag: noindex` hasta que se apruebe el contenido. Para abrirla a buscadores: `node deploy/build.mjs --index` y volver a subir el Worker.
- Tras abrirla: alta en Google Search Console y Bing Webmaster Tools con `https://lamejortintorera.com/sitemap.xml`.
