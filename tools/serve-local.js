// Local static server for site-brand/ that mimics vercel.json "cleanUrls":
// /contact serves contact.html, and /contact.html redirects to /contact.
// Usage: node tools/serve-local.js [port]   (default 8092)
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../site-brand');
const PORT = +process.argv[2] || 8092;
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp',
  '.mp4': 'video/mp4', '.xml': 'application/xml', '.txt': 'text/plain', '.json': 'application/json' };
http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  let p = decodeURIComponent(u.pathname);
  if (p.endsWith('.html') && p !== '/index.html') {            // cleanUrls: canonical form has no extension
    res.writeHead(308, { Location: p.slice(0, -5) + u.search }); return res.end();
  }
  if (p === '/') p = '/index.html';
  let f = path.join(ROOT, p);
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f += '.html';
  if (!fs.existsSync(f)) { res.writeHead(404); return res.end('404'); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(PORT, '127.0.0.1', () => console.log('serving', ROOT, 'on', PORT));
