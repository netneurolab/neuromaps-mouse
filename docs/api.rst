.. _api_ref:

.. currentmodule:: neuromaps_mouse

Reference API
=============

.. contents:: **List of modules**
   :local:

.. _ref_datasets:

:mod:`neuromaps_mouse.datasets` - Dataset fetchers
--------------------------------------------
.. automodule:: neuromaps_mouse.datasets
   :no-members:
   :no-inherited-members:

.. currentmodule:: neuromaps_mouse.datasets

Functions to show all available annotations

.. autosummary::
   :template: function.rst
   :toctree: generated/

   neuromaps_mouse.datasets.available_annotations

Functions to fetch and describe the annotations

.. autosummary::
   :template: function.rst
   :toctree: generated/

   neuromaps_mouse.datasets.fetch_annotation

Functions to fetch the atlases

.. autosummary::
   :template: function.rst
   :toctree: generated/

   neuromaps_mouse.datasets.fetch_allenccfv3
   neuromaps_mouse.datasets.fetch_all_atlases

Support functions

.. autosummary::
   :template: function.rst
   :toctree: generated/

   neuromaps_mouse.datasets.get_data_dir

.. _ref_images:

:mod:`neuromaps_mouse.images` - Image and surface handling
----------------------------------------------------
.. automodule:: neuromaps_mouse.images
   :no-members:
   :no-inherited-members:

.. currentmodule:: neuromaps_mouse.images

Functions to load the images and surfaces

.. autosummary::
   :template: function.rst
   :toctree: generated/

   neuromaps_mouse.images.load_region_data
   neuromaps_mouse.images.load_image_data

.. _ref_plotting:

:mod:`neuromaps_mouse.plotting` - Plotting functions
----------------------------------------------
.. automodule:: neuromaps_mouse.plotting
   :no-members:
   :no-inherited-members:

.. currentmodule:: neuromaps_mouse.plotting

.. autosummary::
   :template: function.rst
   :toctree: generated/

   neuromaps_mouse.plotting.plot_allenccfv3_ortho
   neuromaps_mouse.plotting.plot_allenccfv3_ortho_asym
   neuromaps_mouse.plotting.plot_allenccfv3_lightbox
   neuromaps_mouse.plotting.plot_allenccfv3_3d

.. _ref_resampling:

:mod:`neuromaps_mouse.resampling` - Resampling workflows
--------------------------------------------------
.. automodule:: neuromaps_mouse.resampling
    :no-members:
    :no-inherited-members:

.. currentmodule:: neuromaps_mouse.resampling

.. autosummary::
    :template: function.rst
    :toctree: generated/

    neuromaps_mouse.resampling.query_structure_graph_allenccfv3
    neuromaps_mouse.resampling.get_feature_allenccfv3
    neuromaps_mouse.resampling.align_structures_allenccfv3
    neuromaps_mouse.resampling.match_allenccfv3_structures_fuzzy

.. _ref_stats:

:mod:`neuromaps_mouse.stats` - Statistical functions
----------------------------------------------
.. automodule:: neuromaps_mouse.stats
    :no-members:
    :no-inherited-members:

.. currentmodule:: neuromaps_mouse.stats

.. autosummary::
    :template: function.rst
    :toctree: generated/

    neuromaps_mouse.stats.correlation

.. _ref_transforms:

:mod:`neuromaps_mouse.transforms` - Transformations between spaces
------------------------------------------------------------
.. automodule:: neuromaps_mouse.transforms
   :no-members:
   :no-inherited-members:

.. currentmodule:: neuromaps_mouse.transforms

.. autosummary::
   :template: function.rst
   :toctree: generated/

   neuromaps_mouse.transforms.allenccfv3_to_allenccfv3