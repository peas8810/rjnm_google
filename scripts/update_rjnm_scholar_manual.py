from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("rjnm-scholar.json")

def parse_series(text: str):
    out = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        y, v = line.split("=", 1)
        y = y.strip()
        v = v.strip().replace(",", ".")
        try:
            out.append({"year": str(int(y)), "value": float(v) if "." in v else int(v)})
        except Exception:
            pass
    out.sort(key=lambda x: int(x["year"]))
    return out

def to_int(s: str | None, default=0) -> int:
    s = (s or "").strip()
    if not s: return default
    s = s.replace(".", "").replace(",", ".")
    try: return int(float(s))
    except Exception: return default

def main():
    import os
    payload = {
        "source": os.getenv("SOURCE", "https://scholar.google.com/"),
        "profile_name": os.getenv("PROFILE_NAME", "RJNM (Google Scholar)"),
        "updated_at": datetime.now(timezone.utc).date().isoformat(),
        "metrics": {
            "citations_all": to_int(os.getenv("CITATIONS_ALL")),
            "citations_5y": to_int(os.getenv("CITATIONS_5Y")),
            "h_index_all": to_int(os.getenv("H_INDEX_ALL")),
            "h_index_5y": to_int(os.getenv("H_INDEX_5Y")),
            "i10_index_all": to_int(os.getenv("I10_INDEX_ALL")),
            "i10_index_5y": to_int(os.getenv("I10_INDEX_5Y")),
        },
        "citations_by_year": parse_series(os.getenv("CITATIONS_BY_YEAR", "")),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK: rjnm-scholar.json atualizado.")

if __name__ == "__main__":
    main()
