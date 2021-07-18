import string

class Caesar:
    special_chars = [' ', '!', ',', '.', '?', "'"]
    def __init__(self, offset: str):
        """
        Accepts string for character mapping in the form of 'a=b'

        Parameters:
        -----------
        offset: str
            character mapping for offset
            must be a single string with 3 characters:
                input, '=', and output
        """
        self.offset: str = offset
        self.int_offset = None

    def new_offset(self, offset: str):
        self.offset = offset
        self.int_offset = None

    def _calc_offset_int(self): # currently lazy offset calculation
        plaintext, _, ciphertext = self.offset.partition('=')
        plaintext.lower()
        ciphertext.lower()
        int_plaintext: int = None
        int_ciphertext: int = None
        try:    # not doing range checking on the characters for now
            int_plaintext = ord(plaintext)
            int_ciphertext = ord(ciphertext)
        except TypeError:
            print('Expected offset string to be <char>=<char>, got at least one string')
            raise
        self.int_offset = abs(int_plaintext-int_ciphertext)

    def process(self, in_text: str, decipher: bool = False) -> str:
        """
        This method will process a text string. By default it will encipher with the object's offset, but it also handles decipher.

        Parameters:
        -----------
        in_text: str
            the input text to be processed by the caesar cipher

        decipher: bool = False
            optional configuration to decipher an input ciphertext

        Returns:
        --------
        out_text: str
            resulting string from processing, will be either ciphertext or plaintext
        """
        if not self.int_offset:
            self._calc_offset_int()
        out_text: str = ""
        for character in in_text:
            if character in self.special_chars:
                # TODO: actually encipher this
                out_text = out_text + character
            else:
                if character.isupper():
                    base = ord('A')
                else:
                    base = ord('a')
                normalized_ascii_plain = ord(character) - base
                offset = self.int_offset if not decipher else 0-self.int_offset
                normalized_acii_cipher = (normalized_ascii_plain + offset) % 26
                actual_acii_cipher = normalized_acii_cipher + base
                out_text = out_text + chr(actual_acii_cipher)

        return out_text


class CaesarBreaker:
    common_words_list = [
        "hello", "every", "word", "in", "the", "english", "language",
    ]
    dummy_frequency_dict = {
        "e": .12,
        "t": .091,
        "a": .081,
        "o": .077,
        "i": .073,
        "n": .069,
        "s": .063,
        "r": .06,
        "h": .059,
        "d": .043,
        "l": .04,
        "u": .029,
        "c": .027,
        "m": .026,
        "f": .023,
        "y": .021,
        "w": .021,
        "g": .02,
        "p": .018,
        "b": .015,
        "v": .011,
        "k": .007,
        "x": .002,
        "q": .001,
        "j": .001,
        "z": .001,
    }

    def __init__(self, alphabet: str = None, common_words: list = None, frequency_dict: dict = None):
        self._alphabet = alphabet if alphabet else string.ascii_lowercase
        self._common_words = common_words if common_words else self.common_words_list
        self._lang_frequencies = frequency_dict if frequency_dict else self.dummy_frequency_dict

    def _initialize_dict(self) -> dict:
        prepared_dict = {}
        for char in self._alphabet:
            prepared_dict.update({char: 0})
        return prepared_dict

    def _brute_force(self, ciphertext: str) -> dict:
        # naive brute force algorithm with common word boost
        key_message_dict: dict = {}
        cipher = Caesar('a=a')
        for character in self._alphabet:
            key = f"a={character}"
            cipher.new_offset(offset=key)
            message = cipher.process(in_text=ciphertext, decipher=True)
            for word in self._common_words:
                if word in message:
                    key_message_dict.update({key: message})
        return key_message_dict

    def _frequency_analysis(self, ciphertext: str) -> dict:
        key_message_dict = {}
        cipher_length = len(ciphertext)
        frequency_dict = self._initialize_dict()
        cipher = Caesar('a=a')
        for char in ciphertext:
            if char in self._alphabet:
                old_value = frequency_dict.get(char)
                new_value = old_value + 1/cipher_length
                frequency_dict.update({char: new_value})
        # next we want to compare frequencies and assign possible ciphers  based on that
        # for example, check if frequency_dict
        return key_message_dict

    def break_it(self, ciphertext: str, brute_force: bool = False) -> tuple:
        # frequency analysis
        if brute_force:
            result_dict = self._brute_force(ciphertext=ciphertext)
        else:
            result_dict = self._frequency_analysis(ciphertext=ciphertext)

        print(result_dict)
