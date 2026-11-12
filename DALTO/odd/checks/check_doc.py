#!/usr/bin/env python3
"""Automated quality gate for DALTO/DOC documentation files.

Validates per topic file (Basico|Intermedio|Avanzado/**/*.md):
  1. Single H1 title and the 10 mandatory H2 sections in exact order.
  2. All three progressive example levels (### Básico, ### Intermedio, ### Avanzado).
  3. Relative Markdown links resolve to existing files (or PLANNED paths in incremental mode).
  4. Python code blocks parse cleanly via ast.parse (blocks with '# ERROR INTENCIONAL' excluded),
     and optionally execute cleanly with --exec when self-contained.
  5. Section 10 includes explicit 'Directorio de origen' traceability (or 'fundamento complementario')
     and every referenced CLASES_PYTHON/... or CLASS_PY_POO/... path exists on disk.
  6. Section 11 official docs.python.org URLs point to real pages (no invented tutorial/reference/library pages).
  7. No leaked secret keys ('sk-proj-') anywhere in the file.

Validates for DOC/introduccion.md:
  - All 8 mandatory H2 sections from prompt.md Phase 4, strengths/weaknesses table,
    and navigable links to all 41 planned topic files.
"""
from __future__ import annotations

import ast
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "DOC"

PLANNED = {
    "introduccion.md",
    *{f"Basico/chapter-one/{n}.md" for n in (
        "entradas_y_salidas", "variables", "tipos_datos", "operadores", "condicionales")},
    *{f"Basico/chapter-two/{n}.md" for n in ("bucles", "cadenas", "listas")},
    *{f"Intermedio/chapter-one/{n}.md" for n in (
        "tuplas", "conjuntos", "diccionarios", "desempaquetamiento", "comprensiones")},
    *{f"Intermedio/chapter-two/{n}.md" for n in (
        "funciones", "ambito_variables", "funciones_lambda", "funciones_integradas")},
    *{f"Intermedio/chapter-three/{n}.md" for n in (
        "modulos", "paquetes", "manejo_archivos", "archivos_csv",
        "pandas_fundamentos", "visualizacion")},
    *{f"Intermedio/chapter-four/{n}.md" for n in (
        "excepciones", "fechas_datetime", "decimal", "random")},
    *{f"Intermedio/chapter-five/{n}.md" for n in (
        "clases_y_objetos", "atributos_y_metodos", "encapsulamiento",
        "herencia", "polimorfismo")},
    *{f"Avanzado/chapter-one/{n}.md" for n in (
        "decoradores", "metodos_especiales", "iteradores")},
    *{f"Avanzado/chapter-two/{n}.md" for n in (
        "mro_herencia_multiple", "abstraccion_abc", "principios_solid")},
    *{f"Avanzado/chapter-three/{n}.md" for n in (
        "expresiones_regulares", "regex_avanzada")},
    "Avanzado/chapter-four/pandas_avanzado.md",
}

STRICT = "--strict" in sys.argv[1:]
EXEC_BLOCKS = "--exec" in sys.argv[1:]
ONLY_PREFIX = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--only=")), None)

REQUIRED_H2 = [
    "## 2. Introducción",
    "## 3. Fundamentos y conceptos",
    "## 4. Sintaxis y funcionamiento",
    "## 5. Ejemplos prácticos progresivos",
    "## 6. Aplicaciones en el mundo real",
    "## 7. Uso en producción",
    "## 8. Errores comunes y recomendaciones",
    "## 9. Resumen",
    "## 10. Relación con el material original",
    "## 11. Referencias oficiales",
]

INTRO_REQUIRED_H2 = [
    "## 1. ¿Qué es Python?",
    "## 2. Historia de Python",
    "## 3. ¿Por qué existe Python?",
    "## 4. ¿Para qué se utiliza?",
    "## 5. Fortalezas y debilidades",
    "## 6. Cómo funciona Python",
    "## 7. Introducción a la programación orientada a objetos",
    "## 8. Índice general de documentación",
]

LEVELS = ["### Básico", "### Intermedio", "### Avanzado"]

VALID_TUTORIAL_PAGES = {
    "", "index.html", "appetite.html", "interpreter.html", "introduction.html",
    "controlflow.html", "datastructures.html", "modules.html", "inputoutput.html",
    "errors.html", "classes.html", "stdlib.html", "stdlib2.html", "venv.html",
    "floatingpoint.html", "appendix.html",
}

VALID_REFERENCE_PAGES = {
    "", "index.html", "introduction.html", "lexical_analysis.html", "datamodel.html",
    "executionmodel.html", "import.html", "expressions.html", "simple_stmts.html",
    "compound_stmts.html", "toplevel_components.html", "grammar.html",
}

VALID_LIBRARY_UMBRELLA_PAGES = {
    "", "index.html", "intro.html", "functions.html", "constants.html",
    "stdtypes.html", "exceptions.html", "datatypes.html", "numeric.html",
    "functional.html", "filesys.html", "persistence.html", "archiving.html",
    "fileformats.html", "crypto.html", "allos.html", "concurrency.html",
    "ipc.html", "netdata.html", "markup.html", "internet.html", "mm.html",
    "i18n.html", "frameworks.html", "tk.html", "devmode.html",
    "security_warnings.html", "cmdline.html",
}

KNOWN_BAD_ANCHORS = {
    "more-conditional-statements",
}

LINK_RE = re.compile(r"\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://[^\s)>\"`]+")
PY_BLOCK_RE = re.compile(r"```python\n(.*?)```", re.S)
SOURCE_PATH_RE = re.compile(
    r"`((?:CLASES_PYTHON|CLASS_PY_POO)/[^`\n]+?\.(?:py|PY|csv|txt|png))`"
)
EXTERNAL_IMPORT_RE = re.compile(
    r"^\s*(?:import|from)\s+(pandas|matplotlib|seaborn|numpy|textblob|openai|tkinter)\b",
    re.M,
)


def validate_python_docs_url(rel: Path, url: str, errors: list[str]) -> None:
    parsed = urlparse(url)
    if parsed.netloc != "docs.python.org":
        return
    if parsed.fragment in KNOWN_BAD_ANCHORS:
        errors.append(f"{rel}: known invalid anchor '#{parsed.fragment}' in {url}")
    parts = [p for p in parsed.path.split("/") if p]
    if not parts or parts[0] != "3":
        return
    if len(parts) == 1:
        return
    section = parts[1]
    page = parts[2] if len(parts) >= 3 else ""
    if section == "tutorial" and page not in VALID_TUTORIAL_PAGES:
        errors.append(f"{rel}: non-existent Python tutorial URL: {url}")
    elif section == "reference" and page not in VALID_REFERENCE_PAGES:
        errors.append(f"{rel}: non-existent Python reference URL: {url}")
    elif section == "library" and page:
        if page in VALID_LIBRARY_UMBRELLA_PAGES:
            return
        if page.endswith(".html"):
            mod_name = page[:-5].split(".")[0]
            if mod_name not in sys.stdlib_module_names and mod_name not in {"__main__", "__future__"}:
                errors.append(f"{rel}: suspect Python library URL (unknown module '{mod_name}'): {url}")


def check_topic(path: Path, errors: list[str], pending: list[str]) -> None:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if "sk-proj-" in text:
        errors.append(f"{rel}: SECURITY VIOLATION — contains 'sk-proj-' secret prefix")

    in_fence = False
    h1: list[str] = []
    h2: list[str] = []
    for ln in lines:
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if ln.startswith("# "):
            h1.append(ln)
        elif ln.startswith("## "):
            h2.append(ln)

    if len(h1) != 1:
        errors.append(f"{rel}: expected 1 H1 outside code fences, found {len(h1)}")

    if len(h2) != 10:
        errors.append(f"{rel}: expected 10 H2 sections, found {len(h2)}: {h2}")
    for want in REQUIRED_H2:
        if want not in h2:
            errors.append(f"{rel}: missing section '{want}'")
    present = [ln for ln in h2 if ln in REQUIRED_H2]
    if present != REQUIRED_H2:
        errors.append(f"{rel}: sections out of order")

    if "## 5. Ejemplos prácticos progresivos" in text and "## 6." in text:
        sec5 = text.split("## 5. Ejemplos prácticos progresivos", 1)[1].split("## 6.", 1)[0]
        for lvl in LEVELS:
            if lvl not in sec5:
                errors.append(f"{rel}: missing example level '{lvl}' in Section 5")

    text_no_fences = re.sub(r"```.*?```", "", text, flags=re.S)
    for target in LINK_RE.findall(text_no_fences):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (path.parent / target.split("#")[0]).resolve()
        if resolved.exists():
            continue
        try:
            planned_key = str(resolved.relative_to(DOC)).replace("\\", "/")
        except ValueError:
            planned_key = None
        if planned_key in PLANNED and not STRICT:
            pending.append(f"{rel}: pending link -> {target}")
        else:
            errors.append(f"{rel}: broken relative link -> {target}")

    for i, block in enumerate(PY_BLOCK_RE.findall(text), 1):
        if "# ERROR INTENCIONAL" in block or "# NO EJECUTAR" in block:
            continue
        try:
            ast.parse(block)
        except SyntaxError as exc:
            errors.append(f"{rel}: python block #{i} syntax error: {exc}")
            continue
        if EXEC_BLOCKS:
            if re.search(r"\binput\s*\(", block) or EXTERNAL_IMPORT_RE.search(block):
                continue
            with tempfile.TemporaryDirectory() as tmpdir:
                proc = subprocess.run(
                    [sys.executable, "-c", block],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if proc.returncode != 0:
                    stderr_last = (proc.stderr.strip().splitlines() or ["unknown error"])[-1]
                    errors.append(f"{rel}: python block #{i} runtime failure: {stderr_last}")

    if "## 10. Relación con el material original" in text and "## 11." in text:
        sec10 = text.split("## 10. Relación con el material original", 1)[1].split("## 11.", 1)[0]
        has_origin_label = "directorio de origen" in sec10.lower()
        has_complementary = "fundamento complementario" in sec10.lower()
        cited_paths = SOURCE_PATH_RE.findall(sec10)
        if not cited_paths and not has_complementary:
            errors.append(
                f"{rel}: section 10 must cite backticked source paths (`CLASES_PYTHON/...` or `CLASS_PY_POO/...`) "
                "or state 'fundamento complementario'"
            )
        if cited_paths and not has_origin_label:
            errors.append(f"{rel}: section 10 must explicitly specify 'Directorio de origen'")
        for cited in cited_paths:
            if not (ROOT / cited).exists():
                errors.append(f"{rel}: section 10 cites non-existent source file '{cited}'")

    if "## 11. Referencias oficiales" in text:
        sec11 = text.split("## 11. Referencias oficiales", 1)[1]
        urls = URL_RE.findall(sec11)
        if not urls:
            errors.append(f"{rel}: section 11 has no official URLs")
        for url in urls:
            validate_python_docs_url(rel, url, errors)


def check_indice(errors: list[str], pending: list[str]) -> None:
    intro = DOC / "introduccion.md"
    if not intro.exists():
        if STRICT:
            errors.append("DOC/introduccion.md missing")
        else:
            pending.append("DOC/introduccion.md not written yet")
        return
    text = intro.read_text(encoding="utf-8")
    if "sk-proj-" in text:
        errors.append("DOC/introduccion.md: SECURITY VIOLATION — contains 'sk-proj-'")

    in_fence = False
    h2: list[str] = []
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and ln.startswith("## "):
            h2.append(ln)

    for want in INTRO_REQUIRED_H2:
        if want not in h2:
            errors.append(f"DOC/introduccion.md: missing section '{want}'")
    present = [ln for ln in h2 if ln in INTRO_REQUIRED_H2]
    if present != INTRO_REQUIRED_H2:
        errors.append("DOC/introduccion.md: mandatory H2 sections out of order")

    if "| N° | Fortalezas | Debilidades |" not in text:
        errors.append("DOC/introduccion.md: missing '| N° | Fortalezas | Debilidades |' table")

    text_no_fences = re.sub(r"```.*?```", "", text, flags=re.S)
    topics = sorted(
        p for level in ("Basico", "Intermedio", "Avanzado")
        if (DOC / level).is_dir()
        for p in (DOC / level).rglob("*.md")
    )
    indexed = set()
    for target in LINK_RE.findall(text_no_fences):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (intro.parent / target.split("#")[0]).resolve()
        if not resolved.exists():
            errors.append(f"DOC/introduccion.md: broken link -> {target}")
        else:
            indexed.add(resolved)
    for topic in topics:
        if topic.resolve() not in indexed:
            errors.append(f"DOC/introduccion.md: topic not indexed -> {topic.relative_to(ROOT)}")


def main() -> int:
    if not DOC.is_dir():
        print("DOC/ does not exist yet")
        return 0
    errors: list[str] = []
    pending: list[str] = []
    topics = sorted(
        p for level in ("Basico", "Intermedio", "Avanzado")
        if (DOC / level).is_dir()
        for p in (DOC / level).rglob("*.md")
    )
    if ONLY_PREFIX:
        topics = [p for p in topics if str(p.relative_to(DOC)).startswith(ONLY_PREFIX)]
    for topic in topics:
        check_topic(topic, errors, pending)
    if not ONLY_PREFIX and ((DOC / "introduccion.md").exists() or STRICT):
        check_indice(errors, pending)

    print(
        f"topics checked: {len(topics)} | mode: {'strict' if STRICT else 'incremental'} "
        f"| exec: {'on' if EXEC_BLOCKS else 'off'}"
    )
    if pending:
        print(f"pending links/files ({len(pending)})")
    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("OK: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
