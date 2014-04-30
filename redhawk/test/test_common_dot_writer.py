#!/usr/bin/env python
""" Test the DotWriter module in redhawk/common/writers."""

from . import common_test_utils as T

import nose.tools
from unittest import skipIf

import random
import itertools
import tempfile
import os
import sys

PY3 = sys.version_info[0] >= 3

TEST_DIR = os.path.dirname(__file__)
DOT_FILES = os.path.join(TEST_DIR, 'files', 'dot')

class TestDotWriter:
  def __init__(self):
    self.counter = itertools.count(0)
    self.temp_dir = tempfile.mkdtemp(prefix='images')
    return

  def GetFilename(self):
    i = self.counter.next()
    return os.path.join(self.temp_dir, str(i))

  def FunctionTestDot(self, ast):
    v = self.GetFilename()
    import redhawk.common.writers.dot_writer as D
    open(v + '.dot', "w").write(D.WriteToDot(ast))
    D.WriteToImage(ast, filename = v + '.png')
    return


test_dot_writer = TestDotWriter()

@skipIf(PY3, "pygraphviz isn't ported to Python 3")
def TestGenerator():
  """ Testing Dot Writer. """
  PICK=1
  all_asts = list(T.GetAllLASTs())
  for i in range(PICK):
    r_index = random.randrange(0, len(all_asts))
    test_dot_writer.FunctionTestDot.im_func.description = "Test Random AST (%d) with Dot Writer."%(r_index)
    yield test_dot_writer.FunctionTestDot, all_asts[r_index]

@skipIf(PY3, "pygraphviz isn't ported to Python 3")
def TestDotNewlineSupport():
  """ Test Dot for programs with newlines in keys/attr strings."""
  test_dot_writer.FunctionTestDot(T.GetLASTFromFile(
    os.path.join(DOT_FILES, "newline.c"), "c", None))
  test_dot_writer.FunctionTestDot(T.GetLASTFromFile(
    os.path.join(DOT_FILES, "newline.py"), "python", None))
  return


# Disable the test by default.
@nose.tools.nottest
@skipIf(PY3, "pygraphviz isn't ported to Python 3")
def TestAllPrograms():
  """ Testing Dot Writer (all programs) """
  all_asts = list(T.GetAllLASTs())
  for (i, ast) in enumerate(all_asts):
    test_dot_writer.FunctionTestDot.im_func.description = "Testing AST (%d) with Dot Writer."%(i)
    yield test_dot_writer.FunctionTestDot, ast
