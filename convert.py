import math
import re
import sys


class ColourFormat:
    def __init__(self, pattern, parse, stringify):
        self.pattern = pattern
        self.parse = parse
        self.stringify = stringify


class Colour:
    formats = {
        "hex": ColourFormat(
            r'#[0-9a-f]{6}',
            lambda text: tuple(map(lambda value_text: int(value_text, base=16), (text[i:i + 2]
                                                                                 for i in range(1, 7, 2)))),
            lambda rgb: ("#" + "{:02X}" * 3).format(*rgb)
        ),
        "rgba_decimal": ColourFormat(
            ' '.join([r'\d(?:\.\d+)?'] * 3),
            lambda text: tuple(map(lambda value: float(value) * 255, text.split(' ')[0:3])),
            lambda rgb: ' '.join(["{:g}"] * 3).format(*(value / 255 for value in rgb))
        ),
    }

    def __init__(self, colour_text, colour_format):
        self.original_text = colour_text
        self.rgb = self.formats.get(colour_format, self.formats["hex"]).parse(colour_text)

    def __eq__(self, other):
        return all(value == another_value
                   for (value, another_value) in zip(self.rgb, other.rgb))

    def __repr__(self):
        return "Colour(original_text={}, rgb={})".format(self.original_text, self.rgb)

    def __sub__(self, other):
        return ColourDistance(self, other)

    def __format__(self, colour_format):
        return self.formats[colour_format].stringify(self.rgb)


class ColourDistance:
    types = {
        "euclidean": lambda differences: math.sqrt(sum(tuple(math.pow(difference, 2) for difference in differences))),
        "manhattan": lambda differences: sum(tuple(abs(difference) for difference in differences)),
        "uniform": lambda differences: max(tuple(abs(difference) for difference in differences)),
    }

    def __init__(self, colour, other_colour):
        self.rgb_differences = tuple((value - other_value)
                                     for (value, other_value) in zip(colour.rgb, other_colour.rgb))

    def __eq__(self, other):
        return all(value == other_value
                   for (value, other_value) in zip(self.rgb_differences, other.rgb_differences))

    def __getitem__(self, distance_type):
        return self.types.get(distance_type, self.types["euclidean"])(self.rgb_differences)


def find_nearest_colour(colours_to_find, origin_colour, distance_type):
    return min(colours_to_find, key=lambda colour_to_find: (origin_colour - colour_to_find)[distance_type])


def substitute(theme, theme_colour_to_palette_colour):
    return re.compile('|'.join(theme_colour_to_palette_colour.keys())).sub(
        lambda matched_colour: theme_colour_to_palette_colour[matched_colour.group()], theme)


def read_theme_colours(theme, theme_colour_format):
    colour_pattern = Colour.formats.get(theme_colour_format, Colour.formats["hex"]).pattern
    return set(re.compile(colour_pattern, re.IGNORECASE).findall(theme))


def read_palette_colours(palette):
    return palette.splitlines()


def convert(theme="", theme_colour_format="", palette="", distance_type=""):
    if palette:
        palette_colours = list(map(lambda palette_colour_text: Colour(palette_colour_text, "hex"),
                                   read_palette_colours(palette)))
        theme_colours = list(map(lambda theme_colour_text: Colour(theme_colour_text, theme_colour_format),
                                 read_theme_colours(theme, theme_colour_format)))
        theme_colour_to_palette_colour = {
            theme_colour.original_text:
                format(find_nearest_colour(palette_colours, theme_colour, distance_type), theme_colour_format)
            for theme_colour in theme_colours
        }
        return substitute(theme, theme_colour_to_palette_colour)
    return theme


def main():
    palette_file_name = sys.argv[1]
    theme_file_name = sys.argv[2]
    for distance_type in ColourDistance.types.keys():
        theme_file_name_parts = theme_file_name.split('.')
        theme_file_name_extension = theme_file_name_parts[-1]
        converted_theme_file_name = '.'.join(theme_file_name_parts[0:-1] + [distance_type, theme_file_name_extension])
        with open(palette_file_name, 'r') as palette_file, \
                open(theme_file_name, 'r') as theme_file, \
                open(converted_theme_file_name, 'w') as converted_theme_file:
            converted_theme_file.write(
                convert(theme=theme_file.read(), palette=palette_file.read(), distance_type=distance_type))


if __name__ == '__main__':
    main()
