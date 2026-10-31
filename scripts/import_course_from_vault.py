#!/usr/bin/env python3
"""
Importa markdown do vault Obsidian para o repo open-source.

- Copia aulas → modules/MXX-.../lessons/
- Copia resumo/guia/overview → modules/MXX-.../study/
- Copia CSV de tópicos → docs/
- NÃO copia mídia pesada (mp4/m4a/pptx/pdf/png ~1.3GB)
- Limpa frontmatter Obsidian e rebrand leve para @mosscardoso

Uso:
  python scripts/import_course_from_vault.py
  python scripts/import_course_from_vault.py --vault "/caminho/para/Econofisica — mosscardoso"
"""

from __future__ import annotations

import argparse
import re
import shutil
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

DEFAULT_VAULT = Path(
    "/Users/hardwork/Library/CloudStorage/"
    "GoogleDrive-matheuscbsmsn1994@gmail.com/Meu Drive/Obsidian Vault/"
    "Obsidian Vault/Pesquisas/02 - Mercados e Quant/Sistemas Quant/"
    "Econofisica — mosscardoso"
)

MODULE_DIRS = {
    "M01": "M01-fundamentos",
    "M02": "M02-dinamica-gregas",
    "M03": "M03-curva-juros",
    "M04": "M04-superficie-vol",
    "M05": "M05-econofisica-entropia",
    "M06": "M06-histerese-caudas",
    "M07": "M07-portfolio-fatores",
    "M08": "M08-variancia-garch",
    "M09": "M09-labs-beta-fragilidade",
    "M10": "M10-capstone-janus",
}


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def slugify_lesson(name: str) -> str:
    """M01-A01 — Título.md → A01-titulo.md"""
    stem = Path(name).stem
    stem = nfc(stem)
    m = re.match(r"^(M\d{2})-A(\d{2})\s*[—\-–]\s*(.+)$", stem)
    if not m:
        safe = re.sub(r"[^\w\-]+", "-", stem, flags=re.UNICODE).strip("-").lower()
        return f"{safe}.md"
    num, title = m.group(2), m.group(3)
    title = title.replace(":", " -")
    title = re.sub(r"[“”\"']", "", title)
    title = re.sub(r"\s+", "-", title.strip())
    title = re.sub(r"[^\w\-]+", "", title, flags=re.UNICODE)
    title = re.sub(r"-{2,}", "-", title).strip("-").lower()
    # ascii fold light
    title = (
        unicodedata.normalize("NFKD", title)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    title = re.sub(r"-{2,}", "-", title).strip("-")
    return f"A{num}-{title}.md"


def strip_obsidian_frontmatter(text: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = {}
    if not text.startswith("---"):
        return meta, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return meta, text
    fm, body = parts[1], parts[2].lstrip("\n")
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, body


def clean_body(body: str, module_id: str, lesson_id: str | None = None) -> str:
    body = nfc(body)
    # remove heavy Obsidian wikilinks chrome at top → keep readable titles
    body = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", body)
    body = re.sub(r"\[\[([^\]]+)\]\]", r"\1", body)
    # callouts → blockquotes
    body = re.sub(r">\s*\[!(\w+)\][^\n]*\n", r"> **\1**\n>\n", body)
    # rebrand public-facing mentions
    body = body.replace("@khemkapital", "@mosscardoso (curso) / fonte histórica @khemkapital")
    body = re.sub(
        r"Karim Khemiri\s*/\s*Khem Kapital",
        "fonte histórica: Karim Khemiri / Khem Kapital",
        body,
        flags=re.IGNORECASE,
    )
    # drop NotebookLM proprietary banner lines that discourage open sharing
    # keep educational content; add course header
    header_bits = [
        f"> **Curso:** [econofisica](https://github.com/matheuscbs/econofisica) · [@mosscardoso](https://instagram.com/mosscardoso)",
        f"> **Módulo:** {module_id}",
    ]
    if lesson_id:
        header_bits.append(f"> **Aula:** {lesson_id}")
    header = "\n".join(header_bits) + "\n\n"
    # if body already starts with # title, insert after first heading line
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0] + "\n\n" + header + "\n".join(lines[1:]).lstrip("\n")
    return header + body


def find_module_dir(vault: Path, mid: str) -> Path | None:
    mod_root = vault / "modulos"
    if not mod_root.exists():
        return None
    for d in mod_root.iterdir():
        if d.is_dir() and nfc(d.name).startswith(mid):
            return d
    return None


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def import_lessons(vault: Path) -> int:
    aulas = vault / "aulas"
    n = 0
    for src in sorted(aulas.glob("*.md")):
        name = nfc(src.name)
        m = re.match(r"^(M\d{2})-A(\d{2})", name)
        if not m:
            print(f"  skip (pattern): {src.name}")
            continue
        mid = m.group(1)
        lid = f"{mid}.A{m.group(2)}"
        dest_dir = REPO / "modules" / MODULE_DIRS[mid] / "lessons"
        dest = dest_dir / slugify_lesson(name)
        raw = src.read_text(encoding="utf-8")
        _, body = strip_obsidian_frontmatter(raw)
        out = clean_body(body, mid, lid)
        # prepend provenance
        out = (
            f"<!-- imported from vault study notes; curated for open course -->\n"
            f"{out}"
        )
        write_text(dest, out)
        print(f"  lesson {lid:8} → {dest.relative_to(REPO)}")
        n += 1
    return n


def import_study(vault: Path) -> int:
    n = 0
    for mid, folder in MODULE_DIRS.items():
        src_dir = find_module_dir(vault, mid)
        if not src_dir:
            print(f"  missing module folder for {mid}")
            continue
        study_dir = REPO / "modules" / folder / "study"
        study_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted(src_dir.glob("*.md")):
            raw = src.read_text(encoding="utf-8")
            _, body = strip_obsidian_frontmatter(raw)
            sname = nfc(src.name)
            if sname.startswith("Resumo"):
                dest_name = "resumo.md"
            elif sname.startswith("Guia Completo"):
                dest_name = "guia-completo.md"
            elif sname.startswith(mid):
                dest_name = "overview.md"
            else:
                dest_name = slugify_lesson(sname)
            out = clean_body(body, mid)
            out = f"<!-- imported study note ({dest_name}) -->\n{out}"
            dest = study_dir / dest_name
            write_text(dest, out)
            print(f"  study  {mid} {dest_name:16} ← {sname[:50]}")
            n += 1

        # placeholder for media (not committed)
        assets_readme = study_dir / "ASSETS.md"
        write_text(
            assets_readme,
            f"""# Assets do módulo {mid}

Mídia gerada no vault (podcast, vídeo, slides, PDF) **não entra no Git** (~1.3 GB no total).

Guarde localmente ou use Git LFS se for publicar depois:

| Tipo | Origem no vault |
|------|-----------------|
| podcast `.m4a` | `modulos/{mid}*/assets/` |
| vídeo `.mp4` | idem |
| slides `.pptx` / `.pdf` | idem |
| stories `.png` | idem |

No curso open-source preferimos **animações Manim** geradas a partir dos labs (reproduzíveis).
""",
        )
    return n


def import_docs(vault: Path) -> None:
    csv_src = vault / "assets" / "curso-econofisica-topicos.csv"
    if csv_src.exists():
        dest = REPO / "docs" / "curriculum-topics.csv"
        shutil.copy2(csv_src, dest)
        print(f"  docs   → {dest.relative_to(REPO)}")

    # course map at root of content
    index_src = vault / "00 - Índice das aulas.md"
    if index_src.exists():
        raw = index_src.read_text(encoding="utf-8")
        _, body = strip_obsidian_frontmatter(raw)
        out = clean_body(body, "CURSO")
        write_text(REPO / "docs" / "mapa-aulas.md", f"<!-- course map -->\n{out}")
        print("  docs   → docs/mapa-aulas.md")


def update_module_readmes() -> None:
    """Enrich each module README with links to lessons/."""
    for mid, folder in MODULE_DIRS.items():
        mod = REPO / "modules" / folder
        lessons = sorted((mod / "lessons").glob("A*.md")) if (mod / "lessons").exists() else []
        study = mod / "study"
        readme = mod / "README.md"
        existing = readme.read_text(encoding="utf-8") if readme.exists() else f"# {mid}\n"
        # remove previous auto block if any
        existing = re.sub(
            r"\n## Conteúdo importado\n.*?(?=\n## |\Z)",
            "\n",
            existing,
            flags=re.S,
        )
        lines = ["\n## Conteúdo importado\n"]
        if lessons:
            lines.append("### Aulas\n")
            for p in lessons:
                title = p.stem
                lines.append(f"- [{title}](lessons/{p.name})")
            lines.append("")
        if study.exists():
            lines.append("### Estudo\n")
            for name, label in [
                ("overview.md", "Overview do módulo"),
                ("resumo.md", "Resumo executivo"),
                ("guia-completo.md", "Guia completo"),
                ("ASSETS.md", "Assets (mídia local)"),
            ]:
                if (study / name).exists():
                    lines.append(f"- [{label}](study/{name})")
            lines.append("")
        labs = mod / "labs"
        if labs.exists() and any(labs.iterdir()):
            lines.append("### Labs\n")
            for d in sorted(labs.iterdir()):
                if d.is_dir():
                    lines.append(f"- [{d.name}](labs/{d.name}/)")
            lines.append("")
        write_text(readme, existing.rstrip() + "\n" + "\n".join(lines))
        print(f"  readme → modules/{folder}/README.md")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", type=Path, default=DEFAULT_VAULT)
    args = ap.parse_args()
    vault = args.vault
    if not vault.exists():
        raise SystemExit(f"Vault não encontrado: {vault}")

    print(f"Vault: {vault}")
    print(f"Repo:  {REPO}")
    print("\n[lessons]")
    n_l = import_lessons(vault)
    print(f"\n[study] ({n_l} lessons done)")
    n_s = import_study(vault)
    print("\n[docs]")
    import_docs(vault)
    print("\n[module READMEs]")
    update_module_readmes()
    print(f"\nOK — {n_l} aulas, {n_s} notas de estudo.")


if __name__ == "__main__":
    main()
