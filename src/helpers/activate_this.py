"""Activate virtualenv for current interpreter:

Use exec(open(this_file).read(), {'__file__': this_file}).

This can be used when you must use an existing Python interpreter, not the virtualenv bin/python.

Modified the virtualenv original file: https://github.com/pypa/virtualenv/blob/master/virtualenv_embedded/activate_this.py
"""
import os
import site
import sys

try:
    bin_dir
except NameError:
    raise AssertionError("You must use exec(open(this_file).read(), {'bin_dir': ./.env/}))")

# prepend bin to PATH (this file is inside the bin directory)
os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))

# virtual env is right above bin directory
os.environ["VIRTUAL_ENV"] = bin_dir

# add the virtual environments site-package to the host python import mechanism
IS_PYPY = hasattr(sys, "pypy_version_info")
IS_JYTHON = sys.platform.startswith("java")
if IS_JYTHON:
    site_packages = os.path.join(bin_dir, "Lib", "site-packages")
elif IS_PYPY:
    site_packages = os.path.join(bin_dir, "site-packages")
else:
    IS_WIN = sys.platform == "win32"
    if IS_WIN:
        site_packages = os.path.join(bin_dir, "Lib", "site-packages")
    else:
        site_packages = os.path.join(bin_dir, "lib", "python{}".format(sys.version[:3]), "site-packages")

prev = set(sys.path)
site.addsitedir(site_packages)
sys.real_prefix = sys.prefix
sys.prefix = bin_dir

# Move the added items to the front of the path, in place
new = list(sys.path)
sys.path[:] = [i for i in new if i not in prev] + [i for i in new if i in prev]
