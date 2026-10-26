// Lists every /assets/... file the built site references but assets/ does not contain.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dist = path.join(root, "dist");
const refs = new Set();
(function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const f = path.join(d, e.name);
    if (e.isDirectory()) { if (e.name !== "assets") walk(f); }
    else if (/\.(html|css)$/.test(e.name)) for (const m of fs.readFileSync(f, "utf8").matchAll(/\/assets\/([A-Za-z0-9_./-]+\.[a-z0-9]+)/g)) refs.add(m[1]);
  }
})(dist);
const missing = [...refs].filter((r) => !fs.existsSync(path.join(root, "assets", r))).sort();
console.log(`${refs.size} assets referenced, ${missing.length} missing`);
missing.forEach((m) => console.log("  missing: assets/" + m));
process.exit(missing.length ? 1 : 0);
