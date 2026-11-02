import random
import unittest

from partie2 import ciphers

class CaesarTests(unittest.TestCase):
    def test_invalid_key_is_rejected(self):
        for key in (0, 26, 51):
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    ciphers.validate_key(key)

    def test_prepare_and_restore_keep_format(self):
        text = "Bonjour, monde !"
        letters, mask = ciphers.caesar_prepare(text)
        encrypted = ciphers.caesar(letters, 3)
        restored = ciphers.caesar_restore(ciphers.caesar_decrypt(encrypted, 3), mask)
        self.assertEqual(restored, text)

    def test_roundtrip_both_directions(self):
        msg = "Hello, World! xyz"
        for n in range(0, 60):
            for d in ("right", "left"):
                enc = ciphers.caesar(msg, n, d)
                self.assertEqual(ciphers.caesar_decrypt(enc, n, d), msg)

    def test_known_value(self):
        self.assertEqual(ciphers.caesar("ABC xyz", 3, "right"), "DEF ABC")
        self.assertEqual(ciphers.caesar("DEF ABC", 3, "left"), "ABC xyz")

    def test_uppercase_flows_into_lowercase(self):
        self.assertEqual(ciphers.caesar("WXYZ", 4, "right"), "abcd")
        self.assertEqual(ciphers.caesar("wxyz", 4, "right"), "ABCD")

    def test_automatic_decryption_reads_code_and_direction(self):
        encrypted = ciphers.caesar("Hello", 3, "droite")
        channel_message = ciphers.build_channel_message("Caesar", "droite", encrypted)
        self.assertEqual(ciphers.dechiffrement_automatique(channel_message, 3), "Hello")

class HillTests(unittest.TestCase):
    def test_key_from_text_rejects_non_square_key(self):
        with self.assertRaises(ValueError):
            ciphers.key_from_text("ABCDE")

    def test_decrypt_rejects_incomplete_block(self):
        with self.assertRaises(ValueError):
            ciphers.hill_decrypt("ABC", [[3, 3], [2, 5]])

    def test_classic_example(self):
        key = ciphers.key_from_text("GYBNQKURP")
        self.assertEqual(ciphers.hill_encrypt("ACT", key), "POH")

    def test_roundtrip_2x2(self):
        key = [[3, 3], [2, 5]]
        enc = ciphers.hill_encrypt("HELP", key)
        self.assertEqual(enc, "HIAT")
        self.assertEqual(ciphers.hill_decrypt(enc, key), "HELP")

    def test_roundtrip_random_keys(self):
        rnd = random.Random(4)
        done = 0
        while done < 40:
            n = rnd.choice([2, 3])
            key = [[rnd.randrange(26) for _ in range(n)] for _ in range(n)]
            try:
                ciphers.mat_inverse_mod(key)
            except ValueError:
                continue
            msg = "".join(rnd.choice(ciphers.ALPHA) for _ in range(n * 5))
            self.assertEqual(ciphers.hill_decrypt(ciphers.hill_encrypt(msg, key), key), msg)
            done += 1

    def test_bad_key_rejected(self):
        with self.assertRaises(ValueError):
            ciphers.hill_encrypt("HELLO", [[2, 4], [1, 2]])

    def test_preserves_spaces(self):
        key = [[3, 3], [2, 5]]
        text = "HELLO WORLD"
        positions = ciphers.format_positions(text)
        encrypted = ciphers.hill_encrypt(text, key)
        padding = (-len(ciphers.clean(text))) % len(key)
        decrypted = ciphers.hill_decrypt(encrypted, key)
        if padding:
            decrypted = decrypted[:-padding]
        self.assertEqual(ciphers.restore_format(decrypted, positions), text)

    def test_format_positions(self):
        key = [[3, 3], [2, 5]]
        text = "HELLO WORLD!"
        positions = ciphers.format_positions(text)
        encrypted = ciphers.hill_encrypt(text, key)
        decrypted = ciphers.hill_decrypt(encrypted, key)
        padding = (-len(ciphers.clean(text))) % len(key)
        if padding:
            decrypted = decrypted[:-padding]
        self.assertEqual(ciphers.restore_format(decrypted, positions), text)

    def test_automatic_decryption_reads_hill_code(self):
        key = [[3, 3], [2, 5]]
        encrypted = ciphers.hill_encrypt("HELP", key)
        channel_message = ciphers.build_channel_message("Hill", "", encrypted)
        self.assertEqual(
            ciphers.dechiffrement_automatique(channel_message, "", hill_key=key),
            "HELP",
        )

class PlayfairTests(unittest.TestCase):
    def test_invalid_key_is_rejected(self):
        with self.assertRaises(ValueError):
            ciphers.playfair_encrypt("HELLO", "clé invalide")

    def test_playfair_square_contains_unique_letters_without_j(self):
        square = ciphers.playfair_square("monarchy")
        self.assertEqual(len(square), 25)
        self.assertEqual(len(set(square)), 25)
        self.assertNotIn("J", square)

    def test_roundtrip(self):
        enc = ciphers.playfair_encrypt("balloon", "monarchy")
        dec = ciphers.playfair_decrypt(enc, "monarchy")
        self.assertEqual(ciphers.playfair_strip_padding(dec), "BALLOON")

    def test_odd_length(self):
        enc = ciphers.playfair_encrypt("abc", "key")
        self.assertEqual(len(enc) % 2, 0)

    def test_preserves_spaces(self):
        text = "BALLOON AT NOON"
        positions = ciphers.format_positions(text)
        padding_positions = ciphers.playfair_prepare(text)[1]
        enc = ciphers.playfair_encrypt(text, "monarchy")
        dec = ciphers.playfair_strip_padding(
            ciphers.playfair_decrypt(enc, "monarchy"),
            padding_positions,
        )
        self.assertEqual(ciphers.restore_format(dec, positions), text)

    def test_preserves_real_final_x(self):
        text = "HELLOX"
        padding_positions = ciphers.playfair_prepare(text)[1]
        enc = ciphers.playfair_encrypt(text, "monarchy")
        dec = ciphers.playfair_decrypt(enc, "monarchy")
        self.assertEqual(
            ciphers.playfair_strip_padding(dec, padding_positions),
            text,
        )

    def test_preserves_real_j(self):
        text = "JIGSAW"
        j_positions = ciphers.playfair_j_positions(text)
        enc = ciphers.playfair_encrypt(text, "monarchy")
        dec = ciphers.playfair_decrypt(enc, "monarchy")
        dec = ciphers.playfair_strip_padding(
            dec,
            ciphers.playfair_prepare(text)[1],
        )
        self.assertEqual(
            ciphers.playfair_restore_j(dec, j_positions),
            text,
        )

    def test_automatic_decryption_reads_playfair_code(self):
        key = "monarchy"
        encrypted = ciphers.playfair_encrypt("HELP", key)
        channel_message = ciphers.build_channel_message("Playfair", "", encrypted)
        self.assertEqual(
            ciphers.dechiffrement_automatique(channel_message, key),
            "HELP",
        )

class ChannelTests(unittest.TestCase):
    def test_decode_channel_message_with_embedded_key(self):
        message = ciphers.build_channel_message("Playfair", "", "BMOD", "monarchy")
        self.assertEqual(
            ciphers.decode_channel_message(message),
            ("Playfair", "", "monarchy", "BMOD"),
        )

    def test_channel_rejects_invalid_algorithm_and_direction(self):
        with self.assertRaises(ValueError):
            ciphers.build_channel_message("Unknown", "", "ABC")
        with self.assertRaises(ValueError):
            ciphers.build_channel_message("Caesar", "up", "ABC")

    def test_channel_rejects_malformed_message(self):
        with self.assertRaises(ValueError):
            ciphers.decode_channel_message("000:r")
        with self.assertRaises(ValueError):
            ciphers.decode_channel_message("999:r:ABC")

if __name__ == "__main__":
    unittest.main()
