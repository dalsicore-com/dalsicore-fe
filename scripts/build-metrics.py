#!/usr/bin/env python3
"""
Regenerate src/data/metrics.ts from the raw Google Play Console exports.

Source folder is the user's private data directory (NOT part of this repo):

    /home/baobaojingyi/Documents/Daftar Claude startup/Data aplikasi/<App>/
        Semua negara_daerah, <country>, <country>.csv

Each row of those CSVs is a day and each value is the Play Console
"installed audience" for that day (the number of devices that had the app
installed), per country plus a combined column.

The script aggregates a combined series across all apps, a per-country peak
table, and a per-app series, then downsamples everything to weekly samples
(Mondays) so the page stays light. Output is a single typed TS module.

Usage:
    python3 scripts/build-metrics.py
"""

import csv
import datetime
import json
import os
import re

SRC = "/home/baobaojingyi/Documents/Daftar Claude startup/Data aplikasi"
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
    out = []
    for i, (dt, v) in enumerate(pairs):
        if dt.weekday() == 0 or i == len(pairs) - 1:
            out.append((dt, v))
    return out


def main():
    apps = {}
    for folder in sorted(os.listdir(SRC)):
        path = os.path.join(SRC, folder)
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

    metrics = {
        "range": {"start": dates[0].isoformat(), "end": dates[-1].isoformat(), "days": len(dates)},
        "peak": {"date": peak[0].isoformat(), "value": peak[1]},
        "current": combined[-1][1],
        "appsTracked": len(apps),
        "countries": countries,
        "countriesCount": len(countries),
        "series": [{"d": d.isoformat(), "v": v} for d, v in weekly(combined)],
        "perApp": per_app,
    }

    ts = json.dumps
    L = []
    L.append("// Dalsicore metrics. Generated by scripts/build-metrics.py from the raw")
    L.append("// Google Play Console exports (see /home/baobaojingyi/Documents/Daftar Claude startup).")
    L.append("//")
    L.append("// METRIC DEFINITION: each value is the AUDIENCE OF USERS WITH THE APP INSTALLED")
    L.append('// on that day, the Play Console "installed audience" series, not a cumulative install')
    L.append(f"// count. It rises with installs and falls with uninstalls. Weekly samples cover {metrics['range']['start']} to {metrics['range']['end']}.")
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
    L.append("")
    L.append("export const METRICS = {")
    L.append(f'  range: {ts(metrics["range"])},')
    L.append(f'  peak: {ts(metrics["peak"])},')
    L.append(f'  current: {metrics["current"]},')
    L.append(f'  appsTracked: {metrics["appsTracked"]},')
    L.append(f'  countriesCount: {metrics["countriesCount"]},')
    L.append(f'  countries: {ts(metrics["countries"])} as CountryStat[],')
    L.append("  /** Combined installed audience across all tracked apps (weekly samples). */")
    L.append(f'  series: {ts(metrics["series"])} as MetricPoint[],')
    L.append("  perApp: {")
    for slug, v in per_app.items():
        L.append(f'    "{slug}": {{')
        L.append(f'      peak: {v["peak"]},')
        L.append(f'      peakDate: "{v["peakDate"]}",')
        L.append(f'      firstActive: {ts(v["firstActive"])},')
        L.append(f'      series: {ts(v["series"])} as MetricPoint[],')
        L.append(f'      countries: {ts(v["countries"])}')
        L.append("    },")
    L.append("  } as Record<string, AppMetric>,")
    L.append("};")
    L.append("")
    L.append("export const metricsFor = (slug: string): AppMetric | undefined => METRICS.perApp[slug];")

    open(OUT, "w").write("\n".join(L))
    print(f"wrote {OUT}")
    print(f"  apps={len(apps)} countries={len(countries)} peak={peak[1]} on {peak[0]} points={len(metrics['series'])}")


if __name__ == "__main__":
    main()
