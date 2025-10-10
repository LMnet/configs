#!/usr/bin/env python3
import argparse
import os
import subprocess
from pathlib import Path
import sys

try:
    import pyperclip
except ImportError:
    pyperclip = None

WIDTH = 58  # total width of separator lines
LINE = "-" * WIDTH

def header_block(display_path: str) -> str:
    mid = f" {display_path} "
    pad_total = max(0, WIDTH - len(mid))
    left = pad_total // 2
    right = pad_total - left
    return f"{LINE}\n{'-'*left}{mid}{'-'*right}\n{LINE}"

def get_repo_root(start: Path) -> Path | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            check=True, capture_output=True, text=True
        )
        return Path(out.stdout.strip())
    except Exception:
        return None

def get_git_ignored_paths(start_dir: Path) -> set[Path]:
    repo_root = get_repo_root(start_dir)
    if not repo_root:
        return set()
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_root), "ls-files", "-ci", "--others", "--exclude-standard", "-z"],
            check=True, capture_output=True
        )
        raw = out.stdout.split(b"\x00")
        ignored_repo_rel = [Path(x.decode("utf-8")) for x in raw if x]
    except Exception:
        return set()

    ignored = set()
    for p in ignored_repo_rel:
        abs_p = (repo_root / p).resolve()
        try:
            abs_p.relative_to(start_dir.resolve())
        except ValueError:
            continue
        ignored.add(abs_p)
    return ignored

def should_descend(current: Path, base: Path, max_depth: int) -> bool:
    rel = current.resolve().relative_to(base.resolve())
    depth = 0 if rel == Path('.') else len(rel.parts)
    return depth < max_depth

def iter_files(base: Path, max_depth: int) -> list[Path]:
    files = []
    for root, dirs, filenames in os.walk(base):
        root_path = Path(root)
        if max_depth == 0:
            dirs[:] = []
        else:
            if not should_descend(root_path, base, max_depth):
                dirs[:] = []
        for name in filenames:
            files.append(root_path / name)
    return sorted(files, key=lambda p: str(p).lower())

def rel_dot_posix(base: Path, path: Path) -> str:
    return "./" + path.resolve().relative_to(base.resolve()).as_posix()

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate file contents with headers; respects .gitignore; clipboard by default."
    )
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan (default: .)")
    parser.add_argument("-d", "--depth", type=int, default=0,
                        help="Recursion depth (0 = current folder only).")
    parser.add_argument("-o", "--output", default=None,
                        help="Optional file to also write the result to (disabled by default).")
    parser.add_argument("--no-clipboard", action="store_true",
                        help="Do not copy to clipboard (by default, the result IS copied).")
    args = parser.parse_args()

    base_dir = Path(args.directory).resolve()
    if not base_dir.is_dir():
        raise SystemExit(f"Not a directory: {base_dir}")

    git_ignored = get_git_ignored_paths(base_dir)
    all_files = iter_files(base_dir, args.depth)

    blocks = []
    for f in all_files:
        # Skip .git internals and git-ignored entries
        rel_parts = f.relative_to(base_dir).parts
        if any(part == ".git" for part in rel_parts):
            continue
        if f.resolve() in git_ignored:
            continue
        if not f.is_file():
            continue

        show_path = rel_dot_posix(base_dir, f)
        header = header_block(show_path)
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            content = f"<<ERROR READING FILE: {e}>>"

        blocks.append(header)
        blocks.append(content.rstrip("\n"))
        # add a blank line after each file's content for readability
        blocks.append("")

    result = "\n".join(blocks).rstrip() + "\n"

    # Clipboard (default)
    if not args.no_clipboard:
        if pyperclip is None:
            sys.exit("pyperclip not installed. Install with: pip install pyperclip\n"
                     "Or run with --no-clipboard to only write a file.")
        pyperclip.copy(result)
        print("✅ Output copied to clipboard.")

    # Optional file output
    if args.output:
        out_path = (base_dir / args.output) if not os.path.isabs(args.output) else Path(args.output)
        out_path.write_text(result, encoding="utf-8")
        print(f"✅ Also wrote output to {out_path}")

if __name__ == "__main__":
    main()
