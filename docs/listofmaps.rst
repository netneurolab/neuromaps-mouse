.. _listofmaps:

------------
List of Maps
------------
This is a complete list of maps available in the `neuromaps_mouse` package. 

----

synaptome (zhu2018)
===================

**Full description**

Architecture of the Mouse Brain Synaptome

zhu2018-typedensity-allenccfv3-region
-------------------------------------

**Description**: Synaptic type density

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='zhu2018', desc='typedensity', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/zhu2018

    # file name
    # source-zhu2018_desc-typedensity_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-zhu2018_regionmapping.csv

**References**

----

structural connectome (oh2014)
==============================

**Full description**

A mesoscale connectome of the mouse brain

oh2014-wipsi-allenccfv3-region
------------------------------

**Description**: Weighted ipsilateral strength index

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='oh2014', desc='wipsi', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/oh2014

    # file name
    # source-oh2014_desc-wipsi_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-oh2014_regionmapping.csv

oh2014-pvalipsi-allenccfv3-region
---------------------------------

**Description**: P values for wipsi

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='oh2014', desc='pvalipsi', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/oh2014

    # file name
    # source-oh2014_desc-pvalipsi_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-oh2014_regionmapping.csv

oh2014-wcontra-allenccfv3-region
--------------------------------

**Description**: Weighted contralateral strength index

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='oh2014', desc='wcontra', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/oh2014

    # file name
    # source-oh2014_desc-wcontra_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-oh2014_regionmapping.csv

oh2014-pvalcontra-allenccfv3-region
-----------------------------------

**Description**: P values for wcontra

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='oh2014', desc='pvalcontra', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/oh2014

    # file name
    # source-oh2014_desc-pvalcontra_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-oh2014_regionmapping.csv

oh2014-distipsi-allenccfv3-region
---------------------------------

**Description**: Distance (mm) for ipsilateral projections

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='oh2014', desc='distipsi', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/oh2014

    # file name
    # source-oh2014_desc-distipsi_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-oh2014_regionmapping.csv

oh2014-distcontra-allenccfv3-region
-----------------------------------

**Description**: Distance (mm) for contralateral projections

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='oh2014', desc='distcontra', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/oh2014

    # file name
    # source-oh2014_desc-distcontra_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-oh2014_regionmapping.csv

**References**

----

cell type density (ero2018)
===========================

**Full description**

A Cell Atlas for the Mouse Brain

ero2018-celldensity-allenccfv3-region
-------------------------------------

**Description**: Density of cell types

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='ero2018', desc='celldensity', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/ero2018

    # file name
    # source-ero2018_desc-celldensity_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-ero2018_regionmapping.csv

**References**

----

Allen Mouse Brain Atlas (lein2006amba)
======================================

**Full description**

Allen Mouse Brain Atlas

lein2006amba-sagittalenergy-allenccfv3-region
---------------------------------------------

**Description**: Expression energy of sagittal slices

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='lein2006amba', desc='sagittalenergy', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/lein2006amba

    # file name
    # source-lein2006amba_desc-sagittalenergy_space-allenccfv3_res-region_tabular.csv.gz

    # region mapping file
    # source-lein2006amba_regionmapping.csv

lein2006amba-coronalenergy-allenccfv3-region
--------------------------------------------

**Description**: Expression energy of coronal slices

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='lein2006amba', desc='coronalenergy', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/lein2006amba

    # file name
    # source-lein2006amba_desc-coronalenergy_space-allenccfv3_res-region_tabular.csv.gz

    # region mapping file
    # source-lein2006amba_regionmapping.csv

lein2006amba-sagittaldensity-allenccfv3-region
----------------------------------------------

**Description**: Expression density of sagittal slices

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='lein2006amba', desc='sagittaldensity', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/lein2006amba

    # file name
    # source-lein2006amba_desc-sagittaldensity_space-allenccfv3_res-region_tabular.csv.gz

    # region mapping file
    # source-lein2006amba_regionmapping.csv

lein2006amba-coronaldensity-allenccfv3-region
---------------------------------------------

**Description**: Expression density of coronal slices

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='lein2006amba', desc='coronaldensity', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/lein2006amba

    # file name
    # source-lein2006amba_desc-coronaldensity_space-allenccfv3_res-region_tabular.csv.gz

    # region mapping file
    # source-lein2006amba_regionmapping.csv

lein2006amba-sagittalintensity-allenccfv3-region
------------------------------------------------

**Description**: Expression intensity of sagittal slices

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='lein2006amba', desc='sagittalintensity', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/lein2006amba

    # file name
    # source-lein2006amba_desc-sagittalintensity_space-allenccfv3_res-region_tabular.csv.gz

    # region mapping file
    # source-lein2006amba_regionmapping.csv

lein2006amba-coronalintensity-allenccfv3-region
-----------------------------------------------

**Description**: Expression intensity of coronal slices

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='lein2006amba', desc='coronalintensity', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/lein2006amba

    # file name
    # source-lein2006amba_desc-coronalintensity_space-allenccfv3_res-region_tabular.csv.gz

    # region mapping file
    # source-lein2006amba_regionmapping.csv

**References**

----

ABC Atlas (MERFISH-C57BL6J-638850) (yao2023abca)
================================================

**Full description**

Mouse whole-brain transcriptomic cell type atlas (Hongkui Zeng)

yao2023abca-divimean-allenccfv3-region
--------------------------------------

**Description**: Average regional gene expressions at the division level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='divimean', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-divimean_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_division_regionmapping.csv

yao2023abca-strumean-allenccfv3-region
--------------------------------------

**Description**: Average regional gene expressions at the structure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='strumean', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-strumean_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_structure_regionmapping.csv

yao2023abca-subsmean-allenccfv3-region
--------------------------------------

**Description**: Average regional gene expressions at the substructure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='subsmean', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-subsmean_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_substructure_regionmapping.csv

yao2023abca-impdivimean-allenccfv3-region
-----------------------------------------

**Description**: Average imputed regional gene expressions at the division level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='impdivimean', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-impdivimean_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_division_regionmapping.csv

yao2023abca-impstrumean-allenccfv3-region
-----------------------------------------

**Description**: Average imputed regional gene expressions at the structure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='impstrumean', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-impstrumean_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_structure_regionmapping.csv

yao2023abca-impsubsmean-allenccfv3-region
-----------------------------------------

**Description**: Average imputed regional gene expressions at the substructure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='impsubsmean', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-impsubsmean_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_substructure_regionmapping.csv

yao2023abca-divictclass-allenccfv3-region
-----------------------------------------

**Description**: Cell type (class) at the division level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='divictclass', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-divictclass_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_division_regionmapping.csv

yao2023abca-structclass-allenccfv3-region
-----------------------------------------

**Description**: Cell type (class) at the structure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='structclass', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-structclass_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_structure_regionmapping.csv

yao2023abca-subsctclass-allenccfv3-region
-----------------------------------------

**Description**: Cell type (class) at the substructure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='subsctclass', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-subsctclass_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_substructure_regionmapping.csv

yao2023abca-divictsubclass-allenccfv3-region
--------------------------------------------

**Description**: Cell type (subclass) at the division level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='divictsubclass', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-divictsubclass_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_division_regionmapping.csv

yao2023abca-structsubclass-allenccfv3-region
--------------------------------------------

**Description**: Cell type (subclass) at the structure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='structsubclass', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-structsubclass_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_structure_regionmapping.csv

yao2023abca-subsctsubclass-allenccfv3-region
--------------------------------------------

**Description**: Cell type (subclass) at the substructure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='subsctsubclass', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-subsctsubclass_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_substructure_regionmapping.csv

yao2023abca-divictsupertype-allenccfv3-region
---------------------------------------------

**Description**: Cell type (supertype) at the division level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='divictsupertype', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-divictsupertype_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_division_regionmapping.csv

yao2023abca-structsupertype-allenccfv3-region
---------------------------------------------

**Description**: Cell type (supertype) at the structure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='structsupertype', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-structsupertype_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_structure_regionmapping.csv

yao2023abca-subsctsupertype-allenccfv3-region
---------------------------------------------

**Description**: Cell type (supertype) at the substructure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='subsctsupertype', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-subsctsupertype_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_substructure_regionmapping.csv

yao2023abca-divictcluster-allenccfv3-region
-------------------------------------------

**Description**: Cell type (cluster) at the division level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='divictcluster', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-divictcluster_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_division_regionmapping.csv

yao2023abca-structcluster-allenccfv3-region
-------------------------------------------

**Description**: Cell type (cluster) at the structure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='structcluster', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-structcluster_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_structure_regionmapping.csv

yao2023abca-subsctcluster-allenccfv3-region
-------------------------------------------

**Description**: Cell type (cluster) at the substructure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='yao2023abca', desc='subsctcluster', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/yao2023abca

    # file name
    # source-yao2023abca_desc-subsctcluster_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-yao2023abca_substructure_regionmapping.csv

**References**

----

ABC Atlas (Zhuang-ABCA) (zhang2023abca)
=======================================

**Full description**

A molecularly defined and spatially resolved cell atlas of the whole mouse brain (Xiaowei Zhuang)

zhang2023abca-divimean-allenccfv3-region
----------------------------------------

**Description**: Average regional gene expressions at the division level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='zhang2023abca', desc='divimean', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/zhang2023abca

    # file name
    # source-zhang2023abca_desc-divimean_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-zhang2023abca_division_regionmapping.csv

zhang2023abca-strumean-allenccfv3-region
----------------------------------------

**Description**: Average regional gene expressions at the structure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='zhang2023abca', desc='strumean', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/zhang2023abca

    # file name
    # source-zhang2023abca_desc-strumean_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-zhang2023abca_structure_regionmapping.csv

zhang2023abca-subsmean-allenccfv3-region
----------------------------------------

**Description**: Average regional gene expressions at the substructure level

**Format**: tabular

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='zhang2023abca', desc='subsmean', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/zhang2023abca

    # file name
    # source-zhang2023abca_desc-subsmean_space-allenccfv3_res-region_tabular.csv

    # region mapping file
    # source-zhang2023abca_substructure_regionmapping.csv

**References**

----

hi-res connectome (knox2018)
============================

**Full description**

 High-resolution data-driven model of the mouse connectome

knox2018-conndencontra-allenccfv3-region
----------------------------------------

**Description**: Connection density (contralateral)

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='knox2018', desc='conndencontra', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/knox2018

    # file name
    # source-knox2018_desc-conndencontra_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-knox2018_regionmapping.csv

knox2018-conndenipsi-allenccfv3-region
--------------------------------------

**Description**: Connection density (ipsilateral)

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='knox2018', desc='conndenipsi', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/knox2018

    # file name
    # source-knox2018_desc-conndenipsi_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-knox2018_regionmapping.csv

knox2018-connstrcontra-allenccfv3-region
----------------------------------------

**Description**: Connection strength (contralateral)

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='knox2018', desc='connstrcontra', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/knox2018

    # file name
    # source-knox2018_desc-connstrcontra_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-knox2018_regionmapping.csv

knox2018-connstripsi-allenccfv3-region
--------------------------------------

**Description**: Connection strength (ipsilateral)

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='knox2018', desc='connstripsi', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/knox2018

    # file name
    # source-knox2018_desc-connstripsi_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-knox2018_regionmapping.csv

knox2018-normconndencontra-allenccfv3-region
--------------------------------------------

**Description**: Normalized connection density (contralateral)

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='knox2018', desc='normconndencontra', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/knox2018

    # file name
    # source-knox2018_desc-normconndencontra_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-knox2018_regionmapping.csv

knox2018-normconndenipsi-allenccfv3-region
------------------------------------------

**Description**: Normalized connection density (ipsilateral)

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='knox2018', desc='normconndenipsi', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/knox2018

    # file name
    # source-knox2018_desc-normconndenipsi_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-knox2018_regionmapping.csv

knox2018-normconnstrcontra-allenccfv3-region
--------------------------------------------

**Description**: Normalized connection strength (contralateral)

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='knox2018', desc='normconnstrcontra', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/knox2018

    # file name
    # source-knox2018_desc-normconnstrcontra_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-knox2018_regionmapping.csv

knox2018-normconnstripsi-allenccfv3-region
------------------------------------------

**Description**: Normalized connection strength (ipsilateral)

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='knox2018', desc='normconnstripsi', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/knox2018

    # file name
    # source-knox2018_desc-normconnstripsi_space-allenccfv3_res-region_matrix.csv

    # region mapping file
    # source-knox2018_regionmapping.csv

**References**