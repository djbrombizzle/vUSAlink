# vUSAlink — Web (no download required)

This folder is a complete, self-contained website. Hosting it on GitHub Pages gives
controllers a **direct link** they can open in any browser — no Python, no download,
nothing to install. It runs **hub-only**: every CPDLC clearance goes through the shared
**KUSA** hub, exactly like the desktop app in hub mode.

`index.html` is the entire app (HTML + CSS + JavaScript in one file). It talks directly
to the hub over HTTPS.

---

## Prerequisite (one time): the hub must allow browser calls

The browser version calls the hub directly, so the hub has to send CORS headers. That
support is built into the current `hub.py` — **redeploy `hub-for-railway/` to Railway
once** so the live hub is running the CORS-enabled build. If you skip this, the website
will load but every hub request will fail with a CORS error in the browser console.

(The hub URL is already baked into the page:
`https://web-production-3d9fe.up.railway.app`. If your hub URL changes, edit the
`DEFAULT_HUB_URL` line near the top of the `<script>` in `index.html`.)

---

## Publish the site (GitHub Pages — free)

1. Create (or reuse) a **public** GitHub repo, e.g. `vusalink-web`.
2. Upload **`index.html`** to the repo root (Add file → Upload files → commit).
3. Repo **Settings → Pages**:
   - **Source:** Deploy from a branch
   - **Branch:** `main`, folder `/ (root)` → **Save**
4. Wait ~1 minute. Your link appears at the top of the Pages settings, e.g.
   `https://YOURNAME.github.io/vusalink-web/`
5. Share that link. Done.

> Want a tidier URL? Add a `CNAME` file with your custom domain and point a DNS
> CNAME record at `YOURNAME.github.io` (standard GitHub Pages custom-domain setup).

---

## What a controller does

1. Open the link.
2. Settings opens automatically on the first visit — enter your **VATSIM CID** and save.
   (The hub URL is pre-filled and hidden; there is nothing else to configure.)
3. Be **online controlling a center** on VATSIM (e.g. `JAX_CTR`). The hub identifies your
   sector from your live position.
4. **Verify once:** a yellow bar shows a code like `VUSA-AB12`. Put that code anywhere in
   your controller info / ATIS. Within a few seconds the bar clears and you can uplink.
   (This proves you are the real controller for that position. The code is per-session.)

Everything else is identical to the desktop app: the traffic board, climb/descend,
direct-to, crossing restrictions, route amendments, CONTACT/handoff with frequencies,
the logon chime, and the 20 nm approaching-traffic buffer.

---

## What is **not** on the web version

- **Solo / direct-Hoppie mode.** A browser can't talk to Hoppie directly (no CORS on
  Hoppie's side), which is the whole reason the hub exists. The website is therefore
  hub-only. Anyone who needs solo direct-logon use can still run the downloadable
  `vUSAlink.py` (it supports both modes).

---

## Updating the site later

Edit `index.html` in the repo (or re-upload a newer copy with the same name to
overwrite) and commit. GitHub Pages redeploys automatically in about a minute. Settings
and your session live in each controller's own browser (localStorage), so updates never
touch their saved CID.
