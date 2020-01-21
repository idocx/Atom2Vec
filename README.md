# PyAtom2Vec
A python implement of Atom2Vec: a simple way to describe atoms for machine learning

## Background
Atom2Vec is first proposed on [Zhou Q, Tang P, Liu S, et al. Learning atoms for materials discovery[J]. Proceedings of the National Academy of Sciences, 2018, 115(28): E6411-E6417.](https://www.pnas.org/content/115/28/E6411#page)

It is a powerful but simple method to transfer atoms into vectors, quite similar to Word2Vec in NLP.

## Requirements
To run this program, you will need ```Scipy``` and ```Numpy``` packages. If you want to generate your own dataset, you may also need ```Requests``` package for web requests.

* Anaconda environment is highly recommended.

If you have installed ```pip```, you may use these commands to install these packages.
```shell
# on Linux
pip3 install scipy numpy requests
# on Windows
pip install scipy numpy requests
```

## How To Use
```python3
from Atom2Vec import Atom2Vec

# data_file: path to the dataset file
# vec_length: length of atom vector you want
atoms_vec = Atom2Vec(data_file, vec_length)
atoms_vec.saveAll()
```
Output:
```
Generating index 77402/77402 -- Complete!
Building matrix  -- Complete!
SVD -- Complete!
```

Also, this package contains a dataset, which was obtained from [Material Project](https://materialsproject.org/) using  ```GetMP.py```. The raw response is stored in ```string_2.json``` and ```string_3.json```. Then the response is further processed by ```Preprocess.py```, whose result is saved to ```string.json``` for further use.

## Output File
The output is kept in ```atoms_vec.txt``` and ```atoms_index.txt```.

* ```atoms_vec.txt``` contains a M * N matrix. M is the index of the atoms. N is the length of atom vector. Each row represents a vector describing certain atom.

* ```atoms_index.txt``` contains a M * 1 matrix. Each row contains a integer, which is the atomic number of certain atom. It tells which atom each row represents in ```atoms_vec.txt```. 

## Test Program
```Atom2Vec.py``` also contains a simple test, which can be run by
```shell
# Linux
python3 Atom2Vec
# Windows
python Atom2Vec
```
If the program can run normally, it will exit with no errors raised.

## Interactive Similarity Map
We can calculate cosine distance to quantify similarity between every atom.

You can find a interactive similarity map on [https://www.yuxingfei.com/src/similarity.html](https://www.yuxingfei.com/src/similarity.html)
