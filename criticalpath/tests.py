#!/usr/bin/env python
"""
To run a unittest:

    python criticalpath.py Test.test_model

"""
from __future__ import print_function

import os
import unittest
from timeit import timeit

import pandas as pd

from criticalpath import Node

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Test(unittest.TestCase):

    def test_nodes(self):
        # Confirm nodes work with set operations.
        nodes = set()
        n1 = Node(name=1, duration=1)
        n2 = Node(name=2, duration=1)
        n2a = Node(name=2, duration=1)
        self.assertEqual(n2, n2a)
        nodes.add(n1)
        nodes.add(n2)
        nodes.add(n2a)
        self.assertEqual(len(nodes), 2)

        parent = Node('parent')
        self.assertEqual(len(parent.nodes), 0)
        self.assertTrue(n1 not in parent.nodes)
        parent.add(n1)
        self.assertEqual(len(parent.nodes), 1)
        self.assertTrue(n1 in parent.nodes)
        self.assertTrue(n2 not in parent.nodes)
        parent.add(n2)
        self.assertEqual(len(parent.nodes), 2)
        self.assertTrue(n1 in parent.nodes)
        self.assertTrue(n2 in parent.nodes)

    def test_cycles(self):

        p = Node('project')

        a = p.add(Node('A', duration=3))
        b = p.add(Node('B', duration=3, lag=0))
        c = p.add(Node('C', duration=4, lag=0))
        d = p.add(Node('D', duration=6, lag=0))
        e = p.add(Node('E', duration=5, lag=0))

        p.link(a, b)
        p.link(a, c)
        p.link(a, d)
        p.link(b, e)
        p.link(c, e)
        p.link(d, e)

        self.assertEqual(p.is_acyclic(), True)

        p = Node('project')

        a = p.add(Node('A', duration=3))
        b = p.add(Node('B', duration=3, lag=0))
        c = p.add(Node('C', duration=4, lag=0))
        d = p.add(Node('D', duration=6, lag=0))
        e = p.add(Node('E', duration=5, lag=0))

        p.link(a, b)
        p.link(a, c)
        p.link(a, d)
        p.link(b, e)
        p.link(c, e)
        p.link(d, e)
        p.link(e, a) # links back!

        self.assertEqual(p.is_acyclic(), False)

    def test_project(self):

        p = Node('project')

        a = p.add(Node('A', duration=3))
        b = p.add(Node('B', duration=3, lag=0))
        c = p.add(Node('C', duration=4, lag=0))
        d = p.add(Node('D', duration=6, lag=0))
        e = p.add(Node('E', duration=5, lag=0))

        p.link(a, b)
        p.link(a, c)
        p.link(a, d)
        p.link(b, e)
        p.link(c, e)
        p.link(d, e)

        p.update_all()

#        for node in sorted(p.nodes, key=lambda n: n.name):
#            node.print_times()

        self.assertEqual(a.es, 0)
        self.assertEqual(a.ef, 3)
        self.assertEqual(a.ls, 0)
        self.assertEqual(a.lf, 3)
        self.assertEqual(b.es, 3)
        self.assertEqual(b.ef, 6)
        self.assertEqual(b.ls, 6)
        self.assertEqual(b.lf, 9)
        self.assertEqual(c.es, 3)
        self.assertEqual(c.ef, 7)
        self.assertEqual(c.ls, 5)
        self.assertEqual(c.lf, 9)
        self.assertEqual(d.es, 3)
        self.assertEqual(d.ef, 9)
        self.assertEqual(d.ls, 3)
        self.assertEqual(d.lf, 9)
        self.assertEqual(e.es, 9)
        self.assertEqual(e.ef, 14)
        self.assertEqual(e.ls, 9)
        self.assertEqual(e.lf, 14)

        critical_path = p.get_critical_path()
        #print critical_path
        self.assertEqual(critical_path, [a, d, e])
        self.assertEqual(p.duration, 14)
        self.assertEqual(p.es, 0)
        self.assertEqual(p.ef, 14)
        self.assertEqual(p.ls, 0)
        self.assertEqual(p.lf, 14)

    def test_acyclic(self):

        def test_graph(n):
            """Return an acyclic graph containing 2**n simple paths."""
            p = Node(name='graph')
            for i in range(n):
                from_id = 3 * i
                to_id1 = 3 * i + 1
                to_id2 = 3 * i + 2
                to_id3 = 3 * (i + 1)
                #i=0=>0,1,2,3
                #i=1=>3,4,5,6
                p.add(p.get_or_create_node(name=from_id, duration=1))
                p.add(p.get_or_create_node(name=to_id1, duration=1))
                p.add(p.get_or_create_node(name=to_id2, duration=1))
                p.add(p.get_or_create_node(name=to_id3, duration=1))
                p.link(from_id, to_id1)
                p.link(from_id, to_id2)
                p.link(to_id1, to_id3)
                p.link(to_id2, to_id3)
            return p

        for n in range(10, 20):
            print('checking n=%i' % n)
            g = test_graph(n)
            t = timeit(lambda: g.is_acyclic(), number=1)
            print('%i %.06f' % (n, t))

    def test_model_small(self):

        p = Node('project')

        times = pd.read_csv(os.path.join(BASE_DIR, 'fixtures/timings.dsv'), delimiter='|', dtype={'PROC_ID': str})
        deps = pd.read_csv(os.path.join(BASE_DIR, 'fixtures/deps_small.dsv'), delimiter='|', dtype={'PARENT_ID': str, 'UPROC_ID': str})

        # Define nodes with timings
        for utiming in times.itertuples(index=False):
            p.add(Node(utiming.PROC_ID, duration=utiming.DURATION))

        # Add dependencies to the model
        for dep in deps.itertuples(index=False):
            while True:
                try:
                    p.link(dep.PARENT_ID, dep.UPROC_ID)
                    break
                except KeyError as missingnode:
                    print('Missing node when adding dependency = ')
                    print(missingnode)
                    print(dep)
                    for errordep in dep:
                        p.add(Node(errordep, duration=0))
        p.update_all()
        critical_path = p.get_critical_path()
        print(critical_path)

    @unittest.skip('Too intensive for Travis. Runs fine locally, but takes about 10 minutes to complete.')
    def test_model_big(self):
        """
        A very large graph that tests the CPU and memory efficiency of our cyclic checker.
        """

        p = Node(name='project')

        times = pd.read_csv(os.path.join(BASE_DIR, 'fixtures/timings.dsv'), delimiter='|', dtype={'PROC_ID': str})
        deps = pd.read_csv(os.path.join(BASE_DIR, 'fixtures/deps_big.dsv'), delimiter='|', dtype={'PARENT_ID': str, 'UPROC_ID': str})

        # Define nodes with timings
        for utiming in times.itertuples(index=False):
            p.add(Node(name=utiming.PROC_ID, duration=utiming.DURATION))

        # Add dependencies to the model
        for dep in deps.itertuples(index=False):
            while True:
                try:
                    p.link(dep.PARENT_ID, dep.UPROC_ID)
                    break
                except KeyError as missingnode:
                    print('Missing node when adding dependency = ')
                    print(missingnode)
                    print(dep)
                    for errordep in dep:
                        p.add(Node(errordep, duration=0))
        p.update_all()
        critical_path = p.get_critical_path()
        print(critical_path)

if __name__ == '__main__':
    unittest.main()
