from __future__ import annotations
import os, shutil, logging, subprocess, sys
from argparse import ArgumentParser
from glob import glob
import sys
from .commands import add_object_commands, exec_command
from .logging import configure_logging
from .packaging import BuildMixin

logger = logging.getLogger(__name__)


class CleanMixin:
    clean_paths = [
        "build",
        "dist",
        ".eggs",
        "**/__pycache__",
        "**/*.egg-info",
    ]

    def clean_add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--dry-run", "-n", action="store_true")

    def clean(self, dry_run: bool = False):
        for globpath in self.clean_paths:
            for path in glob(globpath, recursive=True):
                if dry_run:
                    print("would clean", path)
                else:
                    print("clean", path)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.unlink(path)


class LsoMixin:
    lso_excludes = [
        ".venv",
    ]

    def lso(self):
        command = ["git", "ls-files", "-o"]
        for exclude in self.lso_excludes:
            command += ["-x", exclude]
        subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr)


try:
    from .credentials import CredentialsMixin
except ModuleNotFoundError:  # some dependencies for credentials are missing
    class CredentialsMixin:
        pass


class Tools(BuildMixin, CredentialsMixin, CleanMixin, LsoMixin):
    def exec(self):
        configure_logging()

        parser = ArgumentParser()
        subparsers = parser.add_subparsers()

        add_object_commands(subparsers, self, exclude=["exec"])
        exec_command(parser)
