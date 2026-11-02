import string

BINARY = "01"

DIGITS_1_4 = "1234"

FULL = string.ascii_letters + string.digits + "+*-_!@#$%&()=?"

CASES = {
    "3 caractères, chacun 0 ou 1":      (BINARY, 3),
    "4 caractères, chacun de 1 à 4":    (DIGITS_1_4, 4),
    "caractères a-z A-Z 0-9 + * ...":   (FULL, None),
}