from __future__ import annotations
import sys, logging, subprocess, re
from argparse import ArgumentParser
from pathlib import Path
import sys
from .versioning import check_git_version_tag, get_module_version

logger = logging.getLogger(__name__)


class BuildMixin:
    pyproject_path = Path("pyproject.toml")
    pyproject_version_pattern = re.compile(r"^\s*version\s*=\s*\"([^\"]+)\"", re.MULTILINE)

    def _get_build_version(self):
        return get_module_version()


    def _get_build_dist(self, packagename, version):
        dist = []
        #source distribution not built: dist += [f"dist/{packagename}-{version}.tar.gz"] # source distribution
        dist += [f"dist/{packagename}-{version}-py3-none-any.whl"] # wheel built distribution
        
        return dist


    def _get_pyproject_version(self, change_to_version = None) -> str:
        text = self.pyproject_path.read_text(encoding="utf-8")

        m = self.pyproject_version_pattern.search(text)
        if not m:
            raise ValueError("version not found in %s" % self.pyproject_path)
        beforechange_version = m.group(1)

        if change_to_version and change_to_version != beforechange_version:
            logger.warning("updating %s version from %s to %s", self.pyproject_path, beforechange_version, change_to_version)
            text = re.sub(self.pyproject_version_pattern, f"version = \"{change_to_version}\"", text, count=1)
            self.pyproject_path.write_text(text, encoding="utf-8")
            return change_to_version

        return beforechange_version


    def checkbuild(self):
        packagename, version = self._get_build_version()
        command = [sys.executable, "-m", "twine", "check"] + self._get_build_dist(packagename, version)
        cp = subprocess.run(command, text=True, stdout=sys.stdout, stderr=sys.stderr)
        if cp.returncode != 0:
            logger.error(f"check returned code {cp.returncode}")
            return False
        else:
            return True


    def checkversion(self):
        module, version = self._get_build_version()
        pyproject_version = self._get_pyproject_version()

        ok = True
        if pyproject_version != version:
            logger.error(f"invalid pyproject.toml version: {pyproject_version}, {module} module version is {version}")
            ok = False
        
        if not check_git_version_tag(version):
            ok = False

        return ok


    def upload_add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--repository", "-r", help="repository name, as declared in ~/.pypirc")


    def upload(self, repository=None):
        packagename, version = self._get_build_version()        
        if not repository:
            repository = packagename
        
        builds = self._get_build_dist(packagename, version)
        command = [sys.executable, "-m", "twine", "upload", "--repository", repository] + builds

        logger.info(f"uploading to repository \"{repository}\": {', '.join(builds)}")
        cp = subprocess.run(command, text=True, stdout=sys.stdout, stderr=sys.stderr)
        if cp.returncode != 0:
            logger.error(f"twine upload returned code {cp.returncode}")


    def build_add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--upload", "-u", action="store_true", help="upload to pypi after build")
        self.upload_add_arguments(parser)


    def build(self, upload = False, repository = None):
        # Verify/update version in pyproject.toml
        _, version = self._get_build_version()
        self._get_pyproject_version(change_to_version=version)

        # Clean before build
        if hasattr(self, "clean"):
            logger.info("clean before build")
            self.clean()

        # Build
        logger.info("build distribution")
        #deprecated: subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"], check=True, stdout=sys.stdout, stderr=sys.stderr)
        subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps", "-w", "dist", "."], check=True, stdout=sys.stdout, stderr=sys.stderr)

        # Check
        ok = True

        logger.info("check build")
        ok = ok and self.checkbuild()

        logger.info("check git version tag")
        ok = ok and self.checkversion()

        # Upload if required
        if upload:
            if not ok:
                logger.warning(f"upload cancelled")
                return
        
            logger.info(f"upload distribution")
            self.upload(repository=repository)

