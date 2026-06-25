# vUSAlink — Web (no download required)

This folder is a complete, self-contained website. Hosting it on GitHub Pages gives
controllers a **direct link** they can open in any browser — no Python, no download,
nothing to install. It runs **hub-only**: every CPDLC clearance goes through the shared
**KUSA** hub, exactly like the desktop app in hub mode.

`index.html` is the entire app (HTML + CSS + JavaScript in one file). It talks directly
to the hub over HTTPS.

---

## Using it (quick tour)

-----------------------------------------------------------
- Aircraft logging on to CPDLC are accepted automatically.
- Click an ALTITUDE to issue a climb/descend/maintain.
- Click the ROUTE to send a direct-to or crossing restriction.
- Click the FLIGHT ID to hand off (voice CONTACT, or CPDLC HANDOVER).
- The SOUND button toggles the logon/message chimes.
- The EDST button switches to the authentic ERAM EDST look.




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
