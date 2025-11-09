from __future__ import annotations
from pathlib import Path
from typing import List, Dict

def load_all_feeds(feeds_dir: Path) -> List[str]:
    """
    Lê todos os .txt do diretório, uma URL por linha, ignora linhas vazias/comentadas.
    Retorna uma lista plana de URLs (sem duplicatas) — pronto para fetch_headlines.
    """
    urls: List[str] = []
    for p in sorted(feeds_dir.glob("*.txt")):
        text = p.read_text(encoding="utf-8")
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)
    # dedup preservando ordem
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            out.append(u)
            seen.add(u)
    return out

def load_feeds_by_category(feeds_dir: Path) -> Dict[str, List[str]]:
    """
    Opcional: se quiser manter mapeamento categoria→URLs.
    """
    mapping: Dict[str, List[str]] = {}
    for p in sorted(feeds_dir.glob("*.txt")):
        cat = p.stem  # policy, regulation, ...
        urls: List[str] = []
        text = p.read_text(encoding="utf-8")
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)
        # dedup local
        mapping[cat] = list(dict.fromkeys(urls))
    return mapping