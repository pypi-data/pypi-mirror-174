# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cacp']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'joblib>=1.1.0,<2.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.21.6,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'river>=0.11.1,<0.12.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'cacp',
    'version': '0.3.0',
    'description': '',
    'long_description': "===================================================\nCACP: Classification Algorithms Comparison Pipeline\n===================================================\n\n\n.. image:: https://img.shields.io/pypi/v/cacp.svg\n        :target: https://pypi.python.org/pypi/cacp\n\n.. image:: https://github.com/sylwekczmil/cacp/actions/workflows/tox.yml/badge.svg\n        :target: https://github.com/sylwekczmil/cacp/actions/workflows/tox.yml\n\n\n.. image:: https://readthedocs.org/projects/cacp/badge/?version=latest\n        :target: https://cacp.readthedocs.io/en/latest/?version=latest\n        :alt: Documentation Status\n\n* Free software: MIT license\n* Documentation: https://cacp.readthedocs.io.\n* Article: https://doi.org/10.1016/j.softx.2022.101134\n\n\nDescription\n-------------\n\nCACP is made for comparing newly developed classification algorithms (both traditional and incremental) in Python with other commonly used classifiers to evaluate classification performance, reproducibility, and statistical reliability. CACP simplifies the entire classifier evaluation process.\n\nInstallation\n--------------\n\nTo install cacp, run this command in your terminal:\n\n.. code-block:: console\n\n    pip install cacp\n\n\nUsage\n------\nJupyter Notebook on Kaggle:\nhttps://www.kaggle.com/sc4444/cacp-example-usage\n\n\nSimple Usage\n--------------\nAn example usage of this library is included in the package:\nhttps://github.com/sylwekczmil/cacp/tree/main/cacp_examples_simple.\n\n.. code:: python3\n\n    from sklearn.ensemble import RandomForestClassifier\n    from sklearn.neighbors import KNeighborsClassifier\n    from sklearn.svm import SVC\n    from sklearn.tree import DecisionTreeClassifier\n\n    from cacp import run_experiment, ClassificationDataset\n\n    # select datasets\n    experimental_datasets = [\n        ClassificationDataset('iris'),\n        ClassificationDataset('wisconsin'),\n        ClassificationDataset('pima'),\n        ClassificationDataset('wdbc'),\n    ]\n\n    # select classifiers\n    experimental_classifiers = [\n        ('SVC', lambda n_inputs, n_classes: SVC()),\n        ('DT', lambda n_inputs, n_classes: DecisionTreeClassifier(max_depth=5)),\n        ('RF', lambda n_inputs, n_classes: RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),\n        ('KNN', lambda n_inputs, n_classes: KNeighborsClassifier(3)),\n    ]\n\n    # trigger experiment run\n    run_experiment(\n        experimental_datasets,\n        experimental_classifiers,\n        results_directory='./example_result'\n    )\n\n\nAdvanced Usage\n---------------\n\nAn advanced example usage of this library is included in the package:\nhttps://github.com/sylwekczmil/cacp/tree/main/cacp_examples.\n\n.. code:: python3\n\n    from sklearn.neighbors import KNeighborsClassifier\n    from skmultiflow.lazy import KNNClassifier\n    from skmultiflow.meta import LearnPPNSEClassifier\n\n    from cacp import all_datasets, run_experiment, ClassificationDataset\n    from cacp_examples.classifiers import CLASSIFIERS\n    from cacp_examples.example_custom_classifiers.xgboost import XGBoost\n\n    # you can specify datasets by name, all of them will be automatically downloaded\n    experimental_datasets_example = [\n        ClassificationDataset('iris'),\n        ClassificationDataset('wisconsin'),\n        ClassificationDataset('pima'),\n        ClassificationDataset('sonar'),\n        ClassificationDataset('wdbc'),\n    ]\n    # or use all datasets\n    experimental_datasets = all_datasets()\n\n    # same for classifiers, you can specify list of classifiers\n    experimental_classifiers_example = [\n        ('KNN_3', lambda n_inputs, n_classes: KNeighborsClassifier(3)),\n        # you can define classifiers multiple times with different parameters\n        ('KNN_5', lambda n_inputs, n_classes: KNeighborsClassifier(5)),\n        # you can use classifiers from any lib that\n        # supports fit/predict methods eg. scikit-learn/scikit-multiflow\n        ('KNNI', lambda n_inputs, n_classes: KNNClassifier(n_neighbors=3)),\n        # you can also use wrapped algorithms from other libs or custom implementations\n        ('XGB', lambda n_inputs, n_classes: XGBoost()),\n        ('LPPNSEC', lambda n_inputs, n_classes: LearnPPNSEClassifier())\n    ]\n    # or you can use predefined ones\n    experimental_classifiers = CLASSIFIERS\n\n    # this is how you trigger experiment run\n    run_experiment(\n        experimental_datasets,\n        experimental_classifiers,\n        results_directory='./example_result'\n    )\n\n\nDefining custom classifier wrapper:\nhttps://github.com/sylwekczmil/cacp/tree/main/cacp_examples/example_custom_classifiers/xgboost.py.\n\nDefining custom dataset:\nhttps://github.com/sylwekczmil/cacp/tree/main/cacp_examples/example_custom_datasets/random_dataset.py\n\nDefining local dataset:\nhttps://github.com/sylwekczmil/cacp/tree/main/cacp_examples/example_custom_datasets/local_dataset.py\n\n\nIncremental Algorithms Usage\n-----------------------------\nAn example usage of this library for incremental classifiers is included in the package:\nhttps://github.com/sylwekczmil/cacp/tree/main/cacp_examples_incremental.\n\n.. code:: python3\n\n    import river\n    from river.ensemble import AdaptiveRandomForestClassifier\n    from river.naive_bayes import GaussianNB\n    from river.neighbors import KNNClassifier\n    from river.tree import HoeffdingTreeClassifier\n\n    from cacp import run_incremental_experiment, ClassificationDataset\n\n    if __name__ == '__main__':\n        # select datasets\n        experimental_datasets = [\n            ClassificationDataset('iris'),\n            ClassificationDataset('wisconsin'),\n            # you can use datasets from river\n            river.datasets.Phishing(),\n            river.datasets.Bananas(),\n\n        ]\n\n        # select incremental classifiers\n        experimental_classifiers = [\n            ('ARF', lambda n_inputs, n_classes: AdaptiveRandomForestClassifier()),\n            ('HAT', lambda n_inputs, n_classes: HoeffdingTreeClassifier()),\n            ('KNN', lambda n_inputs, n_classes: KNNClassifier()),\n            ('GNB', lambda n_inputs, n_classes: GaussianNB()),\n        ]\n\n        # trigger experiment run\n        run_incremental_experiment(\n            experimental_datasets,\n            experimental_classifiers,\n            results_directory='./example_result'\n        )\n\n",
    'author': 'Sylwester Czmil',
    'author_email': 'sylwekczmil@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
