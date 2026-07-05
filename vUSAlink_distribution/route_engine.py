"""Enroute route expansion — fixes, airways, SID/STAR (mirrors VATFLOW route-engine.js)."""

import math
import re

_AWY_RE = re.compile(r"^[JQV]\d+[A-Z]?$", re.I)
_COORD_RE = re.compile(r"^\d{2,4}[NS]\d{3,5}[EW]$")

_navdata = {"fixes": {}, "airways": {}, "procedures": {}, "airports": {}, "loaded": False}


def _haversine_nm(la1, lo1, la2, lo2):
    r = 3440.065
    to_rad = math.radians
    d_la = to_rad(la2 - la1)
    d_lo = to_rad(lo2 - lo1)
    a = (
        math.sin(d_la / 2) ** 2
        + math.cos(to_rad(la1)) * math.cos(to_rad(la2)) * math.sin(d_lo / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))


def _nearest_candidate(cands, ref_ll):
    if not cands:
        return None
    if not ref_ll or len(cands) == 1:
        return cands[0]
    best, bd = cands[0], 1e9
    for c in cands:
        d = _haversine_nm(ref_ll[0], ref_ll[1], c[0], c[1])
        if d < bd:
            bd, best = d, c
    return best


def _normalize_fix_entry(v):
    """Accept [lat,lon] or [[lat,lon],...] from navdata."""
    if not v:
        return []
    if isinstance(v[0], (int, float)):
        return [(float(v[0]), float(v[1]))]
    out = []
    for pt in v:
        if pt and len(pt) >= 2:
            out.append((float(pt[0]), float(pt[1])))
    return out


def configure_navdata(fixes, airways, procedures=None, airports=None):
    """Load nav maps (for tests or after load_navdata())."""
    _navdata["fixes"] = fixes or {}
    _navdata["airways"] = airways or {}
    _navdata["procedures"] = procedures or {}
    _navdata["airports"] = airports or {}
    _navdata["loaded"] = True


def reset_navdata():
    _navdata["fixes"] = {}
    _navdata["airways"] = {}
    _navdata["procedures"] = {}
    _navdata["airports"] = {}
    _navdata["loaded"] = False


def _clean_token(t):
    return (t or "").split("/")[0].upper()


def parse_route_tokens(route):
    if not route:
        return []
    return [
        t
        for t in re.sub(r"[\n\r]", " ", route.upper()).split()
        if t and t not in ("DCT", "DIRECT", "SID", "STAR")
    ]


def _procedure_matches(proc, dep="", arr="", prefer=""):
    apts = [a.upper() for a in (proc or {}).get("apt") or []]
    if not apts:
        return True
    if prefer == "SID" and dep and dep in apts:
        return True
    if prefer == "STAR" and arr and arr in apts:
        return True
    if dep and dep in apts:
        return True
    if arr and arr in apts:
        return True
    return not (dep or arr)


def _find_procedure(proc_id, procedures, dep="", arr="", route_pos=0, n_tokens=0):
    key = _clean_token(proc_id)
    if not key:
        return None
    prefer = "SID" if route_pos < max(1, n_tokens // 3) else "STAR"
    if key in procedures:
        proc = procedures[key]
        if _procedure_matches(proc, dep, arr, prefer):
            return proc
    m = re.match(r"^([A-Z]{3,6})\d[A-Z]?$", key)
    if not m:
        return None
    pfx = m.group(1)
    matches = [k for k in procedures if k.startswith(pfx) and procedures[k].get("type")]
    if not matches:
        return None
    ranked = sorted(
        matches,
        key=lambda k: (
            0 if _procedure_matches(procedures[k], dep, arr, prefer) else 1,
            0 if key in k else 1,
            len(k),
        ),
    )
    pick = ranked[0]
    return procedures.get(pick)


def _merge_procedure_legs(trans_legs, common_legs):
    if not trans_legs:
        return common_legs or []
    if not common_legs:
        return trans_legs
    out = list(trans_legs)
    last_fix = trans_legs[-1][0]
    start = 1 if common_legs and common_legs[0][0] == last_fix else 0
    return out + common_legs[start:]


def _expand_procedure(proc, transition=None):
    if not proc:
        return []
    tr_name = _clean_token(transition) if transition else None
    if tr_name and proc.get("transitions", {}).get(tr_name):
        legs = _merge_procedure_legs(proc["transitions"][tr_name], proc.get("common") or [])
    elif proc.get("common") and len(proc["common"]) >= 2:
        legs = proc["common"]
    elif proc.get("w") and len(proc["w"]) >= 2:
        legs = proc["w"]
    else:
        return []
    return [(leg[0], leg[1], leg[2]) for leg in legs if leg and len(leg) >= 3]


def _apt_ll(icao, airports):
    icao = (icao or "").upper()
    if not icao:
        return None
    apt = airports.get(icao)
    if apt and len(apt) >= 2:
        return (float(apt[0]), float(apt[1]))
    return None


def _resolve_fix(name, fixes, ref_ll=None, dep="", arr="", airports=None):
    fid = _clean_token(name)
    if not fid or len(fid) < 2:
        return None
    if fid in ((dep or "").upper(), (arr or "").upper()):
        return None
    airports = airports or {}
    if not ref_ll:
        ref_ll = _apt_ll(dep, airports) or _apt_ll(arr, airports)
    if fid in fixes:
        cands = fixes[fid]
        ll = _nearest_candidate(cands, ref_ll)
        if ll:
            return {"name": fid, "lat": ll[0], "lon": ll[1]}
    return None


def _is_airway_token(t):
    return bool(_AWY_RE.match(_clean_token(t)))


def _airway_interior(seq, a, b):
    if a and b and a in seq and b in seq:
        i, j = seq.index(a), seq.index(b)
        return seq[i + 1 : j] if i <= j else list(reversed(seq[j + 1 : i]))
    return []


def _append_item(items, name, kind, lat=None, lon=None):
    if not name:
        return
    if items and items[-1]["name"] == name and items[-1].get("kind") == kind:
        return
    item = {"name": name, "kind": kind}
    if lat is not None and lon is not None:
        item["lat"] = lat
        item["lon"] = lon
    items.append(item)


def expand_route(route, dep="", arr="", navdata=None):
    """Ordered [{name, lat?, lon?, kind?}] for a filed route with airway + SID/STAR expansion."""
    nd = navdata if navdata is not None else _navdata
    fixes = nd.get("fixes") or {}
    airways = nd.get("airways") or {}
    procedures = nd.get("procedures") or {}
    airports = nd.get("airports") or {}
    dep = (dep or "").upper()
    arr = (arr or "").upper()

    tokens = parse_route_tokens(route)
    items = []
    ref_ll = _apt_ll(dep, airports) or _apt_ll(arr, airports)
    prev = None
    n = len(tokens)

    for i, raw in enumerate(tokens):
        tok = _clean_token(raw)
        if _COORD_RE.match(tok):
            continue

        next_tok = _clean_token(tokens[i + 1]) if i + 1 < len(tokens) else ""
        next_proc = _find_procedure(next_tok, procedures, dep, arr, i + 1, n) if next_tok else None

        if next_proc and next_proc.get("transitions", {}).get(tok):
            continue

        if _is_airway_token(tok):
            if tok in airways:
                nxt = None
                for j in range(i + 1, len(tokens)):
                    nt = _clean_token(tokens[j])
                    if not _is_airway_token(nt):
                        resolved = _resolve_fix(nt, fixes, ref_ll, dep, arr, airports)
                        if resolved:
                            nxt = resolved["name"]
                            break
                        if nt and len(nt) >= 2:
                            nxt = nt
                            break
                for f in _airway_interior(airways[tok], prev, nxt):
                    _append_item(items, f, "enroute")
                    prev = f
                    if f in fixes:
                        ll = _nearest_candidate(fixes[f], ref_ll)
                        if ll:
                            ref_ll = ll
                            items[-1]["lat"] = ll[0]
                            items[-1]["lon"] = ll[1]
            continue

        proc = _find_procedure(tok, procedures, dep, arr, i, n)
        if proc:
            prev_tok = _clean_token(tokens[i - 1]) if i > 0 else ""
            transition = prev_tok if proc.get("transitions", {}).get(prev_tok) else None
            kind = "sid" if proc.get("type") == "SID" else "star"
            for leg in _expand_procedure(proc, transition):
                _append_item(items, leg[0], kind, leg[1], leg[2])
                prev = leg[0]
                ref_ll = (leg[1], leg[2])
            continue

        m = re.match(r"^([A-Z]{2,6})\d[A-Z]?$", tok)
        if m:
            base = m.group(1)
            if base in fixes or not procedures:
                tok = base

        resolved = _resolve_fix(tok, fixes, ref_ll, dep, arr, airports)
        if resolved:
            _append_item(items, resolved["name"], "enroute", resolved["lat"], resolved["lon"])
            prev = resolved["name"]
            ref_ll = (resolved["lat"], resolved["lon"])
        elif re.match(r"^[A-Z]{2,6}$", tok):
            _append_item(items, tok, "enroute")
            prev = tok

    out = []
    for it in items:
        n = it["name"]
        if "lat" not in it and n in fixes:
            ll = _nearest_candidate(fixes[n], ref_ll)
            if ll:
                it = dict(it)
                it["lat"] = ll[0]
                it["lon"] = ll[1]
        out.append(it)
    return out
