import inspect
import math
import unittest
from convert import convert, find_nearest_colour, Colour, ColourDistance


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


class TestFindNearestColour(unittest.TestCase):
    def test_find_nearest_colour_by_euclidean_distance_when_no_distance_type_is_specified(self):
        self.assertEqual(find_nearest_colour(
            [Colour("#000000"), Colour("#010101")], Colour("#010101"), ""),
            Colour("#010101"))

    def test_find_nearest_colour_by_euclidean_distance(self):
        self.assertEqual(find_nearest_colour(
            [Colour("#ff0000"), Colour("#00ff00"), Colour("#0000ff")], Colour("#123456"), ""),
            Colour("#0000ff"))


class TestColour(unittest.TestCase):
    def test_colour_evaluates_rgb_when_instantiating(self):
        self.assertTupleEqual(Colour("#000000").rgb, (0, 0, 0))

    def test_colour_represents_as_comma_delimited_text(self):
        self.assertEqual(repr(Colour("#000000")), "Colour(text=#000000,rgb=0,0,0)")

    def test_colour_represents_twice(self):
        colour = Colour("#000000")
        self.assertEqual(repr(colour), "Colour(text=#000000,rgb=0,0,0)")
        self.assertEqual(repr(colour), "Colour(text=#000000,rgb=0,0,0)")

    def test_colour_equals_when_text_is_exactly_same(self):
        self.assertEqual(Colour("#000000"), Colour("#000000"))

    def test_colour_unequals_when_rgb_is_different(self):
        self.assertNotEqual(Colour("#000000"), Colour("#123456"))

    def test_colours_subtraction_results_in_a_colour_distance(self):
        self.assertEqual(Colour("#010101") - Colour("#000000"), ColourDistance(Colour("#010101"), Colour("#000000")))


class TestColourDifference(unittest.TestCase):
    def test_colour_distance_calculates_rgb_respective_differences(self):
        self.assertTupleEqual(ColourDistance(Colour("#010101"), Colour("#000000")).rgb_differences, (1, 1, 1))

    def test_colour_distances_equal_when_they_have_same_differences(self):
        self.assertEqual(ColourDistance(Colour("#010101"), Colour("#000000")),
                         ColourDistance(Colour("#020202"), Colour("#010101")))

    def test_colour_distance_calculates_euclidean_distance_when_distance_type_is_invalid(self):
        self.assertEqual(ColourDistance(Colour("#010101"), Colour("#000000"))[None],
                         math.sqrt(3))

    def test_colour_distance_calculates_euclidean_distance_when_distance_type_is_specified(self):
        self.assertEqual(ColourDistance(Colour("#010101"), Colour("#000000"))["euclidean"],
                         math.sqrt(3))

    def test_colour_distance_calculates_manhattan_distance_when_distance_type_is_specified(self):
        self.assertEqual(ColourDistance(Colour("#010101"), Colour("#000000"))["manhattan"],
                         3)

    def test_colour_distance_calculates_uniform_distance_when_distance_type_is_specified(self):
        self.assertEqual(ColourDistance(Colour("#010101"), Colour("#000000"))["uniform"],
                         1)


if __name__ == '__main__':
    unittest.main()
