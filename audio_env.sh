#!/bin/bash
module load python/3.6

virtualenv --no-download ~/audio_env
source ~/audio_env/bin/activate

pip install --no-index --upgrade pip
pip install numpy --no-index
pip install pandas --no-index
pip install librosa
pip install pydub 




