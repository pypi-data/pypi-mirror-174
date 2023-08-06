from alphabet import Alphabet
from typing import TypedDict
from typing import Dict

Rule = TypedDict("Rule", { "of": str, "to": str })

class RulesDictionary():
    def __init__(self, alphabet: Alphabet):
        self.__alphabet = alphabet
        self.__dictionary: Dict[str, str] = dict()

        self.__initialize__dictionary()

    def __initialize__dictionary(self):
        for symbol in self.__alphabet.symbols:
            self.__dictionary[symbol] = symbol

    def register(self, rule: Rule):
        if not self.__alphabet.has(rule["of"]):
            raise Exception("The symbol {} is not in the alphabet".format(rule["of"]))
        
        if False in map(lambda symbol: self.__alphabet.has(symbol), rule["to"]):
            raise Exception("There is a symbol that does not belong to the alphabet in {}".format(rule["to"]))


        self.__dictionary[rule["of"]] = rule["to"]

        return self

    @property
    def dictionary(self):
        return self.__dictionary

    @property
    def alphabet(self):
        return self.__alphabet.symbols

if __name__ == "__main__":
    alphabet = Alphabet({ "A", "B", "C" })

    rules_dictionary = RulesDictionary(alphabet)

    rules_dictionary.register({
        "of": "A",
        "to": "C"
    })

    print(rules_dictionary.dictionary)
    
    rules_dictionary.register({
        "of": "F",
        "to": "C"
    })

