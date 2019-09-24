#!/usr/bin/env bash

source env_lcg.sh

pip install --user entrypoints==0.3.0
pip install --upgrade --user cloudpickle
pip install --user coffea
pip install --user tqdm
pip install --user pycairo

# progressbar, sliders, etc.
jupyter nbextension enable --py widgetsnbextension

