import re
from periodic_table import ELEMENTS, LOW_CHARS, CAP_CHARS, lookupEle


class NoSuchElementError(Exception):
    """
    if the string is not actually an element, error will be raised
    """
    def __init__(self, ele_str, mat_str):
        super().__init__("No element named {} ({}).".format(ele_str, mat_str))
        

class ElementNotFoundError(Exception):
    """
    if the material dosen't contain the given element, error will be raised
    """
    def __init__(self, ele_index, mat_str):
        super().__init__("[{}] is not in {}.".format(ELEMENTS[ele_index], mat_str))


class MatEntity:
    """
    Class for parse material string
    : string :: raw string of the material
    : elements :: dict { "<(int) element's index>": <(float) its stoichiometry number in the string>, ...}
    """
    def __init__(self, input_string="", input_dict={}, index=-1):
        input_dict = {int(k): v for k, v in input_dict.items()}
        self._string = input_string
        self._elements = self.parseString(self._string) or input_dict
        self.normalize()
        self._index = index
        self._length = len(self._elements)

    @staticmethod
    def parseString(input_string):
        """
        Parse the material string into a dictionary
        """
        elements = {}
        while input_string:
            result = re.match(r"[{}][{}]?".format(CAP_CHARS, LOW_CHARS), input_string)
            
            # for fear that the parser cannot recognize the material string
            try:
                ele_str = result.group(0)
                pos_ele = result.span()[1]
            except AttributeError:
                return {}

            if pos_ele < len(input_string) and input_string[pos_ele].isdigit():
                result = re.match(r"\d+\.?\d*", input_string[pos_ele:])
                pos_num = result.span()[1]
                number = float(result.group(0))
            else:
                pos_num = 0
                number = 1.0
                
            try:
                ele_index = lookupEle(ele_str)
            except KeyError:
                raise NoSuchElementError(ele_str)
            # one element could appear multiple times in one material string
            if ele_index not in elements:  
                elements[ele_index] = 0.0
                
            elements[ele_index] += number
            input_string = input_string[(pos_num+pos_ele):]
        
        return elements
    
    def normalize(self):
        """
        normalize all the stoichiometry numbers
        """
        norm_coff = sum(self._elements.values())
        for each in self._elements:
            self._elements[each] /= norm_coff
    
    def get_env(self, ele_index):
        """
        Get the environment of given element
        : return :: MatEnv
        """
        env = {"atom": [], "environment": self._elements.copy()}
        
        try:
            env["atom"] = [ele_index, env["environment"].pop(ele_index)]
        except KeyError:
            raise ElementNotFoundError(ele_index, self._string)
        
        return MatEnv(env)
    
    def set_index(self, new_index):
        self._index = new_index
        
    @property
    def index(self):
        return self._index

    @property
    def elements(self):
        return list(self._elements)
    
    @property
    def elements_dict(self):
        return self._elements
            
    def __str__(self):
        return self._string
    
    def __repr__(self):
        return str(self._elements)

    def __len__(self):
        return self._length
    
    
class MatEnv:
    """
    Class for storing env matrix
    : env_dict :: {"atom": [name, number], "environment": {...}}
    """
    def __init__(self, env_dict):
        self.env_dict = env_dict
        self._hash = self.get_hash(self.env_dict)
    
    def set_index(self, new_index):
        self._index = new_index
       
    @staticmethod
    def get_hash(env_dict):
        tmp_dict = env_dict["environment"].copy()
        tmp_dict[-1] = env_dict["atom"][1]
        return hash(frozenset(tmp_dict.items()))
    
    def __getitem__(self, key):
        return self.env_dict[key]
    
    def __setitem__(self, key, value):
        self.env_dict[key] = value

    def __hash__(self):
        return self._hash
    
    def __eq__(self, other):
        return self._hash == other._hash
    
    def __str__(self):
        return str(self.env_dict)
    
    __repr__ = __str__
    
    
if __name__ == "__main__":
    from json import load, dump
    
    with open("string.json") as f:
        strings = load(f)["names"]
    
    new_string = []
    for each_string in strings:
        a = MatEntity(each_string)
        if a.elements:
            new_string.append(a.__str__())
    
    with open("string_2.json", "w") as f:
        dump({"names": new_string}, f)
    # # a simple test
    # mat = MatEntity("Sr1.97MgSi0.6O5")
    # print(repr(mat))
    # print(mat.get_env(37))
    # print(hash(mat.get_env(37)))
    