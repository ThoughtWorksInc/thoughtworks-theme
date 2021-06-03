import math
import re
import sys


class ColourFormat:
    def __init__(self, pattern, evaluate):
        self.pattern = pattern
        self.evaluate = evaluate


class Colour:
    formats = {
        "hex": ColourFormat(
            r'#[0-9a-f]{6}',
            lambda text: tuple(map(lambda value: int(value, base=16), (text[i:i + 2] for i in range(1, 7, 2))))),
    }

    def __init__(self, text, format):
        self.text = text
        self.rgb = self.formats.get(format, self.formats["hex"]).evaluate(text)

    def __eq__(self, other):
        return all(value == another_value
                   for (value, another_value) in zip(self.rgb, other.rgb))

    def __repr__(self):
        return "Colour(text=" + self.text + ",rgb=" + ",".join(map(str, self.rgb)) + ")"

    def __sub__(self, other):
        return ColourDistance(self, other)


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


def find_nearest_colour(palette_colours, theme_colour, distance_type):
    return min(palette_colours, key=lambda palette_colour: (theme_colour - palette_colour)[distance_type])


def substitute(theme, theme_colour_to_palette_colour):
    pattern = re.compile('|'.join(theme_colour_to_palette_colour.keys()))
    return pattern.sub(lambda matched_colour: theme_colour_to_palette_colour[matched_colour.group()], theme)


def read_theme_colours(theme, theme_colour_format):
    colour_pattern = Colour.formats.get(theme_colour_format, Colour.formats["hex"]).pattern
    return set(re.compile(colour_pattern, re.IGNORECASE).findall(theme))


def convert(theme="", theme_colour_format="", palette="", distance_type=""):
    if palette:
        def create_colour(colour_text): return Colour(colour_text, theme_colour_format)

        palette_colours = list(map(create_colour, palette.splitlines()))
        theme_colours = list(map(create_colour, read_theme_colours(theme, theme_colour_format)))
        theme_colour_to_palette_colour = {
            theme_colour.text: find_nearest_colour(palette_colours, theme_colour, distance_type).text
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
