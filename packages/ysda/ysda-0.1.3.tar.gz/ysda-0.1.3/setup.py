# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['machine_learning',
 'machine_learning.ranking',
 'machine_learning.recommending',
 'machine_learning.recommending.models',
 'machine_learning.recommending.movielens',
 'machine_learning.recommending.tests',
 'machine_learning.transformers.Annotated_transformer',
 'machine_learning.transformers.ML2TransformerApp',
 'my_tools',
 'my_tools.tests']

package_data = \
{'': ['*'],
 'machine_learning': ['clustering/*',
                      'convolutional_neural_networks/*',
                      'deep_learning_tricks/*',
                      'em_algorithm/*',
                      'natural_language_processing/*',
                      'papers/*',
                      'sandbox/*',
                      'theory/*',
                      'transformers/Attention is all you need.pdf',
                      'transformers/Attention is all you need.pdf',
                      'transformers/Attention is all you need.pdf',
                      'transformers/Attention is all you need.pdf',
                      'transformers/Attention is all you need.pdf',
                      'transformers/BERT.pdf',
                      'transformers/BERT.pdf',
                      'transformers/BERT.pdf',
                      'transformers/BERT.pdf',
                      'transformers/BERT.pdf',
                      'transformers/LambdaNet.pdf',
                      'transformers/LambdaNet.pdf',
                      'transformers/LambdaNet.pdf',
                      'transformers/LambdaNet.pdf',
                      'transformers/LambdaNet.pdf',
                      'transformers/Sem_Transformers.ipynb',
                      'transformers/Sem_Transformers.ipynb',
                      'transformers/Sem_Transformers.ipynb',
                      'transformers/Sem_Transformers.ipynb',
                      'transformers/Sem_Transformers.ipynb',
                      'transformers/Visual_transformer.pdf',
                      'transformers/Visual_transformer.pdf',
                      'transformers/Visual_transformer.pdf',
                      'transformers/Visual_transformer.pdf',
                      'transformers/Visual_transformer.pdf'],
 'machine_learning.ranking': ['Papers/*'],
 'machine_learning.recommending': ['configs/*',
                                   'configs/sweeps/*',
                                   'notebooks/Untitled.ipynb',
                                   'notebooks/Untitled.ipynb',
                                   'notebooks/Untitled.ipynb',
                                   'notebooks/Untitled.ipynb',
                                   'notebooks/Untitled.ipynb',
                                   'notebooks/artifacts/ALS:v0/*',
                                   'notebooks/artifacts/slim:v2/*',
                                   'notebooks/artifacts/tmp:v1/*',
                                   'notebooks/lab_recommending.ipynb',
                                   'notebooks/lab_recommending.ipynb',
                                   'notebooks/lab_recommending.ipynb',
                                   'notebooks/lab_recommending.ipynb',
                                   'notebooks/lab_recommending.ipynb',
                                   'notebooks/sem_recommending.ipynb',
                                   'notebooks/sem_recommending.ipynb',
                                   'notebooks/sem_recommending.ipynb',
                                   'notebooks/sem_recommending.ipynb',
                                   'notebooks/sem_recommending.ipynb',
                                   'notebooks/tmp',
                                   'notebooks/tmp',
                                   'notebooks/tmp',
                                   'notebooks/tmp',
                                   'notebooks/tmp',
                                   'notebooks/tmp.txt',
                                   'notebooks/tmp.txt',
                                   'notebooks/tmp.txt',
                                   'notebooks/tmp.txt',
                                   'notebooks/tmp.txt',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Conjugate gradient for '
                                   'implicit feedback.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/(trash) Factorization machines.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/8951-Article '
                                   'Text-12479-1-2-20201228.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/AlphaBetaNDCG.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian personalized ranking.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Bayesian probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Factorization meets the '
                                   'neighborhood.pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/Implicit feedback model (ALS).pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/LightFM.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Probabilistic matrix '
                                   'factorization.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/Recommending systems overview.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf',
                                   'papers/SLIM.pdf'],
 'machine_learning.transformers.Annotated_transformer': ['images/*',
                                                         'writeup/*'],
 'machine_learning.transformers.ML2TransformerApp': ['resources/frontend/*',
                                                     'resources/latex.json']}

install_requires = \
['catboost>=1.1,<2.0',
 'einops>=0.4.1,<0.5.0',
 'gradio>=3.7,<4.0',
 'implicit>=0.6.1,<0.7.0',
 'matplotlib>=3.5.0,<3.6.0',
 'numba>=0.56.2,<0.57.0',
 'numpy>=1.22,<2.0',
 'pandas>=1.4.0,<2.0.0',
 'protobuf==3.19.4',
 'pytest>=7.1.3,<8.0.0',
 'pytorch-lightning>=1.6,<1.7',
 'scipy>=1.7,<2.0',
 'shap>=0.41.0,<0.42.0',
 'sklearn>=0.0,<0.1',
 'torch>=1.11.0,<1.13',
 'wandb>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'ysda',
    'version': '0.1.3',
    'description': '',
    'long_description': '# YSDA\nYandex School of Data Analysis materials \n',
    'author': 'DimaKoshman',
    'author_email': 'koshmandk@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
