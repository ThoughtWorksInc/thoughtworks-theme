import math
import re
import sys


class Colour:
    def __init__(self, text):
        self.text = text
        self.rgb = evaluate(text)

    def __eq__(self, other):
        return all(value == another_value
                   for (value, another_value) in zip(self.rgb, other.rgb))

    def __repr__(self):
        return "Colour(text=" + self.text + ",rgb=" + ",".join(map(str, self.rgb)) + ")"


def evaluate(colour):
    return tuple(map(lambda value: int(value, base=16), (colour[i:i + 2] for i in range(1, 7, 2))))


def get_euclidean_distance(colour, another_colour):
    return math.sqrt(sum(tuple(math.pow(value - another_value, 2)
                               for (value, another_value) in zip(colour.rgb, another_colour.rgb))))


def get_manhattan_distance(colour, another_colour):
    return sum(tuple(abs(value - another_value)
                     for (value, another_value) in zip(colour.rgb, another_colour.rgb)))


def get_uniform_distance(colour, another_colour):
    return max(tuple(abs(value - another_value)
                     for (value, another_value) in zip(colour.rgb, another_colour.rgb)))


distance_types = {
    'euclidean': get_euclidean_distance,
    'manhattan': get_manhattan_distance,
    'uniform': get_uniform_distance
}


def find_nearest_colour(palette_colours, theme_colour, distance_type):
    distance_calculator = distance_types.get(distance_type, get_euclidean_distance)
    return min(palette_colours, key=lambda palette_colour: distance_calculator(theme_colour, palette_colour))


def substitute(theme, theme_colour_to_palette_colour):
    pattern = re.compile('|'.join(theme_colour_to_palette_colour.keys()))
    return pattern.sub(lambda matched_colour: theme_colour_to_palette_colour[matched_colour.group()], theme)


def convert(theme="", palette="", distance_type=""):
    if palette:
        palette_colours = list(map(Colour, palette.splitlines()))
        theme_colours = list(map(Colour, set(re.compile(r'#[0-9a-f]{6}', re.IGNORECASE).findall(theme))))
        theme_colour_to_palette_colour = {
            theme_colour.text: find_nearest_colour(palette_colours, theme_colour, distance_type).text
            for theme_colour in theme_colours
        }
        return substitute(theme, theme_colour_to_palette_colour)
    return theme


def main():
    palette_file_name = sys.argv[1]
    theme_file_name = sys.argv[2]
    for distance_type in distance_types.keys():
        theme_file_name_parts = theme_file_name.split('.')
        theme_file_name_extension = theme_file_name_parts[-1]
        converted_theme_file_name = '.'.join(theme_file_name_parts[0:-1] + [distance_type, theme_file_name_extension])
        with open(palette_file_name, 'r') as palette_file, \
                open(theme_file_name, 'r') as theme_file, \
                open(converted_theme_file_name, 'w') as converted_theme_file:
            converted_theme_file.write(convert(theme_file.read(), palette_file.read(), distance_type))


if __name__ == '__main__':
    main()
