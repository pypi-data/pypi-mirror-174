class Alphabet():
    def __init__(self, symbols: set[str]) -> None:
        if not Alphabet.valid_symbols(symbols):
            raise Exception("The symbols are not well formatted")

        self.__symbols = symbols

    def __repr__(self):
        return f"Symbols={ self.__symbols }"

    @staticmethod
    def valid_symbols(symbols: set[str]):
        return False not in map(lambda symbol: len(symbol) == 1, symbols)

    @property
    def symbols(self):
        return self.__symbols
        
    def has(self, symbol: str):
        return symbol in self.__symbols



if __name__ == "__main__":
    alphabet = Alphabet({ "A", "B", "c" })

    print(alphabet.has("J"))
    print(alphabet.has("A"))
    print(alphabet.symbols)
    print(alphabet)

