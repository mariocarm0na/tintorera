// Genera dist/worker.js: un Worker de Cloudflare que sirve la web desde lamejortintorera.com
// y redirige (301) el resto de hostnames. og-image.png se sirve desde KV.
// Uso: node deploy/build.mjs [--index]   (--index permite la indexación en buscadores)
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
const root = new URL("..", import.meta.url);
const read = (f) => readFileSync(new URL(f, root), "utf8");
const INDEXABLE = process.argv.includes("--index");
const min = (s) => s.replace(/\n\s+/g, "\n").replace(/\n{2,}/g, "\n");
const files = {
  "/": [min(read("index.html")), "text/html; charset=utf-8"],
  "/robots.txt": [read("robots.txt"), "text/plain; charset=utf-8"],
  "/sitemap.xml": [read("sitemap.xml"), "application/xml; charset=utf-8"],
  "/llms.txt": [read("llms.txt"), "text/markdown; charset=utf-8"],
};
const worker = `const INDEXABLE=${INDEXABLE};
const HOST="lamejortintorera.com";
const F=${JSON.stringify(files)};
export default{async fetch(req,env){
const u=new URL(req.url);
if(u.hostname!==HOST)return Response.redirect("https://"+HOST+u.pathname+u.search,301);
const h={"x-content-type-options":"nosniff","referrer-policy":"strict-origin-when-cross-origin","cache-control":"public, max-age=300"};
if(!INDEXABLE)h["x-robots-tag"]="noindex";
if(u.pathname==="/og-image.png"){const b=await env.KV.get("og-image.png","arrayBuffer");if(!b)return new Response("Not found",{status:404});return new Response(b,{headers:{...h,"content-type":"image/png","cache-control":"public, max-age=86400"}})}
const f=F[u.pathname==="/index.html"?"/":u.pathname];
if(!f)return Response.redirect("https://"+HOST+"/",301);
return new Response(req.method==="HEAD"?null:f[0],{headers:{...h,"content-type":f[1]}});
}};
`;
mkdirSync(new URL("dist/", root), { recursive: true });
writeFileSync(new URL("dist/worker.js", root), worker);
console.log("dist/worker.js", worker.length, "bytes, INDEXABLE =", INDEXABLE);
