__author__ = 'Zhifei Chen'

import os
subject_dir = os.path.join('C:', 'Users', 'JOJO', 'Desktop', 'Pysmell', 'pysmell', 'subjects')

directory = {
    'django': '1.8.2',
    'numpy': 'v1.9.2',
    'ipython': 'rel-3.1.0',
    'boto': '2.38.0',
    'tornado': 'v4.2.0',
    'matplotlib': 'v1.4.3',
    'scipy': 'v0.16.0b2',
    'nltk': '3.0.2',
    'ansible': 'v1.9.2-0.1.rc1'
}

# Aggiungi il percorso dei progetti ai nomi dei progetti
directory = {name: os.path.join(subject_dir, name) for name in directory.keys()}
