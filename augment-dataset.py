# augment-dataset.py
# https://augmentor.readthedocs.io/en/master/

import Augmentor
import os

src = os.getcwd()+"/datasett/" 

# dst-folder blir opprettet som 'output' i src-folder

p = Augmentor.Pipeline(src)

#p.skew(probability=0.7, magnitude=1.0)
#p.rotate(probability=1, max_left_rotation=5, max_right_rotation=5)
p.flip_left_right(probability=1)
p.sample(1000) # filer i folder
