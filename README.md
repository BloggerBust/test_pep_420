
# Table of Contents

1.  [What are the issues?](#org1d8d9d6)
2.  [How to run the tests?](#org65432fb)
3.  [How to build a wheel & source dist](#orgf72f6ff)
4.  [How to install the package](#org163fb90)
5.  [What to watch out for](#orge00bd6b)
    1.  [Use `find_namespace` directive for namespace packages](#orgc77e38f)
    2.  [A fully declarative setup does not yet support editable install](#org9ba8d92)



<a id="org1d8d9d6"></a>

# What are the issues?

PEP-420 [Differences between namespace packages and regular packages](https://www.python.org/dev/peps/pep-0420/#differences-between-namespace-packages-and-regular-packages) says that an implicit namespace package should not have a `__file__` attribute. I wrote a test that checks for the presence of the `__file__` attribute and the test fails.


<a id="org65432fb"></a>

# How to run the tests?

The repository includes an implicitly namespace package named `implicit_namespace_foo`. Clone the repository.

    cd ~/dev
    git clone https://github.com/BloggerBust/test_pep_420.git
    cd test_pep_420

Then run the tests.

    rm -rf venv/
    python -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip setuptools
    python -m unittest discover

    ..F
    ======================================================================
    FAIL: test_namespace_has_no_file_attribute (test.bar.test_pep420_implicit_namespace_package.TestPep420ImplicitNamespacePackage)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/dustfinger/dev/test_pep_420/test/bar/test_pep420_implicit_namespace_package.py", line 14, in test_namespace_has_no_file_attribute
        self.assertFalse(hasattr(implicit_namespace_foo, '__file__'))
    AssertionError: True is not false
    
    ----------------------------------------------------------------------
    Ran 3 tests in 0.000s
    
    FAILED (failures=1)


<a id="orgf72f6ff"></a>

# How to build a wheel & source dist

The project's [setup configuration](setup.cfg) follows [PEP-517](https://www.python.org/dev/peps/pep-0517/) and its [build system configuration](pyproject.toml) follows [PEP-518](https://www.python.org/dev/peps/pep-0518/) at the time of writing. To build a wheel and source distribution you can use [pep517](https://pypi.org/project/pep517/) package.

    pip install -q pep517
    python -m pep517.build .

The wheel and source distribution will be placed in a directory named dist by default.

    ls dist/

    implicit_namespace_foo-_0.0.1_-py3-none-any.whl
    implicit_namespace_foo--0.0.1-.tar.gz

Help documentation is available at the command-line.

    python -m pep517.build --help

    usage: build.py [-h] [--binary] [--source] [--out-dir OUT_DIR] source_dir
    
    positional arguments:
      source_dir            A directory containing pyproject.toml
    
    optional arguments:
      -h, --help            show this help message and exit
      --binary, -b
      --source, -s
      --out-dir OUT_DIR, -o OUT_DIR
                            Destination in which to save the builds relative to
                            source dir


<a id="org163fb90"></a>

# How to install the package

Installing the package is straight forward.

To install using the wheel

    pip install dist/implicit_namespace_foo-_0.0.1_-py3-none-any.whl
    echo
    echo "==================="
    echo "Installed packages:"
    echo "==================="
    pip freeze

    Processing ./dist/implicit_namespace_foo-_0.0.1_-py3-none-any.whl
    Installing collected packages: implicit-namespace-foo
    Successfully installed implicit-namespace-foo--0.0.1-
    
    ===================
    Installed packages:
    ===================
    implicit-namespace-foo===-0.0.1-
    importlib-metadata==1.5.0
    pep517==0.8.1
    toml==0.10.0
    zipp==3.0.0

To install using the source distribution

    pip install -q dist/implicit_namespace_foo--0.0.1-.tar.gz
    echo
    echo "==================="
    echo "Installed packages:"
    echo "==================="
    pip freeze

    
    ===================
    Installed packages:
    ===================
    implicit-namespace-foo===-0.0.1-
    importlib-metadata==1.5.0
    pep517==0.8.1
    toml==0.10.0
    zipp==3.0.0

Or you can simply install from the local source tree.

    pip install -q .
    echo
    echo "==================="
    echo "Installed packages:"
    echo "==================="
    pip freeze

    
    ===================
    Installed packages:
    ===================
    implicit-namespace-foo===-0.0.1-
    importlib-metadata==1.5.0
    pep517==0.8.1
    toml==0.10.0
    zipp==3.0.0


<a id="orge00bd6b"></a>

# What to watch out for


<a id="orgc77e38f"></a>

## Use `find_namespace` directive for namespace packages

When building a namespace package it is important to use the `find_namespace` directive in  [setup.cfg](setup.cfg).

    [options]
    namespace_packages =
        implicit_namespace_foo
    packages = find_namespace:

If instead the setup.cfg used the find directive like this:

    [options]
    namespace_packages =
        implicit_namespace_foo
    packages = find:

Then the build will treat the package as a standard package. When it finds that the package is empty it will not recursively search the sub packages. The project will still build and install without errors.

    pip install -q pep517
    python -m pep517.build .
    pip install dist/implicit_namespace_foo-_0.0.1_-py3-none-any.whl

    ... above output omitted for brevity
    running install_scripts
    creating build/bdist.linux-x86_64/wheel/implicit_namespace_foo-_0.0.1_.dist-info/WHEEL
    creating '/tmp/tmpxv0wm9jr/tmphsnicn86/implicit_namespace_foo-_0.0.1_-py3-none-any.whl' and adding 'build/bdist.linux-x86_64/wheel' to it
    adding 'implicit_namespace_foo-_0.0.1_-py3.7-nspkg.pth'
    adding 'implicit_namespace_foo-_0.0.1_.dist-info/LICENSE-2.0.txt'
    adding 'implicit_namespace_foo-_0.0.1_.dist-info/METADATA'
    adding 'implicit_namespace_foo-_0.0.1_.dist-info/WHEEL'
    adding 'implicit_namespace_foo-_0.0.1_.dist-info/namespace_packages.txt'
    adding 'implicit_namespace_foo-_0.0.1_.dist-info/top_level.txt'
    adding 'implicit_namespace_foo-_0.0.1_.dist-info/RECORD'
    removing build/bdist.linux-x86_64/wheel

However; none of the namespace packages sub packages were added to the wheel. Not only that, but calls to pip will report an error.

    pip freeze

    Error processing line 1 of /home/dustfinger/dev/test_pep_420/venv/lib/python3.7/site-packages/implicit_namespace_foo-_0.0.1_-py3.7-nspkg.pth:
    
      Traceback (most recent call last):
        File "/usr/lib/python-exec/python3.7/../../../lib/python3.7/site.py", line 168, in addpackage
          exec(line)
        File "<string>", line 1, in <module>
        File "<frozen importlib._bootstrap>", line 580, in module_from_spec
      AttributeError: 'NoneType' object has no attribute 'loader'
    
    Remainder of file ignored
    implicit-namespace-foo===-0.0.1-
    importlib-metadata==1.5.0
    pep517==0.8.1
    toml==0.10.0
    zipp==3.0.0

That is the same error reported in [pip issue #6055](https://github.com/pypa/pip/issues/6055).


<a id="org9ba8d92"></a>

## A fully declarative setup does not yet support editable install

    pip install -e .

    ERROR: File "setup.py" not found. Directory cannot be installed in editable mode: /home/dustfinger/dev/test_pep_420
    (A "pyproject.toml" file was found, but editable mode currently requires a setup.py based build.)

