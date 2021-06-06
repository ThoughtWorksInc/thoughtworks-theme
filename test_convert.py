import inspect
import math
import unittest
from convert import convert, find_nearest_colour, Colour, ColourDistance, substitute


class TestConvert(unittest.TestCase):

    def test_returns_empty_string_with_nothing(self):
        self.assertEqual("", convert())

    def test_returns_consistently_without_any_color_in_content(self):
        self.assertEqual("anything", convert(theme="anything"))

    def test_convert_to_colours_in_palette(self):
        self.assertEqual("#FFFFFF", convert(theme="#f0f0f0", theme_colour_format="hex", palette="#FFFFFF"))

    def test_convert_to_least_euclidean_distance_colour_in_palette_when_no_distance_type_specified(self):
        # sqrt(49) < sqrt(51) < sqrt(57)
        palette = inspect.cleandoc("""
            #020306
            #040405
            #010107
            """)
        self.assertEqual("#020306", convert(theme="#000000", theme_colour_format="hex", palette=palette))

    def test_convert_to_least_manhattan_distance_colour_in_palette_when_the_distance_type_specified(self):
        # 1+1+7=9 < 2+3+6=11 < 4+4+5=13
        palette = inspect.cleandoc("""
            #020306
            #040405
            #010107
            """)
        self.assertEqual(
            "#010107",
            convert(theme="#000000", theme_colour_format="hex", palette=palette, distance_type="manhattan"))

    def test_convert_to_least_uniform_distance_colour_in_palette_when_the_distance_type_specified(self):
        # 5 < 6 < 7
        palette = inspect.cleandoc("""
            #020306
            #040405
            #010107
            """)
        self.assertEqual(
            "#040405",
            convert(theme="#000000", theme_colour_format="hex", palette=palette, distance_type="uniform"))

    def test_convert_all_hex_colour_like_text_in_the_content(self):
        converted_result = inspect.cleandoc("""
                <colour>#0000FF</colour>
                <anotherColour>#FF0000</anotherColour>
                """)
        theme = inspect.cleandoc("""
                <colour>#123456</colour>
                <anotherColour>#654321</anotherColour>
                """)
        palette = inspect.cleandoc("""
                #ff0000
                #00ff00
                #0000ff
                """)
        self.assertEqual(converted_result, convert(theme=theme, theme_colour_format="hex", palette=palette))

    def test_convert_all_rgba_decimal_colour_like_text_in_the_content(self):
        converted_result = inspect.cleandoc("""
                <colour>0 0 1 1</colour>
                <anotherColour>1 0 0 1</anotherColour>
                """)
        theme = inspect.cleandoc("""
                <colour>0.1 0.2 0.3 1</colour>
                <anotherColour>1 0.9 0.8 1</anotherColour>
                """)
        palette = inspect.cleandoc("""
                #ff0000
                #00ff00
                #0000ff
                """)
        self.assertEqual(converted_result, convert(theme=theme, theme_colour_format="rgba_decimal", palette=palette))

    def test_convert_case_insensitively(self):
        self.assertEqual("#000000", convert(theme="#ABCDEF", theme_colour_format="hex", palette="#000000"))


class TestFindNearestColour(unittest.TestCase):
    def test_find_nearest_colour_by_euclidean_distance_when_no_distance_type_is_specified(self):
        colours_to_find = [Colour("#000000", "hex"), Colour("#010101", "hex")]
        origin_colour = Colour("#010101", "hex")
        self.assertEqual(Colour("#010101", "hex"), find_nearest_colour(colours_to_find, origin_colour, ""))

    def test_find_nearest_colour_by_euclidean_distance(self):
        colours_to_find = [Colour("#ff0000", "hex"), Colour("#00ff00", "hex"), Colour("#0000ff", "hex")]
        origin_colour = Colour("#123456", "hex")
        self.assertEqual(Colour("#0000ff", "hex"), find_nearest_colour(colours_to_find, origin_colour, ""))


class TestColour(unittest.TestCase):
    def test_colour_keep_original_text_when_instantiating(self):
        self.assertEqual("#000000", Colour("#000000", "hex").original_text)

    def test_colour_evaluates_rgb_from_hex_when_instantiating(self):
        self.assertTupleEqual((0, 0, 0), Colour("#000000", "hex").rgb)

    def test_colour_evaluates_rgb_from_rgba_decimal_when_instantiating(self):
        self.assertTupleEqual((0, 0, 0), Colour("0 0 0 0", "rgba_decimal").rgb, )
        self.assertTupleEqual((51, 51, 51), Colour("0.2 0.2 0.2 0.2", "rgba_decimal").rgb)
        self.assertTupleEqual((255, 255, 255), Colour("1 1 1 1", "rgba_decimal").rgb)

    def test_colour_represents_as_rgb_tuple(self):
        colour = Colour("#000000", "hex")
        self.assertEqual("Colour(original_text=#000000, rgb=(0, 0, 0))", repr(colour))

    def test_colour_represents_twice(self):
        colour = Colour("#000000", "hex")
        self.assertEqual("Colour(original_text=#000000, rgb=(0, 0, 0))", repr(colour))
        self.assertEqual("Colour(original_text=#000000, rgb=(0, 0, 0))", repr(colour))

    def test_colour_equals_when_text_is_exactly_same(self):
        self.assertEqual(Colour("#000000", "hex"), Colour("#000000", "hex"))

    def test_colour_unequals_when_rgb_is_different(self):
        self.assertNotEqual(Colour("#000000", "hex"), Colour("#123456", "hex"))

    def test_colours_subtraction_results_in_a_colour_distance(self):
        self.assertEqual(ColourDistance(Colour("#010101", "hex"), Colour("#000000", "hex")),
                         Colour("#010101", "hex") - Colour("#000000", "hex"))

    def test_colour_outputs_to_text_by_format(self):
        colour = Colour("#333333", "hex")
        self.assertEqual("#333333", format(colour, "hex"))
        self.assertEqual("0.2 0.2 0.2", format(colour, "rgba_decimal"))


class TestColourDifference(unittest.TestCase):
    def test_colour_distance_calculates_rgb_respective_differences(self):
        self.assertTupleEqual(
            (1, 1, 1),
            ColourDistance(Colour("#010101", "hex"), Colour("#000000", "hex")).rgb_differences)

    def test_colour_distances_equal_when_they_have_same_differences(self):
        self.assertEqual(
            ColourDistance(Colour("#010101", "hex"), Colour("#000000", "hex")),
            ColourDistance(Colour("#020202", "hex"), Colour("#010101", "hex")))

    def test_colour_distance_calculates_euclidean_distance_when_distance_type_is_invalid(self):
        self.assertEqual(
            math.sqrt(3),
            ColourDistance(Colour("#010101", "hex"), Colour("#000000", "hex"))[None])

    def test_colour_distance_calculates_euclidean_distance_when_distance_type_is_specified(self):
        self.assertEqual(
            math.sqrt(3),
            ColourDistance(Colour("#010101", "hex"), Colour("#000000", "hex"))["euclidean"])

    def test_colour_distance_calculates_manhattan_distance_when_distance_type_is_specified(self):
        self.assertEqual(
            3,
            ColourDistance(Colour("#010101", "hex"), Colour("#000000", "hex"))["manhattan"])

    def test_colour_distance_calculates_uniform_distance_when_distance_type_is_specified(self):
        self.assertEqual(
            1,
            ColourDistance(Colour("#010101", "hex"), Colour("#000000", "hex"))["uniform"])


if __name__ == '__main__':
    unittest.main()
