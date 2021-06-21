import json
import os
import unittest
from io import StringIO
from itertools import product

from pymatgen.core import Element
from pymatgen.ext.matproj import MPRester

from atom2vec import AtomSimilarity


class TestAtomSimilarityQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.k_dim = 20
        cls.max_element = 3

        with MPRester(os.environ["MP_API_KEY"]) as mpr:
            criteria = {
                "nelements": 2,
                "e_above_hull": {"$lte": 0.}
            }
            properties = [
                "structure",
            ]
            entries = mpr.query(criteria=criteria, properties=properties, mp_decode=True)

        structures = [entry["structure"] for entry in entries]
        cls.atom_similarity = AtomSimilarity.from_structures(structures=structures,
                                                             k_dim=cls.k_dim,
                                                             max_elements=cls.max_element)

    def test_k_dim(self):
        self.assertEqual(self.k_dim, self.atom_similarity.k_dim)

    def test_same_atom_similarity(self):
        elements = self.atom_similarity._atoms_vector.keys()
        for element in elements:
            similarity = self.atom_similarity[element, element]
            self.assertAlmostEqual(1., similarity,
                                   msg="Similarity of same element is not 1.", delta=1e-5)

    def test_atom_similarity(self):
        elements = ("Fe", 27, Element("Ni"))

        query_tuples = product(elements, elements)
        for q in query_tuples:
            self.assertTrue(-1 - 1e-5 <= self.atom_similarity.__getitem__(q) <= 1. + 1e-5,
                            msg="Similarity of element {0}, {1} not in -1 ~ 1.".format(*q))

    def test_not_exist_atom_similarity(self):
        elements = (118, "Na")

        self.assertEqual(-1, self.atom_similarity.__getitem__(elements),
                         msg="Similarity for non-existing element should be -1.")

    def test_atom_vector(self):
        elements = ("Na", 12, Element("Al"))

        for element in elements:
            self.assertEqual(self.k_dim, len(self.atom_similarity.get_atom_vector(element)),
                             msg="Wrong size for queried vector")

    def test_not_exist_atom_vector(self):
        self.assertRaises(KeyError, self.atom_similarity.get_atom_vector, 118)

    def test_load_dump(self):
        # dump to json format
        atom_similarity_dict = self.atom_similarity.as_dict()
        atom_similarity_json = StringIO()
        json.dump(atom_similarity_dict, atom_similarity_json)

        atom_similarity_json.seek(0)

        # load json string to new AtomSimilarity object
        new_atom_similarity_dict = json.load(atom_similarity_json)
        new_atom_similarity = AtomSimilarity.from_dict(new_atom_similarity_dict)

        self.assertEqual(new_atom_similarity._atoms_vector, self.atom_similarity._atoms_vector,
                         msg="Unmatched atom vector after dumping and loading.")
        self.assertEqual(new_atom_similarity._atoms_similarity, self.atom_similarity._atoms_similarity,
                         msg="Unmatched atom similarity after dumping and loading.")

        self.assertEqual(new_atom_similarity.k_dim, self.atom_similarity.k_dim,
                         msg="Unmatched k_dim after dumping and loading.")
        self.assertEqual(new_atom_similarity.max_elements, self.atom_similarity.max_elements,
                         msg="Unmatched max_elements after dumping and loading.")
