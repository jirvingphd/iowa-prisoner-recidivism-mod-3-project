conda create --name fair-env python=3.12 jupyter notebook pandas scikit-learn matplotlib seaborn  conda-forge::lightgbm -y
conda activate fair-env
python -m ipykernel install --user --name=fair-env
pip install igraph
pip install torch torchvision torchaudio
pip install tensorflow-macos tensorflow-metal
pip install 'aif360[Reductions]'
pip install 'aif360[OptimalTransport]'
pip install 'aif360[inFairness]'
pip install 'aif360[FairAdapt]'
pip install 'aif360[AdversarialDebiasing]'
pip install pycairo

# echo "Environment created and activated"

