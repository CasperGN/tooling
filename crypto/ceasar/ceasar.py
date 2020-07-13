class Ceasar:

    def __init__(self):
        self._alphabet = ['a', 'b', 'c', 'd', 'e',
                          'f', 'g', 'h', 'i', 'j',
                          'k', 'l', 'm', 'n', 'o',
                          'p', 'q', 'r', 's', 't',
                          'u', 'v', 'w', 'x', 'y',
                          'z']
        while True:
            # Semi Switch statement
            try:
                option = int(input("Press 1 for encryption\nPress 2 for decryption\nPress 3 for bruteforcing\nPress 4 to exit.\nOption: "))
                if option == 1:
                    self.encrypt()
                elif option == 2:
                    self.decrypt()
                elif option == 3:
                    self.bruteforce()
                elif option == 4:
                    exit(0)
            except ValueError:
                print("Non-valid input. Terminating..")
                exit(1)
            except KeyboardInterrupt:
                print("\nExiting..")
                exit(0)

    def encrypt(self):
        try:
            offset = int(input("Please enter offset: "))
            # Theres no point in going beyond, 26 is just the same character
            if offset >= 25:
                raise ValueError
            text = str(input("Input text: "))
            print("Calculating Ceasar of '{0}' with offset of '{1}'".format(text, offset))

            encrypted_text = ""

            for char in text:
                if char == " ":
                    encrypted_text += " "
                else:
                    # Need to ensure the reset the index of the list, if we go beyond the last entry
                    if (self._alphabet.index(char.lower()) + offset) > 25:
                        new_offset = (self._alphabet.index(char.lower()) + offset) - 26
                        encrypted_text += str(self._alphabet[new_offset])
                    else:
                        encrypted_text += str(self._alphabet[self._alphabet.index(char.lower()) + offset])
            print(encrypted_text)
            print("\n")
        except ValueError:
            print("Incorrect input. Try again.")
            self.encrypt()

    def decrypt(self):
        try:
            offset = int(input("Please enter offset: "))
            if offset >= 26:
                raise ValueError
            text = str(input("Please enter ciphertext: "))

            decrypted_text = ""

            for char in text:
                if char == " ":
                    decrypted_text += " "
                else:
                    decrypted_text += str(self._alphabet[self._alphabet.index(char.lower()) - offset])

            print(decrypted_text)
            print("\n")
        except ValueError:
            print("Incorrect input. Try again.")
            self.decrypt()

    def bruteforce(self):
        try:
            text = str(input("Please enter ciphertext: "))
        except ValueError:
            print("Incorrect input. Try again.")
            self.bruteforce()

        decrypted_array = []
        decrypted_text = ""

        for num in range(0, 26):
            for char in text:
                if char == " ":
                    decrypted_text += " "
                else:
                    decrypted_text += str(self._alphabet[self._alphabet.index(char.lower()) - num])
            decrypted_array.append(decrypted_text)
            decrypted_text = ""

        print("Result from bruteforce: ")
        for val in decrypted_array:
            print("{0}:\t{1}".format(decrypted_array.index(val), val))
        print("\n")


ceasar = Ceasar()