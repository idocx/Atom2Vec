from MatParser import MatEntity
from json import load, dump
import numpy as np


class EnvsMat:
    """
    the env matrix built directly from the mat string
    """
    def __init__(self, filename):
        self.atoms = set()
        self.envs = []  # storing envs instances
        self.atoms_length = 0
        self.envs_length = 0  # number of envs
        self.envs_mat = self.generateMatrix(filename)
        # self.normalizeMatrix()
        
    def generateMatrix(self, filename):
        """
        This routine is divided into two parts:
        PART 1: building a hash table in order to search and compare in a fast way
        PART 2: using the hash table, generate a envs matrix
        RETURN: the matrix it generates
        """
        # PART 1: build hash table and find all the envs
        cnt = 0
        names = self.loadJson(filename)
        envs_hash = []
        print("Generating index -- {}/{}".format(cnt, len(names)), end="")
        for each_entity in names:
            mat = MatEntity(input_dict=each_entity)
            for each_atom in mat.elements:
                env = mat.get_env(each_atom)
                self.atoms.add(env["atom"][0])
                self.envs.append(env)
                # use hash value as the env's unique identifier (much faster)
                env_hash = hash(env)
                if envs_hash:
                    # find the target index
                    env_pos = bSearch(envs_hash, env_hash)
                    # if the env is not in the envs array,
                    # add the env to the array
                    if env_pos < 0:
                        env_pos = -env_pos
                else:
                    # for the condition that the envs array
                    # has no elements (first element for example)
                    env_pos = 0
                envs_hash.insert(env_pos, env_hash)
            cnt += 1
            if cnt % 10000 == 0:
                print("\rGenerating index {}/{}".format(cnt, len(names)), end="")
        print("\rGenerating index {}/{} -- Complete!".format(cnt, len(names)))
        
        self.atoms = list(self.atoms)
        self.atoms.sort()
        self.atoms = tuple(self.atoms)
        self.atoms_length = len(self.atoms)
        self.envs_length = len(envs_hash)  # update the length
        
        # PART 2: building envs matrix
        print("Building matrix  --", end="")
        envs_mat = np.zeros((self.atoms_length, self.envs_length), dtype=np.float32)
        for env in self.envs:
            env_pos = bSearch(envs_hash, hash(env))
            atom = env["atom"][0]
            envs_mat[bSearch(self.atoms, atom)][env_pos] = 1.0
        print(" Complete!")
        
        return envs_mat
    
    def normalizeMatrix(self):
        print("Normalizing matrix  --", end="")
        norm_coof = np.sum(np.square(self.envs_mat), axis=1)
        self.envs_mat = (self.envs_mat.T / norm_coof).T
        print(" Complete!")
            
    @staticmethod
    def loadJson(filename):
        """
        load json that contains material string from file
        """
        with open(filename, "r") as f:
            names = load(f)["names"]
        return names


def bSearch(arr, target, start=0, end=-1):
    """
    -- BINARY SEARCH --
    if target is not in arr, the opposite number of the
    first number's index larger than target will return
    """
    if not arr:
        return None
    if end == -1:
        end = len(arr) - 1
    if end < start:
        raise Exception("start({}) should be smaller or equal than end({})".format(start, end))
    
    low = start
    high = end

    while low <= high:
        mid = int((high + low) / 2)
        if target == arr[mid]:
            return mid 
        elif target > arr[mid]:
            low = mid + 1
        else:
            high = mid - 1

    return -(mid + ((arr[mid] < target) & 1))


if __name__ == "__main__":
    ii = EnvsMat("string.json")
