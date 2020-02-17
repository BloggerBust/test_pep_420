
# Table of Contents

1.  [What are the issues?](#org52483bf)
2.  [How to run the tests?](#orgd8c242b)



<a id="org52483bf"></a>

# What are the issues?

PEP-420 [Differences between namespace packages and regular packages](https://www.python.org/dev/peps/pep-0420/#differences-between-namespace-packages-and-regular-packages) says that an implicit namespace package should not have a `__file__` attribute. I wrote a test that checks for the presense of the `__file__` attribute and the test fails.


<a id="orgd8c242b"></a>

# How to run the tests?

The repository includes an implicitly namespace package named `implicit_namespace_foo`. Clone the repository.

    cd ~/dev
    git clone https://github.com/BloggerBust/test_pep_420.git
    cd test_pep_420

Then run the tests

    rm -rf venv/
    python -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip
    python -m unittest discover

