#!/usr/bin/env python3
"""
Regenerate src/data/metrics.ts from the raw Google Play Console and
Google Analytics 4 / Firebase exports.

Two clearly separated layers:

  1. PLAY  - per-app "installed audience" (devices with the app installed), daily,
             2021-2026. Source: Data aplikasi/<App>/Semua negara_*.csv

  2. GA4   - analytics for the combined "Android App" property, 2020-2026:
             MAU/WAU/DAU, new users, countries, languages, ages, channels.
             Source: Firebase_overview.csv, Acquisition.csv,
                     User_attributes_overview.csv, Demographic_details_Country.csv

The two are different metrics measured by different tools. They are never
summed or mixed. Everything is downsampled to weekly samples (Mondays) so the
page stays light.

Usage:
    python3 scripts/build-metrics.py
"""

import csv
import datetime
import json
import os
import re

SRC = "/home/baobaojingyi/Documents/Daftar Claude startup"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "data", "metrics.ts")

MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Mei": 5, "Jun": 6,
          "Jul": 7, "Agu": 8, "Sep": 9, "Okt": 10, "Nov": 11, "Des": 12}

SLUG = {
    "Android Material Components": "android-material-components",
    "BookMan: Bookmark Manager": "bookman",
    "Compose Material Component": "compose-material-component",
    "Compose Material Design 3": "compose-material-design-3",
    "Financial Records": "financial-records",
    "Material Design 3 Android": "material-design-3-android",
    "MathQ: Math Riddle": "mathq",
    "NPuzzle - Sliding Puzzle": "npuzzle",
    "Staver": "staver",
    "Substracker": "substracker",
}

COUNTRY = {
    "Amerika Serikat": "United States", "Rusia": "Russia", "Jerman": "Germany",
    "India": "India", "Indonesia": "Indonesia", "Tiongkok": "China",
    "Turki": "Turkey", "Brasil": "Brazil", "Prancis": "France",
    "Filipina": "Philippines", "Ceko": "Czechia", "Mesir": "Egypt",
    "Bahrain": "Bahrain", "Hong Kong": "Hong Kong", "Jepang": "Japan",
    "Pakistan": "Pakistan",
}

GA4_START = datetime.date(2020, 9, 10)


def parse_date(s):
    m = re.match(r"(\d{1,2})\s+(\w+)\s+(\d{4})", s.strip())
    if not m:
        return None
    d, mon, y = m.groups()
    return datetime.date(int(y), MONTHS[mon], int(d)) if mon in MONTHS else None


def parse_int(x):
    x = (x or "").strip()
    if x in ("", "-"):
        return None
    try:
        return int(round(float(x.replace(",", "."))))
    except ValueError:
        return None


def weekly(pairs):
    return [p for i, p in enumerate(pairs) if p[0].weekday() == 0 or i == len(pairs) - 1]


def sections(path):
    """CSV exports put several tables in one file, separated by '#' comment rows."""
    rows = list(csv.reader(open(path, encoding="utf-8-sig", errors="replace")))
    out, cur = [], []
    for r in rows:
        if r and r[0].startswith("#"):
            if cur:
                out.append(cur)
                cur = []
            continue
        if r:
            cur.append(r)
    if cur:
        out.append(cur)
    return out


def nth(sec, col=1):
    """Map Nth-day index -> value for a daily export section."""
    out = {}
    for r in sec[1:]:
        try:
            out[int(r[0])] = float(r[col])
        except (ValueError, IndexError):
            pass
    return out


def day(k):
    return GA4_START + datetime.timedelta(days=k)


def build_play():
    apps = {}
    data_dir = os.path.join(SRC, "Data aplikasi")
    for folder in sorted(os.listdir(data_dir)):
        path = os.path.join(data_dir, folder)
        if not os.path.isdir(path) or folder not in SLUG:
            continue
        files = [f for f in os.listdir(path) if "Semua negara" in f]
        if not files:
            continue
        rows = list(csv.reader(open(os.path.join(path, files[0]), encoding="utf-8-sig")))
        ctry = [re.sub(r".*Harian\):\s*", "", h).strip() for h in rows[0][1:-1]]
        ctry = [c for c in ctry if c and c != "Semua negara/daerah"]
        series, by_country = {}, {COUNTRY.get(c, c): {} for c in ctry}
        for r in rows[1:]:
            dt = parse_date(r[0])
            if not dt:
                continue
            total = parse_int(r[1])
            if total is not None:
                series[dt] = total
            for i, c in enumerate(ctry):
                v = parse_int(r[2 + i]) if 2 + i < len(r) else None
                if v is not None:
                    by_country[COUNTRY.get(c, c)][dt] = v
        apps[SLUG[folder]] = {"series": series, "countries": by_country}

    dates = sorted(set().union(*[set(a["series"]) for a in apps.values()]))
    combined = [(dt, sum(a["series"].get(dt, 0) for a in apps.values())) for dt in dates]
    peak = max(combined, key=lambda x: x[1])

    agg = {}
    for a in apps.values():
        for c, cs in a["countries"].items():
            if not cs:
                continue
            e = agg.setdefault(c, {"peak": 0, "latest": 0, "apps": 0})
            e["peak"] += max(cs.values())
            e["latest"] += cs[max(cs)]
            e["apps"] += 1
    countries = sorted([{"name": k, **v} for k, v in agg.items()], key=lambda x: -x["peak"])

    per_app = {}
    for slug, a in apps.items():
        s = a["series"]
        nz = [dt for dt in sorted(s) if s[dt] > 0]
        cpp = sorted(
            [{"name": c, "peak": max(cs.values()), "latest": cs[max(cs)]}
             for c, cs in a["countries"].items() if cs],
            key=lambda x: -x["peak"],
        )
        per_app[slug] = {
            "peak": max(s.values()),
            "peakDate": max(s, key=s.get).isoformat(),
            "firstActive": nz[0].isoformat() if nz else None,
            "series": [{"d": d.isoformat(), "v": v} for d, v in weekly(sorted(s.items()))],
            "countries": cpp,
        }

    return {
        "range": {"start": dates[0].isoformat(), "end": dates[-1].isoformat(), "days": len(dates)},
        "peak": {"date": peak[0].isoformat(), "value": peak[1]},
        "current": combined[-1][1],
        "appsTracked": len(apps),
        "countries": countries,
        "countriesCount": len(countries),
        "series": [{"d": d.isoformat(), "v": v} for d, v in weekly(combined)],
        "perApp": per_app,
    }


def build_ga4():
    fb = sections(os.path.join(SRC, "Firebase_overview.csv"))
    acq = sections(os.path.join(SRC, "Acquisition.csv"))
    attrs = sections(os.path.join(SRC, "User_attributes_overview.csv"))
    dem = [r for r in csv.reader(open(os.path.join(SRC, "Demographic_details_Country.csv"), encoding="utf-8-sig"))
           if r and not r[0].startswith("#")]

    mau, wau, dau = nth(fb[0], 1), nth(fb[0], 2), nth(fb[0], 3)
    newu = nth(acq[0], 1)
    rev_total = nth(fb[14], 1)
    rev_purchase = nth(fb[15], 1)
    rev_ads = nth(fb[16], 1)

    def peak(d):
        k = max(d, key=lambda x: d[x])
        return {"date": day(k).isoformat(), "value": round(d[k])}

    countries = []
    rev_idx = dem[0].index("Total revenue") if "Total revenue" in dem[0] else None
    for r in dem[1:]:
        try:
            countries.append({
                "name": r[0],
                "active": int(r[1]),
                "newUsers": int(r[2]),
                "engagementRate": round(float(r[4]), 3),
                "engagementSeconds": round(float(r[6])),
                "revenue": round(float(r[rev_idx])) if rev_idx is not None else 0,
            })
        except (ValueError, IndexError):
            pass
    countries = sorted(countries, key=lambda x: -x["active"])[:14]

    total_rev = round(sum(rev_total.values()))
    ad_rev = round(sum(rev_ads.values()))
    purchase_rev = round(sum(rev_purchase.values()))
    rev_by_country = sorted(
        [{"name": c["name"], "v": c["revenue"]} for c in countries if c["revenue"] > 0],
        key=lambda x: -x["v"],
    )

    mau_pairs = sorted((day(k), v) for k, v in mau.items())
    new_pairs = sorted((day(k), v) for k, v in newu.items())

    return {
        "range": {"start": day(min(mau)).isoformat(), "end": day(max(mau)).isoformat()},
        "peak": {"mau": peak(mau), "wau": peak(wau), "dau": peak(dau), "newUsers": peak(newu)},
        "newUsersTotal": round(sum(newu.values())),
        "latest": {"mau": round(mau[max(mau)]), "wau": round(wau[max(wau)]), "dau": round(dau[max(dau)])},
        "countriesCount": len(dem) - 1,
        "series": [{"d": d.isoformat(), "v": round(v)} for d, v in weekly(mau_pairs)],
        "newSeries": [{"d": d.isoformat(), "v": round(v)} for d, v in weekly(new_pairs) if v > 0],
        "countries": countries,
        "revenue": {
            "currency": "IDR",
            "total": total_rev,
            "ads": ad_rev,
            "purchases": purchase_rev,
            "adShare": round(ad_rev / total_rev, 3) if total_rev else 0,
            "countries": rev_by_country[:8],
        },
        "languages": [{"name": r[0], "v": int(r[1])} for r in attrs[6][1:7]],
        "ages": [{"name": r[0], "v": int(r[1])} for r in attrs[5][1:]],
        "channels": [{"name": r[0], "v": int(r[1])} for r in acq[1][1:]],
    }


def emit(play, ga4):
    ts = json.dumps
    L = []
    L.append("// Dalsicore metrics. Generated by scripts/build-metrics.py.")
    L.append("//")
    L.append("// Two layers, never mixed:")
    L.append("//   PLAY - Google Play Console 'installed audience' per app (devices with the")
    L.append("//          app installed on a given day), 2021-2026.")
    L.append("//   GA4  - Google Analytics / Firebase for the combined Android property:")
    L.append("//          MAU/WAU/DAU, new users, countries, languages, ages, channels, 2020-2026.")
    L.append("//")
    L.append("// Weekly samples (Mondays). See /home/baobaojingyi/Documents/Daftar Claude startup")
    L.append("// for the raw exports.")
    L.append("")
    L.append("export interface MetricPoint { d: string; v: number }")
    L.append("export interface CountryStat { name: string; peak: number; latest: number; apps: number }")
    L.append("export interface AppMetric {")
    L.append("  peak: number;")
    L.append("  peakDate: string;")
    L.append("  firstActive: string | null;")
    L.append("  series: MetricPoint[];")
    L.append("  countries: { name: string; peak: number; latest: number }[];")
    L.append("}")
    L.append("export interface Ga4Country {")
    L.append("  name: string;")
    L.append("  active: number;")
    L.append("  newUsers: number;")
    L.append("  engagementRate: number;")
    L.append("  engagementSeconds: number;")
    L.append("  revenue: number;")
    L.append("}")
    L.append("export interface Ga4Revenue {")
    L.append("  currency: string;")
    L.append("  total: number;")
    L.append("  ads: number;")
    L.append("  purchases: number;")
    L.append("  adShare: number;")
    L.append("  countries: Labeled[];")
    L.append("}")
    L.append("export interface Labeled { name: string; v: number }")
    L.append("export interface PeakPoint { date: string; value: number }")
    L.append("")
    L.append("export const METRICS = {")
    L.append(f'  range: {ts(play["range"])},')
    L.append(f'  peak: {ts(play["peak"])},')
    L.append(f'  current: {play["current"]},')
    L.append(f'  appsTracked: {play["appsTracked"]},')
    L.append(f'  countriesCount: {play["countriesCount"]},')
    L.append(f'  countries: {ts(play["countries"])} as CountryStat[],')
    L.append("  /** Combined installed audience across all tracked apps (weekly). */")
    L.append(f'  series: {ts(play["series"])} as MetricPoint[],')
    L.append("  perApp: {")
    for slug, v in play["perApp"].items():
        L.append(f'    "{slug}": {{')
        L.append(f'      peak: {v["peak"]},')
        L.append(f'      peakDate: "{v["peakDate"]}",')
        L.append(f'      firstActive: {ts(v["firstActive"])},')
        L.append(f'      series: {ts(v["series"])} as MetricPoint[],')
        L.append(f'      countries: {ts(v["countries"])}')
        L.append("    },")
    L.append("  } as Record<string, AppMetric>,")
    L.append("")
    L.append("  ga4: {")
    L.append(f'    range: {ts(ga4["range"])},')
    L.append(f'    peak: {ts(ga4["peak"])},')
    L.append(f'    newUsersTotal: {ga4["newUsersTotal"]},')
    L.append(f'    latest: {ts(ga4["latest"])},')
    L.append(f'    countriesCount: {ga4["countriesCount"]},')
    L.append(f'    series: {ts(ga4["series"])} as MetricPoint[],')
    L.append(f'    newSeries: {ts(ga4["newSeries"])} as MetricPoint[],')
    L.append(f'    countries: {ts(ga4["countries"])} as Ga4Country[],')
    L.append(f'    revenue: {ts(ga4["revenue"])} as Ga4Revenue,')
    L.append(f'    languages: {ts(ga4["languages"])} as Labeled[],')
    L.append(f'    ages: {ts(ga4["ages"])} as Labeled[],')
    L.append(f'    channels: {ts(ga4["channels"])} as Labeled[]')
    L.append("  }")
    L.append("};")
    L.append("")
    L.append("export const metricsFor = (slug: string): AppMetric | undefined => METRICS.perApp[slug];")
    open(OUT, "w").write("\n".join(L))


def main():
    play = build_play()
    ga4 = build_ga4()
    emit(play, ga4)
    print(f"wrote {OUT}")
    print(f"  PLAY apps={play['appsTracked']} countries={play['countriesCount']} "
          f"peak={play['peak']['value']} on {play['peak']['date']} points={len(play['series'])}")
    print(f"  GA4  peak_mau={ga4['peak']['mau']['value']} new_users_total={ga4['newUsersTotal']} "
          f"countries={ga4['countriesCount']}")


if __name__ == "__main__":
    main()
