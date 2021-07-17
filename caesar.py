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
