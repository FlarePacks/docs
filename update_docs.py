#!/usr/bin/env python3
"""
update_docs.py

Automates parsing Python code blocks in flaredocs markdown files, compiling them
via Flare, and updating or generating VitePress `::: code-group` blocks with the
corresponding `.mcfunction` and `.json` outputs.
"""

import json
import re
import sys
from pathlib import Path

FLAREDOCS_DIR = Path(__file__).parent.resolve()
FLARE_DIR = (FLAREDOCS_DIR.parent / "flare").resolve()
if str(FLARE_DIR) not in sys.path:
    sys.path.insert(0, str(FLARE_DIR))

import flare.context as ctx
from flare.preprocessor import setup_global_env, transform_source


def get_tab_name_and_sort_order(raw_key: str) -> tuple[tuple[int, str], str]:
    if ":" in raw_key:
        ns, path = raw_key.split(":", 1)
    else:
        ns, path = "", raw_key

    clean_path = path.lstrip("/")

    if clean_path == "__constants__":
        order = (0, clean_path)
    elif clean_path == "__init__":
        order = (1, clean_path)
    elif clean_path.startswith("___init__/generated_") or clean_path.startswith("__init__/generated_"):
        order = (2, clean_path)
    else:
        order = (3, clean_path)

    tab_label = f"{clean_path}.mcfunction"
    return order, tab_label


def compile_python_snippet(code: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]]] | str:
    ctx.reset_context()
    ctx._current_namespace = "pack"

    global_env = {"__name__": "__main__", "__file__": "main.py"}

    try:
        setup_global_env(global_env)
        code_obj, _ = transform_source(code, "main.py")
        exec(code_obj, global_env)
        ctx.evaluate_pending_exports()
    except Exception as e:
        return f"Execution Error: {e}"

    if not ctx.files and not ctx.json_files:
        return "No files generated"

    processed_mcfuncs = []
    for k, lines in ctx.files.items():
        if not lines:
            continue
        order, tab_label = get_tab_name_and_sort_order(k)

        lines_copy = list(lines)
        if lines_copy and lines_copy[-1] in ("return 1", "return 0"):
            lines_copy.pop()

        content = "\n".join(lines_copy).strip()
        if content:
            processed_mcfuncs.append((order, tab_label, content))

    processed_mcfuncs.sort(key=lambda x: x[0])
    mcfunc_tabs = [(label, content) for _, label, content in processed_mcfuncs]

    json_tabs = []
    for k, json_obj in ctx.json_files.items():
        if ":" in k:
            _, path = k.split(":", 1)
        else:
            path = k
        filename = path.split("/")[-1]
        if not filename.endswith(".json"):
            filename = f"{filename}.json"
        tab_label = filename
        content = json.dumps(json_obj, indent=4)
        json_tabs.append((tab_label, content))

    if not mcfunc_tabs and not json_tabs:
        return "No non-empty mcfunction or json content"

    return mcfunc_tabs, json_tabs


def build_code_group(python_code: str, py_label: str, mcfunc_tabs: list, json_tabs: list) -> str:
    py_label_str = f" [{py_label}]" if py_label else " [Flare]"
    group_lines = ["::: code-group\n"]
    group_lines.append(f"```python{py_label_str}\n{python_code.strip()}\n```\n")

    for label, content in mcfunc_tabs:
        group_lines.append(f"```mcfunction [{label}]\n{content}\n```\n")

    for label, content in json_tabs:
        group_lines.append(f"```json [{label}]\n{content}\n```\n")

    group_lines.append(":::")
    return "\n".join(group_lines)


def process_markdown_file(file_path: Path, failures: list) -> int:
    text = file_path.read_text(encoding="utf-8")
    updated_count = 0

    cg_pattern = re.compile(r":::\s*code-group\s*\n\s*```python(?:\s*\[(.*?)\])?\n(.*?)\n```.*?\n\s*:::", re.DOTALL)

    def replace_code_group(match: re.Match) -> str:
        nonlocal updated_count
        label = match.group(1) or "Flare"
        py_code = match.group(2)
        compiled = compile_python_snippet(py_code)

        if isinstance(compiled, str):
            failures.append((str(file_path.name), label, py_code[:40].replace('\n', ' '), compiled))
            return match.group(0)

        mcfunc_tabs, json_tabs = compiled
        updated_count += 1
        return build_code_group(py_code, label, mcfunc_tabs, json_tabs)

    new_text = cg_pattern.sub(replace_code_group, text)

    if new_text != text:
        file_path.write_text(new_text, encoding="utf-8")

    return updated_count


def main():
    print(f"Scanning markdown files in: {FLAREDOCS_DIR}")
    md_files = sorted(
        [p for p in FLAREDOCS_DIR.glob("**/*.md") if "node_modules" not in p.parts and ".venv" not in p.parts])

    total_files = len(md_files)
    modified_files = 0
    total_code_groups = 0
    failures = []

    for md_path in md_files:
        rel_path = md_path.relative_to(FLAREDOCS_DIR)
        count = process_markdown_file(md_path, failures)
        if count > 0:
            modified_files += 1
            total_code_groups += count
            print(f"  ✓ {rel_path}: updated {count} code-groups")

    print("\n" + "=" * 50)
    print(f"Done! Updated {total_code_groups} code-groups across {modified_files}/{total_files} files.")
    if failures:
        print(f"\nSkipped / Failed Snippets ({len(failures)}):")
        for filename, label, snippet_preview, reason in failures:
            print(f"  - [{filename} / {label}] '{snippet_preview}...': {reason}")
    else:
        print("All code-groups compiled successfully with zero failures!")
    print("=" * 50)


if __name__ == "__main__":
    main()
