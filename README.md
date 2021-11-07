# Thoughtworks Theme

This is a collection of IDEs theme based on the (new) Thoughtworks Brand Guidelines color palette. The color palette is also as the same as the colors in our keynote template.

![Thoughtworks Brand Guidelines - Color](./tw_202108_brand_guidelines_color.png)

## How to use

There are READMEs in every directory such as `JetBrains`, `Terminal`, `VisualStudioCode`, and so on. Find what you want and install the themes by the instruction.

## Contribution

Basically there're several ways to contribute this repository.

- Define a theme in your IDE and export it as a importable setting patch.
- Export a readable theme file(e.g. `xml`) and convert it within the ThoughtWorks colors([Docs](#convertor)).
- Check if there is instruction in the corresponding README and follow it.

### Convertor

The convertor developed under `python3` and via TDD way. It will convert all the color-like string (`#[0-9a-f]{6}`) in a readable theme file to the nearest color (least euclidean distance) in palette.

You can use it like,

```shell
    python3 convert.py ThoughtWorks.palette <readable_theme_file>
```

in which the `ThoughtWorks.palette` is a palette file with lines of color-like string.

And also test the convertor by

```shell
    python3 test_convert.py
```
