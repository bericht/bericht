Coding Guidelines
=================

You probably read this because you decided to contribute to Bericht. That's
nice and highly appreciated, but please make sure that your code respects the 
following conventions before you push code into our repositories.


PEP8
----

Python comes with its own opinionated style guide, which is called
`pep8 <http://www.python.org/dev/peps/pep-0008/>`_ and available online.
We use `flake8 <https://pypi.python.org/pypi/flake8>`_ to check if our code
respects pep8 and does not contain known symptoms of common problems ("code
smell").

.. NOTE::
   It is strongly recommended to use a git hook to ensure that you are only
   committing code which does satisfy flake8. We might reject code that does
   not!

To use such a git hook, create a file in ``.git/hooks/pre-commit`` with
the following contents::

  #!/usr/bin/env python

  import os
  import subprocess
  import sys


  def system(*args, **kwargs):
      kwargs.setdefault('stdout', subprocess.PIPE)
      proc = subprocess.Popen(args, **kwargs)
      out, err = proc.communicate()
      return out

  def main():
      project_dir = os.path.dirname(os.path.dirname(
          os.path.dirname(os.path.realpath(__file__))))
      print(project_dir)
      output = system('flake8', '.', cwd=project_dir)
      if output:
          print output,
          sys.exit(1)

  if __name__ == '__main__':
      main()

and make it executable::

  chmod +x .git/hooks/pre-commit

.. HINT::
   If you are absolutely certain that a file should not be checked, add
   ``# flake8: noqa`` to the beginning of that file. This should only
   be used for configuration of used tools or auto-generated code like
   migrations, never for production code!

Tests
-----

Please write tests whenever you add or change functionality and run existing
tests before you push. We use Djangos tools which are based on Pythons 
`unittest <http://docs.python.org/2.7/library/unittest.html#module-unittest>`_
module. There is a `short overview
<https://docs.djangoproject.com/en/1.6/topics/testing/overview/>`_ as well
as a `longer tutorial
<https://docs.djangoproject.com/en/1.6/intro/tutorial05/>`_ available on
Djangos website.

A test suite for client-side javascript tests must yet be chosen.
