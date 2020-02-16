
# Table of Contents

1.  [What is this about?](#org697baa5)
2.  [Prerequisite](#org2fbf35b)
3.  [What are the issues?](#org18000ba)
    1.  [PEP 420 Namespace package causes pip commands to raise AttributeError](#org42d8215)
    2.  [PEP-420 namespace package has a <span class="underline"><span class="underline">file</span></span> attribute](#orga401fa7)
4.  [How to run the tests?](#org8d6d6e8)



<a id="org697baa5"></a>

# What is this about?

I have run into an issue installing packages with implicit namespaces. I would like to explore the issue to better understand what is going wrong. Someone has already created [pip issue 6055](https://github.com/pypa/pip/issues/6055), the only difference is that my example uses a PEP 420 implicit namespace.


<a id="org2fbf35b"></a>

# Prerequisite

Everything beyond this point assumes that you have cloned this repository and changed directory to the repository root.

    cd ~/dev
    git clone https://github.com/BloggerBust/test_pep_420.git
    cd test_pep_420

The repository includes an implicitly namespace package named implicit<sub>namespace</sub><sub>foo</sub>. 


<a id="org18000ba"></a>

# What are the issues?


<a id="org42d8215"></a>

## PEP 420 Namespace package causes pip commands to raise AttributeError

If I install a namespace package using pip install the installation will appear to have been successful.

    rm -rf venv/
    python -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip
    pip install .

However, running any pip command in the venv will now result in an AttributeError.

    pip freeze

The same result happens if I first build a wheel with pep517.

    rm -rf venv/
    rm -rf build/
    rm -rf dist/
    rm -rf implicit_namespace_foo.egg-info
    python -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip pep517
    python -v -m pep517.check . > pep517check.log 2>&1
    python -v -m pep517.build . > pep517build.log 2>&1
    pip install dist/implicit_namespace_foo-_0.0.1_-py3-none-any.whl

Here is the output for [pep517.check](pep517check.log) and [pep517.build](pep517build.log). The installation succeeds, but running pip in the venv causes the same AttributeError

    pip check


<a id="orga401fa7"></a>

## PEP-420 namespace package has a <span class="underline"><span class="underline">file</span></span> attribute

I wanted to see if the namespace was being created correctly as described in [PEP-420 Differences between namespace packages and regular packages](https://www.python.org/dev/peps/pep-0420/#differences-between-namespace-packages-and-regular-packages). I wrote the following three tests:

1.  test<sub>namespace</sub><sub>has</sub><sub>no</sub><sub>file</sub><sub>attribute</sub>
2.  test<sub>namespace</sub><sub>has</sub><sub>no</sub>\_\_<sub>init</sub>\_\_<sub>module</sub>
3.  test<sub>namespace</sub><sub>has</sub><sub>different</sub><sub>type</sub><sub>of</sub><sub>object</sub><sub>for</sub>\_<sub>loader</sub>\_\_

The first test fails because the namespace package has a `__file__` attribute which violates PEP420.


<a id="org8d6d6e8"></a>

# How to run the tests?

    rm -rf venv/
    python -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip
    python -m unittest discover

