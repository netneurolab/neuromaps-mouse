.. _api_ref:

.. currentmodule:: mousemaps

Reference API
=============

.. contents:: **List of modules**
   :local:

.. _ref_datasets:

:mod:`mousemaps.datasets` - Dataset fetchers
--------------------------------------------
.. automodule:: mousemaps.datasets
   :no-members:
   :no-inherited-members:

.. currentmodule:: mousemaps.datasets

Functions to show all available annotations

.. autosummary::
   :template: function.rst
   :toctree: generated/

   mousemaps.datasets.available_annotations

Functions to fetch and describe the annotations

.. autosummary::
   :template: function.rst
   :toctree: generated/

   mousemaps.datasets.fetch_annotation

Functions to fetch the atlases

.. autosummary::
   :template: function.rst
   :toctree: generated/

   mousemaps.datasets.fetch_allenccfv3
   mousemaps.datasets.fetch_all_atlases
   mousemaps.datasets.get_atlas_dir

.. _ref_images:

:mod:`mousemaps.images` - Image and surface handling
----------------------------------------------------
.. automodule:: mousemaps.images
   :no-members:
   :no-inherited-members:

.. currentmodule:: mousemaps.images

Functions to load the images and surfaces

.. autosummary::
   :template: function.rst
   :toctree: generated/

   mousemaps.images.load_region_data
   mousemaps.images.load_image_data

.. _ref_plotting:

:mod:`mousemaps.plotting` - Plotting functions
----------------------------------------------
.. automodule:: mousemaps.plotting
   :no-members:
   :no-inherited-members:

.. currentmodule:: mousemaps.plotting

.. autosummary::
   :template: function.rst
   :toctree: generated/

   mousemaps.plotting.plot_allenccfv3_ortho
   mousemaps.plotting.plot_allenccfv3_ortho_asym
   mousemaps.plotting.plot_allenccfv3_lightbox
   mousemaps.plotting.plot_allenccfv3_3d

.. _ref_resampling:

:mod:`mousemaps.resampling` - Resampling workflows
--------------------------------------------------
.. automodule:: mousemaps.resampling
    :no-members:
    :no-inherited-members:

.. currentmodule:: mousemaps.resampling

.. autosummary::
    :template: function.rst
    :toctree: generated/

    mousemaps.resampling.query_structure_graph_allenccfv3
    mousemaps.resampling.get_feature_allenccfv3
    mousemaps.resampling.align_structures_allenccfv3
    mousemaps.resampling.match_allenccfv3_structures_fuzzy

.. _ref_stats:

:mod:`mousemaps.stats` - Statistical functions
----------------------------------------------
.. automodule:: mousemaps.stats
    :no-members:
    :no-inherited-members:

.. currentmodule:: mousemaps.stats

.. autosummary::
    :template: function.rst
    :toctree: generated/

    mousemaps.stats.correlation

.. _ref_transforms:

:mod:`mousemaps.transforms` - Transformations between spaces
------------------------------------------------------------
.. automodule:: mousemaps.transforms
   :no-members:
   :no-inherited-members:

.. currentmodule:: mousemaps.transforms

.. autosummary::
   :template: function.rst
   :toctree: generated/

   mousemaps.transforms.allenccfv3_to_allenccfv3