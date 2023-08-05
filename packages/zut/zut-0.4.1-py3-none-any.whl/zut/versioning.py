from __future__ import annotations
import subprocess, re, logging
from pathlib import Path
from importlib import import_module
from importlib.util import find_spec
from types import ModuleType
from .colors import FOREGROUND_BLUE

logger = logging.getLogger(__name__)


def get_git_tags(points_at: str = None, pattern: str = None) -> list[str]:
    """
    Get list of defined tags.
    Use points_at="HEAD" for tags pointing on last commit.
    """
    cmd = ['git', 'tag', '--list']
    if points_at:
        cmd.append("--points-at")
        cmd.append(points_at)
    if pattern:
        cmd.append(pattern)

    cp = subprocess.run(cmd, check=True, text=True, capture_output=True)
    tags = cp.stdout.strip()
    if not tags:
        return []
    
    return tags.splitlines()


def get_git_hash(ref: str = "HEAD") -> None|str:
    """
    Get commit hash of a reference (branch, tag, etc).
    Use ref="HEAD" for last commit and ref=None for last commit only if there is no changes.
    """
    try:
        cp = subprocess.run(['git', 'rev-list', '-n', '1', ref], check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError:
        if cp.returncode == 128:
            return None

    return cp.stdout.strip()


def git_has_changes():
    """
    Indicate whether working directory has changes since last commit.
    """
    cp = subprocess.run(['git', 'status', '--porcelain'], check=True, text=True, capture_output=True)
    return cp.stdout != ""


def check_git_version_tag(version: str) -> bool:
    if not isinstance(version, str):
        raise ValueError(f"invalid type for argument \"version\": {type(version)}")
    
    ok = True

    # Check version
    if not re.match(r"^\d+\.\d+\.\d+(?:\-[a-z0-9\-]+)?$", version):
        logger.error(f"version \"{version}\" does not match required regex")
        ok = False

    # Compare version with git tags
    tags = get_git_tags(pattern="v*")
    if not tags or not f"v{version}" in tags:
        logger.warning(f"tag v{version} not found")
        ok = False
    
    else:
        # Ensure corresponding version tag matches current hash
        tag_hash = get_git_hash(f"v{version}")
        
        if tag_hash:
            head_hash = get_git_hash()
            
            if tag_hash != head_hash:
                logger.error(f"tag v{version} points at {FOREGROUND_BLUE % tag_hash}, head points at {FOREGROUND_BLUE % head_hash}")
                ok = False
            
            elif git_has_changes():
                logger.error(f"git has changes since HEAD (tag v{version})")
                ok = False

    return ok


def get_module_version() -> tuple[str,str]:
    modules = []

    for path in Path().iterdir():
        if not path.is_dir():
            continue

        try:
            package = find_spec(path.name)
        except ImportError:
            continue

        if not package:
            continue

        module = import_module(package.name)

        if hasattr(module, "__version__"):
            modules.append(module)

    if not modules:
        raise ValueError("no module found with __version__ attribute")

    if len(modules) > 1:
        raise ValueError("several modules found with __version__ attribute: %s" % ", ".join(module.__name__ for module in modules))

    module = modules[0]
    return module.__name__, getattr(module, "__version__")

