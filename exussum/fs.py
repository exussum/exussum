import subprocess
import fnmatch
from pathlib import Path
import os
import re


def all_files(src):
    regex_include = re.compile("|".join((fnmatch.translate(e) for e in src.included_files)))
    regex_exclude = re.compile("|".join((fnmatch.translate(e) for e in src.excluded_files)))

    for root, dirs, files in os.walk(src.root):
        dirs[:] = [d for d in dirs if d not in src.excluded_paths]
        path = os.path.relpath(root, src.root)
        for file in files:
            if regex_include.match(file) and not (src.excluded_files and regex_exclude.match(file)):
                yield os.path.join(path, file)


def _run_rg(args):
    result = subprocess.run(args, stdout=subprocess.PIPE)
    out = result.stdout.decode("utf-8")
    if out:
        print(out, end="", flush=True)


def _chunk_by_len(arr, max_size):
    chunk = []
    size = 0

    for e in arr:
        if len(e) + size + len(chunk) > max_size:
            yield chunk
            chunk.clear()
            size = 0
        size += len(e)
        chunk.append(e)
    if chunk:
        yield chunk


def grep(config, args):
    os.chdir(config.src.root)
    cmd = [config.unix.rg, "--color", "never", "-j1"] + args
    max = 4096 - sum(len(e) for e in cmd)

    for chunk in _chunk_by_len(all_files(config.src), max):
        _run_rg(cmd + chunk)
