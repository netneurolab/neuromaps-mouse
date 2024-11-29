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

zhu2018-similarity-allenccfv3-region
------------------------------------

**Description**: Synaptic similarity

**Format**: matrix

**How to use**

.. code:: python

    # get annotation
    fetch_annotation(source='zhu2018', desc='similarity', space='allenccfv3', res='region')

    # file location
    # $MOUSEMAPS_DATA/zhu2018

    # file name
    # source-zhu2018_desc-similarity_space-allenccfv3_res-region_matrix.csv

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
    # source-lein2006amba_desc-sagittalenergy_space-allenccfv3_res-region_tabular.csv

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
    # source-lein2006amba_desc-coronalenergy_space-allenccfv3_res-region_tabular.csv

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