class Caesar:
    def __init__(self, offset: str):
        self.offset: str = offset
        self.int_offset = None

    def _calc_offset_int(self):
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

    def encipher(self, plaintext: str) -> str:
        if not self.int_offset:
            self._calc_offset_int()
        ciphertext: str = ""
        for character in plaintext: # not currently handling special characters at all
            if character.isupper():
                base = ord('A')
            else:
                base = ord('a')
            normalized_ascii_plain = ord(character) - base
            normalized_acii_cipher = (normalized_ascii_plain + self.int_offset) % 26
            actual_acii_cipher = normalized_acii_cipher + base
            ciphertext = ciphertext + chr(actual_acii_cipher)

        return ciphertext
