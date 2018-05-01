import unittest
import json


class JsonTestCase(unittest.TestCase):
    def test_parse(self):
        testjson = """{
        "conts" : 
            {
                "cont_key": "cont_value",
                "cont_list_key": [{"one": "1"}, {"2": "two"}, 3]
            }
        }
        """

        nodes = json.loads(testjson)
        conts = nodes["conts"]
        cont_list = conts["cont_list_key"]
        listitem2 = cont_list[1]
        dictitem2 = listitem2["2"]
        self.assertEqual(dictitem2, "two")

    def test_dump_primitives(self):
        original = {"conts": {"cont_key": "cont_value", "cont_list_key": [{"one": "1"}, {"2": "two"}, 2]}}
        jsontext = json.dumps(original)
        copy = json.loads(jsontext)
        self.assertEqual(original, copy)

        def get_the_number(nds):
            return nds["conts"]["cont_list_key"][-1]

        original_nr = get_the_number(original)
        copy_nr = get_the_number(copy)
        self.assertEqual(original_nr, copy_nr)

        self.assertIsInstance(copy_nr, int)

    def test_dump_class(self):
        class Animal:
            def __init__(self, name=None):
                self.name = name

            def __eq__(self, other):
                return self.serializeable() == other.serializeable()

            def serializeable(self):
                return {"name": self.name}

            @staticmethod
            def from_serialization(serializable):
                obj = Animal()
                obj.name = serializable["name"]
                return obj

        dog = Animal("Bodri")
        jsontext = json.dumps(dog.serializeable())
        copy = Animal.from_serialization(json.loads(jsontext))

        self.assertEqual(dog, copy)
