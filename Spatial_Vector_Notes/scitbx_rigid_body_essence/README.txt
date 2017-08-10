scitbx_rigid_body_essence
=========================

- A subset of ``scitbx/rigid_body/essence`` that can be used in isolation.

- Plain Python code for rigid body dynamics and gradient-driven minimization.

- Main reference::

    Rigid Body Dynamics Algorithms.
    Roy Featherstone,
    Springer, New York, 2007.
    ISBN-10: 0387743146

- `Open Source License <http://cctbx.svn.sourceforge.net/viewvc/cctbx/trunk/cctbx/LICENSE_2_0.txt?view=markup>`_

Context
-------

``scitbx/rigid_body/essence`` grew out of the development of the
dynamics engine for the ``phenix.refine`` **torsion angle dynamics**
module, which is used as a complementary method to gradient-driven
minimization, as a way to escape from local minima. See also:

  - Rice & Brunger (1994). Proteins: Structure, Function, and Genetics 19, 277-290.

  - http://phenix-online.org/

Nomenclature
------------

The variable names in the ``scitbx/rigid_body/essence`` source code
follow the nomenclature used in Featherstone's *Rigid Body Dynamics
Algorithms* as much as possible. Numerous ``RBDA`` comments point to
equations, tables, and figures in the book. **When using the source
code, it will be essential to have the book available as an introduction
and reference.**

Details
-------

Files::

  featherstone.py:   dynamics algorithms, based on Roy Featherstone's Matlab library
  spatial_lib.py:    spatial algebra, also based on Roy Featherstone's library
  joint_lib.py:      some joint models
  body_lib.py:       corresponding body objects
  scitbx_matrix.py:  general matrix algorithm (copy of scitbx/matrix/__init__.py)
  tst_basic.py:      unit tests compatible with Python 2.2 or higher

Download all files at once:

  - http://cctbx.sourceforge.net/scitbx_rigid_body_essence.tgz
  - http://cctbx.sourceforge.net/scitbx_rigid_body_essence.zip

To run the unit tests::

  cd scitbx_rigid_body_essence
  python tst_basic.py

The full scitbx/rigid_body functionality requires compiled modules,
written in C++. Download the entire scitbx from here:

  - http://cci.lbl.gov/scitbx_bundles/current/

or the entire cctbx (of which scitbx is a subset) from here:

  - http://cci.lbl.gov/cctbx_build/

Follow the instructions on the latter page to install the cctbx or
scitbx bundles (e.g. ``perl scitbx_bundle.selfx``).

The cctbx source tree is hosted at SourceForge. The latest versions
of the files in scitbx_rigid_body_essence can be found here:

  - http://cctbx.svn.sourceforge.net/viewvc/cctbx/trunk/scitbx/rigid_body/essence/

A version of featherstone.py that's closer to Roy Featherstone's original
Matlab code can be found here:

  - http://cctbx.svn.sourceforge.net/viewvc/cctbx/trunk/scitbx/rigid_body/proto/

The file ``wx_tardy.py`` is a simple 3D graphical viewer displaying
trajectories. It requires ``wxPython`` and the ``gltbx`` module of
the cctbx project. An easy way to get everything in one file and
install with a single command, is to download the phenix package from:

  - http://phenix-online.org/

Send questions to: cctbx@cci.lbl.gov or cctbxbb@phenix-online.org
