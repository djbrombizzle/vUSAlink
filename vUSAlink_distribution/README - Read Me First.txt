===========================================================
  vUSAlink  -  CPDLC controller tool for VATSIM (USA)
  Read Me First
===========================================================

This is a small, safe program. There is nothing to install for the app
itself and nothing gets added to your system -- it just runs and opens
in your web browser. To stop it, close the black window it opens.

It does need Python (a free, standard tool) to run. One-time setup below.

-----------------------------------------------------------
STEP 1 - Install Python (one time, ~2 minutes)
-----------------------------------------------------------
1. Go to:  https://www.python.org/downloads/
2. Click the big "Download Python" button and run the installer.
3. WINDOWS USERS: on the first screen of the installer, TICK THE BOX
   "Add Python to PATH" before clicking Install. (Important!)
4. Finish the install. You only ever do this once.

-----------------------------------------------------------
STEP 2 - Start vUSAlink
-----------------------------------------------------------
WINDOWS:  double-click  "Start vUSAlink (Windows).bat"
MAC:      double-click  "Start vUSAlink (Mac or Linux).command"
          (First time on a Mac: right-click it, choose "Open", then
           click "Open" again to get past the security prompt.)

A black window opens and your web browser pops up with vUSAlink.
Leave the black window open while you use it. Closing it stops vUSAlink.

-----------------------------------------------------------
STEP 3 - Set it up (click SETTINGS in the app)
-----------------------------------------------------------
You will use ONE of these two modes:

A) SHARED HUB (the KUSA network - what most people use)
   Enter these under SETTINGS -> "Shared HUB mode":
     - Hub URL          (e.g. https://something.up.railway.app, from your
                         coordinator)
     - My VATSIM CID    (your VATSIM member ID number)
   That's all. The hub figures out which center you're working from your
   LIVE VATSIM position, so you must be signed on and actually controlling a
   center (e.g. JAX_CTR) for traffic to appear. Leave the Hoppie code blank.
   (There's an optional "network password" field - you only fill it in if your
    coordinator tells you the hub requires one. Most won't.)

B) SOLO / DIRECT (your own Hoppie connection)
   If you are not using the shared hub, enter under SETTINGS:
     - Hoppie logon code  (free from hoppie.nl)
     - Station ID         (your ARTCC ICAO, e.g. KZJX)
   Leave the Hub fields blank in this mode.

Click Save. The board fills with traffic for your airspace.

-----------------------------------------------------------
USING IT (quick tour)
-----------------------------------------------------------
- Aircraft logging on to CPDLC are accepted automatically.
- Click an ALTITUDE to issue a climb/descend/maintain.
- Click the ROUTE to send a direct-to or crossing restriction.
- Click the FLIGHT ID to hand off (voice CONTACT, or CPDLC HANDOVER).
- The SOUND button toggles the logon/message chimes.
- The EDST button switches to the authentic ERAM EDST look.

-----------------------------------------------------------
TROUBLESHOOTING
-----------------------------------------------------------
"Python was not found"
   -> You skipped Step 1, or (Windows) didn't tick "Add Python to PATH".
      Re-run the Python installer and tick that box.

Mac: "cannot be opened because it is from an unidentified developer"
   -> Right-click the .command file, choose Open, then Open again.

The browser didn't open
   -> Look in the black window for a line like
      http://127.0.0.1:8732  and open that address in your browser.

Nothing reaches aircraft
   -> Make sure the pilot has logged their CPDLC on to the station you
      were told to use (KUSA for the shared hub).

That's it. Happy controlling!
