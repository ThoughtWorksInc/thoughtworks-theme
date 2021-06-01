import inspect
import unittest
from convert import convert


class TestConvert(unittest.TestCase):

    def test_returns_empty_string_with_nothing(self):
        self.assertEqual(convert(), "")

    def test_returns_consistently_without_any_color_in_content(self):
        self.assertEqual(convert("anything"), "anything")

    def test_convert_to_colours_in_palette(self):
        self.assertEqual(convert("#f0f0f0", "#ffffff"), "#ffffff")

    def test_convert_to_least_euclidean_distance_colour_in_palette_when_no_distance_type_specified(self):
        # sqrt(49) < sqrt(51) < sqrt(57)
        self.assertEqual(convert(
            "#000000",
            inspect.cleandoc(
                """
                #020306
                #040405
                #010107
                """
            )),
            "#020306")

    def test_convert_to_least_manhattan_distance_colour_in_palette_when_the_distance_type_specified(self):
        # 1+1+7=9 < 2+3+6=11 < 4+4+5=13
        self.assertEqual(convert(
            "#000000",
            inspect.cleandoc(
                """
                #020306
                #040405
                #010107
                """
            ), "manhattan"),
            "#010107")

    def test_convert_to_least_uniform_distance_colour_in_palette_when_the_distance_type_specified(self):
        # 5 < 6 < 7
        self.assertEqual(convert(
            "#000000",
            inspect.cleandoc(
                """
                #020306
                #040405
                #010107
                """
            ), "uniform"),
            "#040405")

    def test_convert_all_the_colour_like_text_in_the_content(self):
        self.assertEqual(convert(
            inspect.cleandoc(
                """
                <colour>#123456</colour>
                <anotherColour>#654321</anotherColour>
                """
            ),
            inspect.cleandoc(
                """
                #ff0000
                #00ff00
                #0000ff
                """
            )),
            inspect.cleandoc(
                """
                <colour>#0000ff</colour>
                <anotherColour>#ff0000</anotherColour>
                """
            ))

    def test_convert_case_insensitively(self):
        self.assertEqual(convert("#ABCDEF", "#000000"), "#000000")


if __name__ == '__main__':
    unittest.main()
