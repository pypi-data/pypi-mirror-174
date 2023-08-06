import unittest
from translit_me.transliterator import transliterate as tr
from translit_me.lang_tables import *


class TestTransliterate(unittest.TestCase):
    def test_hebrew_arabic(self):
        names = ['נועַם', "מאנץ'", "בישינה", "דימונה"]
        expected = ['نوعَم', 'مانض', 'بيشينة', 'بيسينة', 'ديمونة', 'ضيمونة']
        res = tr(names, HE_AR)
        print(res)
        self.assertListEqual(res, expected)

    def test_hebrew_english(self):
        names = ['נועַם', "מאנץ'", "בישינה"]  # ["מסטראי'",'משתראן']
        # ['כסבין', 'קלש', 'ארמילו', 'אבירו', 'בישינה', 'קדמות', 'לודקיא', 'גרדיגי', 'מיטילין', 'יובשטריסה']

        expected = ['nuʿam', 'noʿam', 'manḍ', 'manch', 'mānḍ', 'mānch', 'menḍ', 'mench', 'bīṣīna', 'bīṣīne', 'bīshīna',
                    'bīshīne', 'vīṣīna', 'vīṣīne', 'vīshīna', 'vīshīne']
        res = tr(names, HE_EN)
        print(res)
        self.assertListEqual(res, expected)

    def test_multi_word(self):
        names = ['כפר סבא', 'כפר סבא רבא', 'בן פורד יוסף']
        expected = ['كفر سبا', 'كفر سبا ربا', 'بن فورد يوسف', 'بن فورض يوسف']
        res = tr(names, HE_AR)
        print(res)
        self.assertListEqual(res, expected)


if __name__ == '__main__':
    unittest.main()
