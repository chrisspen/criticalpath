CriticalPath
============

[![](https://img.shields.io/pypi/v/criticalpath.svg)](https://pypi.python.org/pypi/criticalpath) [![Build Status](https://img.shields.io/travis/chrisspen/criticalpath.svg?branch=master)](https://travis-ci.org/chrisspen/criticalpath)

Calculates the
[critical path](http://en.wikipedia.org/wiki/Critical_path_method)
through a network of tasks.

Assumes the given graph is acyclic (has no loops).

A task network is composed of nodes, but it's also organized within
a parent node. This allows my node/task model to support recursive nesting
of tasks. e.g. An overall "project" node containing multiple tasks can be
treated as a single task in itself, and therefore included in more abstract
task groupings.

Installation
------------

    pip install criticalpath

Usage
-----

    >>> from criticalpath import Node
    >>> p = Node('project')
    >>> a = p.add(Node('A', duration=3))
    >>> b = p.add(Node('B', duration=3, lag=0))
    >>> c = p.add(Node('C', duration=4, lag=0))
    >>> d = p.add(Node('D', duration=6, lag=0))
    >>> e = p.add(Node('E', duration=5, lag=0))
    >>> p.link(a, b).link(a, c).link(a, d).link(b, e).link(c, e).link(d, e)
    project
    >>> p.update_all()
    >>> p.get_critical_path()
    [A, D, E]
    >>> p.duration
    14

Development
-----------

To run unittests across multiple Python versions, install:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python-dev python3-dev python3.3-minimal python3.3-dev python3.4-minimal python3.4-dev python3.5-minimal python3.5-dev python3.6 python3.6-dev

To run all [tests](http://tox.readthedocs.org/en/latest/):

    export TESTNAME=; tox

To run tests for a specific environment (e.g. Python 2.7):
    
    export TESTNAME=; tox -e py27
