#!/usr/bin/python
# coding: utf8
# /*##########################################################################
#
# Copyright (c) 2015-2019 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["Jérôme Kieffer", "Thomas Vincent", "H. Payno"]
__date__ = "12/02/2019"
__license__ = "MIT"


import sys
import os
import logging
import io

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("rsyncmanager.setup")


from distutils.command.build import build as _build
try:
    from setuptools import Command
    from setuptools.command.build_ext import build_ext
    from setuptools.command.sdist import sdist
    logger.info("Use setuptools")
except ImportError:
    try:
        from numpy.distutils.core import Command
    except ImportError:
        from distutils.core import Command
    from distutils.command.build_ext import build_ext
    from distutils.command.sdist import sdist
    logger.info("Use distutils")

try:
    import sphinx
    import sphinx.util.console
    sphinx.util.console.color_terminal = lambda: False
    from sphinx.setup_command import BuildDoc
except ImportError:
    sphinx = None


PROJECT = "rsyncmanager"

if "LANG" not in os.environ and sys.platform == "darwin" and sys.version_info[0] > 2:
    print("""WARNING: the LANG environment variable is not defined,
an utf-8 LANG is mandatory to use setup.py, you may face unexpected UnicodeError.
export LANG=en_US.utf-8
export LC_ALL=en_US.utf-8
""")


def get_version():
    """Returns current version number from version.py file"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, dirname)
    import rsyncmanager.version
    sys.path = sys.path[1:]
    return rsyncmanager.version.strictversion


def get_readme():
    """Returns content of README.rst file"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, "README.rst")
    with io.open(filename, "r", encoding="utf-8") as fp:
        long_description = fp.read()
    return long_description


classifiers = ["Development Status :: 4 - Beta",
               "Environment :: Console",
               "Environment :: MacOS X",
               "Environment :: Win32 (MS Windows)",
               "Intended Audience :: Education",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: MIT License",
               "Natural Language :: English",
               "Operating System :: MacOS",
               "Operating System :: Microsoft :: Windows",
               "Operating System :: POSIX",
               "Programming Language :: Cython",
               "Programming Language :: Python :: 3.5",
               "Programming Language :: Python :: 3.6",
               "Programming Language :: Python :: 3.7",
               "Programming Language :: Python :: Implementation :: CPython",
               "Topic :: Scientific/Engineering :: Physics",
               "Topic :: Software Development :: Libraries :: Python Modules",
               ]

########
# Test #
########

class PyTest(Command):
    """Command to start tests running the script: run_tests.py"""
    user_options = []

    description = "Execute the unittests"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        errno = subprocess.call([sys.executable, 'run_tests.py'])
        if errno != 0:
            raise SystemExit(errno)


# ################### #
# build_doc command   #
# ################### #

if sphinx is None:
    class SphinxExpectedCommand(Command):
        """Command to inform that sphinx is missing"""
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            raise RuntimeError(
                'Sphinx is required to build or test the documentation.\n'
                'Please install Sphinx (http://www.sphinx-doc.org).')


if sphinx is not None:
    class BuildDocCommand(BuildDoc):
        """Command to build documentation using sphinx.

        Project should have already be built.
        """

        def run(self):
            # make sure the python path is pointing to the newly built
            # code so that the documentation is built on this and not a
            # previously installed version

            build = self.get_finalized_command('build')
            sys.path.insert(0, os.path.abspath(build.build_lib))

            # Build the Users Guide in HTML and TeX format
            for builder in ['html', 'latex']:
                self.builder = builder
                self.builder_target_dir = os.path.join(self.build_dir, builder)
                self.mkpath(self.builder_target_dir)
                BuildDoc.run(self)
            sys.path.pop(0)

else:
    BuildDocCommand = SphinxExpectedCommand


# ############################# #
# numpy.distutils Configuration #
# ############################# #

def configuration(parent_package='', top_path=None):
    """Recursive construction of package info to be used in setup().

    See http://docs.scipy.org/doc/numpy/reference/distutils.html#numpy.distutils.misc_util.Configuration
    """
    try:
        from numpy.distutils.misc_util import Configuration
    except ImportError:
        raise ImportError(
            "To install this package, you must install numpy first\n"
            "(See https://pypi.python.org/pypi/numpy)")
    config = Configuration(None, parent_package, top_path)
    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True)
    config.add_subpackage(PROJECT)
    return config

# ############## #
# Compiler flags #
# ############## #


class Build(_build):
    """Command to support more user options for the build."""

    def _parse_env_as_bool(self, key):
        content = os.environ.get(key, "")
        value = content.lower()
        if value in ["1", "true", "yes", "y"]:
            return True
        if value in ["0", "false", "no", "n"]:
            return False
        if value in ["none", ""]:
            return None
        msg = "Env variable '%s' contains '%s'. But a boolean or an empty \
            string was expected. Variable ignored."
        logger.warning(msg, key, content)
        return None

################################################################################
# Debian source tree
################################################################################


class sdist_debian(sdist):
    """
    Tailor made sdist for debian
    * remove auto-generated doc
    * remove cython generated .c files
    * remove cython generated .cpp files
    * remove .bat files
    * include .l man files
    """

    description = "Create a source distribution for Debian (tarball, zip file, etc.)"

    @staticmethod
    def get_debian_name():
        import rsyncmanager.version
        name = "%s_%s" % (PROJECT, rsyncmanager.version.debianversion)
        return name

    def prune_file_list(self):
        sdist.prune_file_list(self)
        to_remove = ["doc/build", "doc/pdf", "doc/html", "pylint", "epydoc"]
        for rm in to_remove:
            self.filelist.exclude_pattern(pattern="*", anchor=False, prefix=rm)

        # this is for Cython files specifically: remove C & html files
        search_root = os.path.dirname(os.path.abspath(__file__))
        for root, _, files in os.walk(search_root):
            for afile in files:
                if os.path.splitext(afile)[1].lower() == ".pyx":
                    base_file = os.path.join(root, afile)[len(search_root) + 1:-4]
                    self.filelist.exclude_pattern(pattern=base_file + ".c")
                    self.filelist.exclude_pattern(pattern=base_file + ".cpp")
                    self.filelist.exclude_pattern(pattern=base_file + ".html")

    def make_distribution(self):
        self.prune_file_list()
        sdist.make_distribution(self)
        dest = self.archive_files[0]
        dirname, basename = os.path.split(dest)
        base, ext = os.path.splitext(basename)
        while ext in [".zip", ".tar", ".bz2", ".gz", ".Z", ".lz", ".orig"]:
            base, ext = os.path.splitext(base)
        # if ext:
        #     dest = "".join((base, ext))
        # else:
        #     dest = base
        # sp = dest.split("-")
        # base = sp[:-1]
        # nr = sp[-1]
        debian_arch = os.path.join(dirname, self.get_debian_name() + ".orig.tar.gz")
        os.rename(self.archive_files[0], debian_arch)
        self.archive_files = [debian_arch]
        print("Building debian .orig.tar.gz in %s" % self.archive_files[0])


# ##### #
# setup #
# ##### #

def get_project_configuration(dry_run):
    """Returns project arguments for setup"""
    install_requires = [
        # for the script launcher and pkg_resources
        "setuptools",
        "silx>=0.9",
        "lxml",
    ]

    setup_requires = ["setuptools",]

    # extras requirements: target 'full' to install all dependencies at once
    full_requires = [

    ]

    extras_require = {
        'full': full_requires,
    }

    package_data = {
    }

    entry_points = {
    }

    cmdclass = dict(
        build=Build,
        test=PyTest,
        build_doc=BuildDocCommand,
        debian_src=sdist_debian)

    if dry_run:
        # DRY_RUN implies actions which do not require NumPy
        #
        # And they are required to succeed without Numpy for example when
        # pip is used to install rsyncmanager when Numpy is not yet present in
        # the system.
        setup_kwargs = {}
    else:
        config = configuration()
        setup_kwargs = config.todict()


    setup_kwargs.update(name=PROJECT,
                        version=get_version(),
                        url="https://gitlab.esrf.fr/payno/rsyncmanager.git",
                        author="data analysis unit",
                        author_email="henri.payno@esrf.fr",
                        classifiers=classifiers,
                        description="utilitary to access tomography data at esrf",
                        long_description=get_readme(),
                        install_requires=install_requires,
                        setup_requires=setup_requires,
                        extras_require=extras_require,
                        cmdclass=cmdclass,
                        package_data=package_data,
                        zip_safe=False,
                        entry_points=entry_points,
                        )
    return setup_kwargs


def setup_package():
    """Run setup(**kwargs)

    Depending on the command, it either runs the complete setup which depends on numpy,
    or a *dry run* setup with no dependency on numpy.
    """

    # Check if action requires build/install
    dry_run = len(sys.argv) == 1 or (len(sys.argv) >= 2 and (
        '--help' in sys.argv[1:] or
        sys.argv[1] in ('--help-commands', 'egg_info', '--version',
                        'clean', '--name')))

    if dry_run:
        # DRY_RUN implies actions which do not require dependencies, like NumPy
        try:
            from setuptools import setup
            logger.info("Use setuptools.setup")
        except ImportError:
            from distutils.core import setup
            logger.info("Use distutils.core.setup")
    else:
        try:
            from setuptools import setup
        except ImportError:
            from numpy.distutils.core import setup
            logger.info("Use numpy.distutils.setup")

    setup_kwargs = get_project_configuration(dry_run)
    setup(**setup_kwargs)


if __name__ == "__main__":
    setup_package()
