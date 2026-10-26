# Higher Heights — existing site

`index.html` is the live single-page site. The first commit on this branch is the exact production HTML; the second applies the edits.

## What changed from the original
- **Fonts:** Geist and Instrument Serif replaced by Bricolage Grotesque (display and body) and DM Mono (labels).
- **Colours:** navy, cream and gold replaced by obsidian `#0C0D0C`, bone `#E9E5DB`, sage `#8A9A86` (plus graphite `#1E201F`). Client logo hover tints are unchanged. The monogram SVGs in `assets/img/` are the approved originals and keep their own colours.
- **Enquiry form:** same four-step flow, now collects name, email and a short message and POSTs to `/api/enquiry` (see `api/enquiry.js`) instead of opening the visitor's email app. Success only shows after the studio email is really sent.
- **SEO and sharing:** one consistent title and description, canonical URL, absolute `og:image`, Twitter card, JSON-LD (Organization and a VideoObject per film), `robots.txt`, `sitemap.xml`.

## Needed to run
`assets/` (images, video, logos) is not in the repo yet. Copy the existing folder in unchanged.

## Enquiry form setup (Vercel → Settings → Environment Variables)
| Variable | |
|---|---|
| `RESEND_API_KEY` | required. Until set the form says it isn't connected and points to the email address |
| `ENQUIRY_FROM` | e.g. `Higher Heights <enquiries@higherheights.studio>` (domain verified in Resend) |
| `ENQUIRY_TO` | optional, default `hello@higherheights.studio` |
| `TURNSTILE_SECRET_KEY` | optional Cloudflare Turnstile (the widget would also need adding to the form) |

Spam protection: hidden honeypot, minimum fill time, same-origin check, per-IP rate limit.

## Before the real domain goes on
Replace `https://higher-heights.vercel.app` in `index.html`, `robots.txt` and `sitemap.xml`.
