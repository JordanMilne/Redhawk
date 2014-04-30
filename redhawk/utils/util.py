from __future__ import print_function
#!/usr/bin/env python
import redhawk

import hashlib
import operator
import os
import sys

try:
    reduce
except NameError:
    from functools import reduce

def Concat(li):
  """ Concat :: [[a]] -> [a].
      similar to Haskell's concat."""
  return reduce(operator.concat, li)

def Flatten(li):
  """ Returns a generator that is a flattened out version of the original
      list.
      Example:
        Flatten([1, 2, [3, 4]])     ->  [1, 2, 3, 4]
        Flatten([[1, [2]], [3, 4]]) ->  [1, 2, 3, 4]
  """
  flat = []
  for x in li:
    if type(x) == list:
      flat.extend(Flatten(x))
    else:
      flat.append(x)
  return flat


def GetHashDigest(filename):
  """ Get the sha1 digest of `filename`)"""
  with open(filename, 'rb') as fp:
      return hashlib.sha1(fp.read()).hexdigest()


def GuessLanguage(filename):
  """ Attempts to Guess Langauge of `filename`. Essentially, we do a
  filename.rsplit('.', 1), and a lookup into a dictionary of extensions."""
  try:
    (_, extension) = filename.rsplit('.', 1)
  except ValueError:
    raise ValueError("Could not guess language as '%s' does not have an \
        extension"%filename)

  return {'c'   : 'c'
         ,'py'  : 'python'}[extension] 


def IndexInto(li, indices):
  """ Index into a list (or list of lists) using the indices given. If the
  indices are out of bounds, or are too many in number, return None, instead
  of throwing an error. 0 is a special case."""
  for i in indices:
    if type(li) != list and i == 0:
      return li
    if type(li) != list or i >= len(li):
      return None

    li = li[i]
  return li

def LogWarning(s, stream=sys.stderr):
  """ Log a warning to `stream` (default: sys.stderr.)"""
  stream.write("[WARNING]: %s\n"%(s))
  return


def StartShell(local_vars, banner='', try_ipython=True):
  """ Start a shell, with the given local variables. It prints the given
  banner as a welcome message."""

  def IPythonShell(namespace, banner):
    from IPython import start_ipython
    sys.argv = ['']  # This is needed because argparse tries to grab argv[0]
    from IPython.config import Config
    c = Config()
    c.TerminalInteractiveShell.banner1 = banner
    start_ipython(user_ns=namespace, argv=[], config=c)

  def PythonShell(namespace, banner):
    import readline, rlcompleter, code 
    readline.parse_and_bind("tab: complete")
    readline.set_completer(rlcompleter.Completer(namespace).complete)
    code.interact(local=namespace, banner=banner)

  if try_ipython:
    try:
      return IPythonShell(local_vars, banner)
    except ImportError:
      pass

  PythonShell(local_vars, banner)

def FindFileInDirectoryOrAncestors(filename, dirname, perm=os.R_OK | os.W_OK):
  """ Tries to find the file `filename` in the given directory `dirname` or
  its parents. When found it makes sure the permissions match the given
  `perm`. If no file is found, None is returned. If the file was found, but
  the permissions are not satisfied, it raises an IOError."""
  dirname = os.path.abspath(dirname)

  while not os.path.exists(os.path.join(dirname, filename)):
    parent_dirname = os.path.dirname(dirname)
    if dirname == parent_dirname:
      return None
    dirname = parent_dirname

  filepath = os.path.join(dirname, filename)
  if os.access(filepath, perm) is False:
    raise IOError("Read write permissions deny access to file %s"%(filepath))

  return filepath

def GetDBPathRelativeToCurrentDirectory(filepath):
  database_dir = os.path.dirname(
      FindFileInDirectoryOrAncestors(
        redhawk.GetDBName(),
        os.curdir))

  abs_filepath = os.path.join(database_dir, filepath)
  return os.path.relpath(abs_filepath, os.curdir)

def GetRelativeFilePath(filepath):
  """ Try to open the file. If not, we try to open the filepath as one
  relative to the redhawk database."""
  if os.path.exists(filepath):
    return os.path.relpath(filepath)

  return GetDBPathRelativeToCurrentDirectory(filepath)
