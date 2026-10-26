# Higher Heights

Static site for the Higher Heights film and photography studio. No framework, no runtime dependencies. Pages are generated from two data files by `scripts/build.mjs`; the enquiry form is a Vercel serverless function.

```
data/site.json        clients, expertise, process, contact details
data/projects.json    one entry per film. Edit this to add or change a project
src/css, src/js       design system and progressive-enhancement script
scripts/build.mjs     data -> dist/ (home, work, project pages, expertise, studio, contact, privacy, 404, sitemap, robots)
api/enquiry.js        POST /api/enquiry
legacy/index.html     the previous single-page site, kept for reference (not built)
assets/               images, video, logos (see below). Not generated
```

## Run it

```
npm run build      # writes dist/
npm run dev        # build + preview at http://localhost:4173
npm run check      # lists any /assets/... files the site references but assets/ lacks
```

## Assets: required before it looks right

The site uses the same file names as the previous site. Copy the old `assets/` folder in unchanged:

- `assets/img/`: `hh-cream.svg`, `hh-navy.svg`, `hh-gold.svg` (favicon), `wordmark-cream.svg`, `icon-180.png`, every `poster-*.jpg`, `rm-1…6.jpg`, `aerial-*.jpg`, `portrait.jpg`, `matchroom-1.jpg`, `clients/*.png`
- `assets/vid/`: `commercial.mp4` (home hero), `roller`, `nobl`, `wtc`, `rm69`, `cleanco`, `hero` (used for Highland Road), `whoop`, `aduna`

Optional: `assets/og/<project-slug>.jpg` (1200×630) is used as the share image for that project page. Without it the poster is used, which crops badly for vertical films.

## Adding or editing a project

Add an object to `data/projects.json` (copy an existing one). `brief`, `credits` (`[{"role":"Director","name":"…"}]`), `services` and `gallery` are optional and only render when filled in. Nothing is invented: empty fields simply don't appear. Run `npm run build`.

## Enquiry form (needs setup before launch)

`/api/enquiry` emails the studio through [Resend](https://resend.com). Set these in Vercel → Settings → Environment Variables:

| Variable | |
|---|---|
| `RESEND_API_KEY` | required. Until set, the form tells visitors to email directly instead of pretending to send |
| `ENQUIRY_FROM` | e.g. `Higher Heights <enquiries@higherheights.studio>`. The domain must be verified in Resend |
| `ENQUIRY_TO` | optional, defaults to `hello@higherheights.studio` |
| `TURNSTILE_SITE_KEY` + `TURNSTILE_SECRET_KEY` | optional Cloudflare Turnstile. Add both to enable it |
| `SITE_URL` | optional, canonical origin for share tags and sitemap (default `https://higher-heights.vercel.app`; set to the real domain at launch) |

Spam protection: hidden honeypot field, minimum fill time, same-origin check, per-IP rate limit, optional Turnstile. The limiter is in-memory per function instance, so Turnstile is the real defence if spam appears.

## Deploying

Vercel settings come from `vercel.json` (`node scripts/build.mjs` → `dist`). Connect this repo to the `higher-heights` project (Settings → Git) or run `vercel --prod`.

## Before launch

- Review `/privacy`. It is a placeholder written from what the site does today.
- Fonts (Bricolage Grotesque, DM Mono) load from Google Fonts. Self-host the WOFF2 files for best performance and privacy.
- Fill in `brief` and `credits` per project when Morgan has the wording.
