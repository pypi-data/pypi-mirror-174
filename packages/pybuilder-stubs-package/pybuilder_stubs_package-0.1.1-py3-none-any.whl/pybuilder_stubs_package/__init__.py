# -*- coding: utf-8 -*-
import os
import shutil

from pybuilder.core import depends, init, task
from pybuilder.utils import jp


@init
def init_stubs_plugin(project):
    project.plugin_depends_on("mypy", "~=0.980")
    project.plugin_depends_on("twine", ">=1.15.0")
    project.plugin_depends_on("wheel", ">=0.34.0")
    project.plugin_depends_on("setuptools", ">=38.6.0")


def build_dir(project):
    return jp(project.expand_path(project.get_property("dir_dist")), "stubs")


@task("stubs_publish", "Creates .pyi type stubs as a separate -stubs package")
def stubs_publish(project, reactor):
    name = project.get_property("name", None)
    version = project.get_property("version", None)
    maintainer = ", ".join(map(lambda a: a.name, project.maintainers))
    maintainer_email = ",".join(map(lambda a: a.email, project.maintainers))
    build_file = f"""import os
from setuptools import setup


def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for file in files:
            path = os.path.join(root, file).replace(package + os.sep, "", 1)
            stubs.append(path)
    return {{package: stubs}}


setup(
    name="{name}-stubs",
    maintainer="{maintainer}",
    maintainer_email="{maintainer_email}",
    description="Stubs for {name}",
    url="{project.url}",
    license="{project.license}",
    version="{version}",
    packages=["{name}-stubs"],
    install_requires=[
        "{name}=={version}"
    ],
    package_data=find_stubs("{name}-stubs"),
    zip_safe=False,
)
"""
    bd = build_dir(project)
    venv = reactor.pybuilder_venv
    python_exec = " ".join(venv.executable)

    shutil.rmtree(bd, ignore_errors=True)
    os.makedirs(bd)
    with open(jp(bd, "setup.py"), "w", encoding="utf8") as fw:
        fw.write(build_file)
    src_dir = project.expand_path(project.get_property("dir_source_main_python"))
    private = project.get_property("stubs_include_private")
    docstrings = project.get_property("stubs_include_docstrings")
    command = [python_exec]
    command.extend((
        "-m","mypy.stubgen",
        "--output",bd,
    ))
    if private:
        command.append("--include-private")
    if docstrings:
        command.append("--include-docstrings")
    command.append(src_dir)
    venv.execute_command(
        " ".join(command),
        shell=True,
    )
    os.rename(jp(bd, name), jp(bd, f"{name}-stubs"))
    venv.execute_command(f"{python_exec} setup.py bdist_wheel", cwd=bd, shell=True)


@task("stubs_upload", "Uploads type stubs using twine")
@depends("stubs_publish")
def stubs_upload(project, reactor):
    venv = reactor.pybuilder_venv
    python_exec = " ".join(venv.executable)
    venv.execute_command(
        f"{python_exec} -m twine upload dist/*", cwd=build_dir(project), shell=True
    )


@task
def clean(project):
    shutil.rmtree(build_dir(project), ignore_errors=True)
