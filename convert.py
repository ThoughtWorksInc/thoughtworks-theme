import functools
import math
import re
import sys


def evaluate(colour):
    return map(functools.partial(int, base=16), list(colour[i:i + 2] for i in range(1, 7, 2)))


def get_euclidean_distance(colour, another_colour):
    return math.sqrt(sum(tuple(
        math.pow(value - another_value, 2) for (value, another_value) in
        zip(*map(evaluate, (colour, another_colour))))))


def find_nearest_colour(palette, colour):
    return min(palette, key=functools.partial(get_euclidean_distance, another_colour=colour))


def convert(content="", palette=None):
    if palette:
        colours_in_content = set(re.compile(r'#[0-9a-f]{6}', re.IGNORECASE).findall(content))
        dictionary = {
            colour: find_nearest_colour(palette, colour)
            for colour in colours_in_content
        }
        pattern = re.compile('|'.join(dictionary.keys()))
        return pattern.sub(lambda matched_colour: dictionary[matched_colour.group()], content)
    return content


if __name__ == '__main__':
    palette_file_name = sys.argv[1]
    original_file_name = sys.argv[2]
    split_name = original_file_name.split('.')
    split_name.insert(-1, 'ThoughtWorks')
    new_file_name = '.'.join(split_name)
    with open(palette_file_name, 'r') as palette_file,\
            open(original_file_name, 'r') as original_file,\
            open(new_file_name, 'w') as new_file:
        new_file.write(convert(original_file.read(), palette_file.read().splitlines()))
