from __future__ import annotations
from subprocess import CompletedProcess
from .colors import FOREGROUND_YELLOW

def get_subprocess_result(cp: CompletedProcess, ignore_returncode: int|list[int] = None, ignore_stderr = False, ignore_stdout = False) -> str:
    def include_returncode(returncode):
        if isinstance(ignore_returncode, int):
            return returncode != ignore_returncode
        elif isinstance(ignore_returncode, list):
            return returncode not in ignore_returncode
        else:
            return True

    parts = []

    if include_returncode(cp.returncode):
        parts.append(f"returncode: {FOREGROUND_YELLOW}" % cp.returncode)

    if not ignore_stderr:
        if isinstance(cp.stderr, str):
            stderr = cp.stderr.strip()
        else: # byte array
            stderr = cp.stderr
        if stderr:
            parts.append(f"stderr: {FOREGROUND_YELLOW}" % stderr)

    if not ignore_stdout:
        if isinstance(cp.stdout, str):
            stdout = cp.stdout.strip()
        else: # byte array
            stdout = cp.stdout
        if stdout:
            parts.append(f"stdout: {FOREGROUND_YELLOW}" % stdout)
    
    return " - ".join(parts)
