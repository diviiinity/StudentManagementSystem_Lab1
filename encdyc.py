class TextSecurity:
    """This class with encrypt the test using Caesar cipher"""
    def __init__(self, shift):
        """COnstructor."""
        self.shifter=shift
        self.s=self.shifter%26
  
    def _convert(self, text, s):
        result = ""

        for ch in text:
            if ch.isupper():
                result += chr((ord(ch) + s - 65) % 26 + 65)
            elif ch.islower():
                result += chr((ord(ch) + s - 97) % 26 + 97)
            else:
            # Leave numbers and symbols unchanged
                result += ch
        return result
  
    def encrypt(self, text):
        """return encrypted string."""
        return self._convert(text,self.shifter)
        
    def decrypt(self, text):
        """return encrypted string."""
        return self._convert(text,26-self.s) 

if __name__ == '__main__':
    cipher = TextSecurity(4)
    message = "WElcome"
    coded = cipher.encrypt(message)
    print('Secret: ', coded)
    answer = cipher.decrypt(coded)
    print('Message:', answer)