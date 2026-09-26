#!/usr/bin/env python3
"""Local content-boundary lint. No network, no project-content reads.

Checks structural links and known project markers; human source review remains
necessary. A clean result does not imply access control or clean Git history.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit, parse_qs
import argparse
import json
import posixpath
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECT_HOST = 'nkd-lkz.github.io'
REPO = 'nkd-lkz/physical-self-evolution'
TEXT_EXTENSIONS = {'.md', '.json', '.bib', '.svg', '.html', '.txt', '.yml', '.yaml'}
MARKERS = re.compile(
    r'Universal Physical Token|loss[- ]first|train450|clean490|'
    r'B0-Head|B1-Measured|B2-ValidPhysics|'
    r'对当前\s*RLT\s*研究|对\s*RLT\s*的可执行借鉴|'
    r'本周最值得完成|研究者提供的随想', re.I)
INLINE = re.compile(r'\]\(\s*<?([^\s)>]+)')
REFERENCE = re.compile(r'^\s*\[[^\]]+\]:\s*<?([^\s>]+)', re.M)
HTML = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)', re.I)
URL = re.compile(r'https?://[^\s<>"\')\]}]+')
PATH_IN_CODE = re.compile(r'`((?:\.\./|survey-rsi/)[^`\s]+)`')


def within(path, parent):
    return path == parent or parent in path.parents


def target_problem(target, source, root):
    if source.relative_to(root).as_posix() == 'templates/paper.md' and target == '原图URL或有许可的本地图路径':
        return None
    target = unquote(target.strip('<>'))
    if not target or target.startswith(('#', 'mailto:', 'data:')):
        return None
    u = urlsplit(target)
    if u.netloc:
        host = (u.hostname or '').lower()
        if host == PROJECT_HOST:
            return 'project website URL'
        if host in {'github.com', 'raw.githubusercontent.com', 'api.github.com'}:
            path = posixpath.normpath(u.path).strip('/')
            if host == 'api.github.com':
                prefix = 'repos/' + REPO
                if path == prefix or path.startswith(prefix+'/'):
                    if not path.startswith(prefix+'/contents/survey-rsi/'):
                        return 'own-repository URL outside survey'
            elif path == REPO or path.startswith(REPO+'/'):
                tail = path[len(REPO):].strip('/')
                if host == 'github.com':
                    valid = re.match(r'(?:blob|tree)/[^/]+/survey-rsi(?:/|$)', tail)
                else:
                    valid = re.match(r'[^/]+/survey-rsi(?:/|$)', tail)
                if not valid:
                    return 'own-repository URL outside survey'
        return None
    if u.scheme:
        return 'non-web local resource link'
    if not u.path:
        return None
    # Repository-root command paths are allowed only within the survey.
    if u.path.startswith('survey-rsi/'):
        dest = root.parent/u.path
    elif u.path.startswith('/'):
        return 'absolute local path'
    else:
        dest = source.parent/u.path
    dest = dest.resolve()
    if not within(dest, root):
        return 'local link escapes survey'
    if not dest.exists():
        return 'missing local target'
    for p in parse_qs(u.query).get('path', []):
        if not within((dest.parent/p).resolve(), root):
            return 'reader query escapes survey'
    return None


def check(root):
    root = root.resolve()
    errors = []
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            errors.append((rel, 'symlink not allowed in survey'))
            continue
        if not path.is_file() or path.suffix not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding='utf-8')
        if MARKERS.search(text):
            errors.append((rel, 'project-specific content marker; review provenance'))
        targets = INLINE.findall(text)+REFERENCE.findall(text)+HTML.findall(text)+URL.findall(text)+PATH_IN_CODE.findall(text)
        if path.suffix == '.json':
            try:
                obj = json.loads(text)
            except ValueError as exc:
                errors.append((rel, f'invalid JSON: {exc}'))
                continue
            def paths(value):
                if isinstance(value, dict):
                    for k, v in value.items():
                        if k in {'note','note_path','figure_path'} and isinstance(v,str):
                            targets.append('survey-rsi/'+v)
                        paths(v)
                elif isinstance(value,list):
                    for v in value: paths(v)
            paths(obj)
        for target in sorted(set(targets)):
            problem = target_problem(target, path, root)
            if problem:
                # Report paths and error classes, not copied project content.
                errors.append((rel, problem))
    if (root/'experiments').exists():
        errors.append(('experiments/', 'project experiment directory not allowed'))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    errors = check(args.root)
    for path, message in errors:
        print(f'{path}: {message}')
    if errors:
        print(f'Boundary check failed: {len(errors)} issue(s).')
        return 1
    print('Survey boundary check passed (links, paths, known markers). Semantic source review still required.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
