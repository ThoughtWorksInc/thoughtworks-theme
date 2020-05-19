import unittest
from unittest import mock
from convert import convert, find_nearest_colour


class TestConvert(unittest.TestCase):

    def test_returns_empty_string_with_nothing(self):
        self.assertEqual(convert(), "")

    def test_returns_consistently_without_any_color_in_content(self):
        self.assertEqual(convert("anything"), "anything")

    def test_convert_to_colours_in_palette(self):
        self.assertEqual(convert("#f0f0f0", ['#ffffff']), "#ffffff")

    def test_convert_to_least_euclidean_distance_colour_in_palette(self):
        self.assertEqual(convert("#123456", ["#ff0000", "#00ff00", "#0000ff"]), "#0000ff")

    def test_convert_all_the_colour_like_text_in_the_content(self):
        self.assertEqual(convert("""
            <colour>#123456</colour>
            <anotherColour>#654321</anotherColour>
        """, ["#ff0000", "#00ff00", "#0000ff"]), """
            <colour>#0000ff</colour>
            <anotherColour>#ff0000</anotherColour>
        """)

    def test_convert_case_insensitively(self):
        self.assertEqual(convert("#ABCDEF", ["#000000"]), "#000000")

    @mock.patch('convert.find_nearest_colour', wraps=find_nearest_colour)
    def test_should_merge_duplicated_colour_in_content(self, spied_find_nearest_colour):
        convert("#ABCDEF,#ABCDEF", ["#000000"])
        self.assertEqual(spied_find_nearest_colour.call_count, 1)


if __name__ == '__main__':
    unittest.main()
