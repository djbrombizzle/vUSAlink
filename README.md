# vUSAlink

A simple, browser‑based **CPDLC controller tool for VATSIM US center controllers.**
It shows a live traffic board for your ARTCC and lets you issue clearances —
altitude changes, direct‑to‑fix, crossing restrictions, and handoffs — to
CPDLC‑equipped aircraft over the **Hoppie ACARS** network.

There's nothing to install beyond Python, no compiled `.exe` (so nothing trips
antivirus), and no account to create. You run it, it opens in your browser, you
enter your VATSIM CID, and you're controlling.

\---

## The hub address

vUSAlink connects through a shared hub (the **KUSA** proxy). You'll need this
address during setup:

```
https://web-production-3d9fe.up.railway.app/
```

Want to check it's up? Open this in a browser — it should return `ok`:

```
https://web-production-3d9fe.up.railway.app/hub/health
```

\---

## Get started in 3 steps

### Step 1 — Install Python (one time, \~2 minutes)

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click **Download Python** and run the installer.
3. **Windows users:** on the first screen, **tick "Add Python to PATH"** before
clicking Install. (This is important — skip it and the launcher won't find Python.)
4. Finish the install. You only do this once.

### Step 2 — Download and run vUSAlink

1. Download the app files (`vUSAlink.py` plus the two **Start vUSAlink**
launchers) and put them together in one folder.
2. Start it:

   * **Windows:** double‑click **`Start vUSAlink (Windows).bat`**
   * **Mac:** double‑click **`Start vUSAlink (Mac or Linux).command`**
*(first time on a Mac: right‑click it → **Open** → <b>Open</b> to clear the
security prompt)*
3. A small black window opens and your browser pops up with vUSAlink. **Leave the
black window open** while you work — closing it stops the app.

### Step 3 — Connect to the hub

1. In vUSAlink, click **SETTINGS**.
2. Under **Shared HUB mode**, fill in:

|Field|What to enter|
|-|-|
|**Hub URL**|`https://web-production-3d9fe.up.railway.app/`|
|**My VATSIM CID**|your VATSIM member ID number|

   Leave the Hoppie code blank, and leave **Network password** blank unless your
coordinator told you the hub needs one.

3. Click **Save**.

   That's it. The board fills with traffic for **whatever center you're currently
controlling on VATSIM** — vUSAlink reads your live position, so you must be
signed on and working a center (e.g. `JAX\_CTR`) for aircraft to appear.

   \---

   ## Using it

* **Aircraft that log on to CPDLC are accepted automatically** — the LOGON
column turns green.
* **Click an aircraft's ALTITUDE** to issue climb / descend / maintain.
* **Click the ROUTE** to send a direct‑to‑fix or a crossing restriction.
* **Click the FLIGHT ID** to hand off — voice **CONTACT** (frequency change) or
CPDLC **HANDOVER** to a neighboring center, or release to UNICOM.
* The **R** box flashes red when a new message comes in; click it to read/clear.
* **SOUND** toggles the logon/message chimes.
* **EDST** switches between the classic look and the authentic ERAM EDST skin
(see the next section).

  \---

  ## Switching the look — Classic or EDST

  vUSAlink has two visual styles, and you flip between them with the **EDST**
button in the toolbar across the top of the window:

* **Classic** (the default) — a clean, high‑contrast traffic list. Easiest to read.
* **EDST** — an authentic ERAM EDST skin: the teal "Aircraft List" title bar, the
real EDST fonts and colors, the ACL column layout, and the EDST master toolbar
with a live UTC clock. It looks like the real scope.

  **To switch:**

1. Click the **`EDST`** button in the top toolbar.
2. When the skin is on, the button shows **`EDST ✓`** (with a checkmark). Click it
again to turn the skin off and go back to Classic.
3. Your choice is remembered — vUSAlink reopens in whichever look you used last.

   Everything works exactly the same in both styles. The buttons, clearance menus,
handoffs, sounds, and the message/logon alerts are identical — only the
appearance changes, so use whichever you find easier and switch any time.

   \---

   ## Solo mode (without the hub)

   If you'd rather connect straight to Hoppie with your own logon instead of the
shared hub, open **SETTINGS** and fill in:

* **Hoppie logon code** — free from [https://www.hoppie.nl/acars/](https://www.hoppie.nl/acars/)
* **Station ID** — your ARTCC ICAO, e.g. `KZJX`

  Leave the Hub fields blank in this mode.

  \---

  ## Troubleshooting

  **"Python was not found"**
You skipped Step 1, or (Windows) didn't tick **Add Python to PATH**. Re‑run the
Python installer and tick that box.

  **Mac: "cannot be opened because it is from an unidentified developer"**
Right‑click the `.command` file → **Open** → **Open**.

  **The browser didn't open on its own**
Look in the black window for a line like `http://127.0.0.1:8732` and open that
address in your browser.

  **The board is empty**
Make sure you're signed on to VATSIM and actively controlling a **center**
(`\_CTR`) position — the hub only serves you traffic for the sector you're really
working. After you connect or switch positions, give it up to \~30 seconds.

  **Nothing reaches an aircraft**
Confirm the pilot has logged their CPDLC on to the station you were told to use
(**KUSA** for the shared hub).

  \---

  \---

  *vUSAlink is a community tool for VATSIM (a flight‑simulation network) and is not
used for real‑world air traffic control.*

