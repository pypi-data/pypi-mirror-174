PET dataset reader
##################

ATTENTION: ALPHA VERSION

Benchmarking procedure to test approaches on the `PET-dataset`_ (hosted on huggingface_).

.. _PET-dataset: https://pdi.fbk.eu/pet-dataset/
.. _huggingface: https://huggingface.co/datasets/patriziobellan/PET

This is an beta version.

Documentation will come soon.

Example of ''how to benchmark an approach''
*******************************************


.. code-block:: python

    from petbenchmarks.benchmarks import BenchmarkApproach

    BenchmarkApproach(tested_approach_name='Approach-name',
                      predictions_file_or_folder='path-to-prediction-file.json')


The ``BenchmarkApproach`` object does all the job.
It reads the prediction file, computes score and generates a reports.


Created by `Patrizio Bellan`_.

.. _Patrizio Bellan: https://pdi.fbk.eu/bellan/

