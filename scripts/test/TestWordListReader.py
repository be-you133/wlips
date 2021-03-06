# This Python file uses the following encoding: utf-8
import unittest

from scripts.src.WordListReader import WordListReader
from scripts.src.WordList import WordList
from scripts.test.TestCharacterSetUtils import CHARACTER_SET_DESCRIPTION_POLISH


class TestWordListReader(unittest.TestCase):

    SAMPLE_WORD_LIST = "sample_word_list"

    def test_correct_validate_file_exists(self):
        WordListReader().validate_file_exists(self.SAMPLE_WORD_LIST)

    def test_incorrect_validate_file_exists(self):
        NON_EXISTING_WORD_LIST = "non_existing_word_list"
        with self.assertRaises(SystemExit):
            WordListReader().validate_file_exists(NON_EXISTING_WORD_LIST)

    def test_get_file_hash_info(self):
        expected_file_hash_info = {"3b784e25": self.SAMPLE_WORD_LIST}
        file_hash_info = WordListReader().get_file_hash_info(self.SAMPLE_WORD_LIST)
        self.assertEqual(file_hash_info, expected_file_hash_info)

    def test_read_file(self):
        expected_lines = [
            "[english-qvx+ą:a+ć:c+ę:e+ł:l+ń:n+ó:o+ś:s+ź:z+ż:z]\n",
            "awokado\n",
            "banan\n",
            "tygrys\n"
        ]
        lines = WordListReader().read_file(self.SAMPLE_WORD_LIST)
        self.assertListEqual(expected_lines, lines)

    correct_scenarios_lines = [
        (["firstline\n"], []),
        (["firstline\n", "word1\n"], ["word1"]),
        (["firstline\n", "word1\n", "word2\n", "word3\n"], ["word1", "word2", "word3"])
    ]
    def test_correct_parse_word_list(self):
        for lines, expected_word_list in self.correct_scenarios_lines:
            with self.subTest():
                word_list = WordListReader().parse_word_list(lines)
                self.assertListEqual(expected_word_list, word_list)

    incorrect_scenarios_lines = [
        ["firstline"],
        ["firstline\n", "word1"],
        ["firstline", "\n", "word2\n"],
        ["firstline\n", "word1\n", "word2\n", "\n"]
    ]
    def test_incorrect_parse_word_list(self):
        for lines in self.incorrect_scenarios_lines:
            with self.subTest():
                self.assertRaises(Exception,
                                  WordListReader().parse_word_list,
                                  lines)

    def test_parse_file(self):
        EXPECTED_WORD_LIST = WordList(CHARACTER_SET_DESCRIPTION_POLISH,
                                      ["awokado", "banan", "tygrys"],
                                      {"3b784e25": self.SAMPLE_WORD_LIST})
        word_list = WordListReader().parse_file(self.SAMPLE_WORD_LIST)
        self.assertEqual(EXPECTED_WORD_LIST, word_list)

if __name__ == '__main__':
    unittest.main()
