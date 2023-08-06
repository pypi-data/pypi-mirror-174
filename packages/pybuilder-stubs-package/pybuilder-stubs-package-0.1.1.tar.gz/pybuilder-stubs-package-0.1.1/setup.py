#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup, Extension
from setuptools.command.install import install as _install


class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()



if __name__ == '__main__':
    setup(
        name = 'pybuilder-stubs-package',
        version = '0.1.1',
        description = 'PyBuilder plugin that creates "*-stubs" package for your project using MyPy\'s stubgen',
        long_description = "\nThis plugin adds stubs_publish and stubs_upload tasks that you can use in your\nbuild script.\n\nUsing MyPy's stubgen it creates type hinting stubs (``*.pyi`` files) as a separate\npackage. This stubs-only package is named with the ``stubs`` suffix following PEP\n561. For a pybuilder project foo this would create stubs-only package foo-stubs.\n",
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3'
        ],
        keywords = '',

        author = 'Adam Chýlek',
        author_email = 'adam.chylek@amitia-ai.com',
        maintainer = '',
        maintainer_email = '',

        license = 'MIT',

        url = 'https://github.com/chylek/pybuilder-stubs-package',
        project_urls = {},

        scripts = [],
        packages = ['pybuilder_stubs_package'],
        namespace_packages = [],
        py_modules = [],
        ext_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        include_package_data = False,
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
        setup_requires = [],
    )
