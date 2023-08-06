from colour import Color
from matplotlib.colors import LinearSegmentedColormap, to_hex

USA_PALETTES = dict(
	Alaska = dict(colors = ('#c5d0dc', '#4d769f', '#274e5a', '#71b9ce', '#6999bf'), order = (5, 3, 1, 2, 4), colorblind = True),
	Arizona = dict(colors = ('#e39a27', '#f2d6a2', '#d17d5e', '#603d42', '#aa5a40', '#3c3963'), order = (2, 1, 3, 5, 4, 6), colorblind = False))

COLORBLIND_PALETTE_NAMES = ('Alaska')
COLOBLIND_PALETTES = {name: USA_PALETTES[name] for name in COLORBLIND_PALETTE_NAMES}
EXPORT_FORMATS = {'HEX', 'DEC', 'REL', 'XML', 'IPE'}

def usa_brew(name, n=None, brew_type="discrete"):

    palette = USA_PALETTES.get(name)

    if not brew_type or type(name) in (int, float):
        raise Exception(f"Palette {name} does not exist.")

    if not n:
        n = len(palette["colors"])
        print(f"Palette '{name}' has '{n}' discrete colors")


    if brew_type not in {"discrete", "continuous"}:
        brew_type = "discrete"

    if brew_type == "discrete" and n > len(palette["colors"]):
        print(f"Number of requested colors ('{n}') greater than number of colors '{name}' can offer. \n Setting brew_type to 'continuous' instead.")
        brew_type = "continuous"

    out = list()
    if brew_type == "continuous":

        colors = [Color(c).rgb for c in palette["colors"]]
        color_map = LinearSegmentedColormap.from_list(name, colors, N=n)
        for i in range(n):
            out.append(to_hex(color_map(i)))

    elif brew_type == "discrete":

        rounds = n // len(palette["colors"])
        delta = n % len(palette["colors"])
        for _ in range(rounds):
            for i in range(len(palette["colors"])):
                idx = palette["order"][i] - 1
                color = palette["colors"][idx]
                out.append(color)

        for i in range(delta):
            idx = palette["order"][i] - 1
            color = palette["colors"][idx]
            out.append(color)

    return out


def is_colorblind_friendly(name):

    if name not in USA_PALETTES:
        raise Exception(f"Palette {name} does not exist.")
    else:
        print(f"Palette '{name}' is colorblind friendly.")

    return name in COLORBLIND_PALETTES_NAMES


def export(name, format="hex"):

    format = format.upper()

    palette = USA_PALETTES.get(name)
    colors = [Color(c) for c in palette.get("colors")]

    export = dict()
    if palette and format in EXPORT_FORMATS:
        if format == "HEX":
            export = {
                "name": name,
                "colors": [c.hex for c in colors]
            }

        elif format == "DEC":
            export = {
                "name": name,
                "colors": [tuple([int(v*255) for v in c.rgb]) for c in colors]
            }

        elif format == "REL":
            export = {
                "name": name,
                "colors": [tuple([round(v, 3) for v in c.rgb]) for c in colors]
            }

        elif format in {"XML", "IPE"}:
            color_values = [
                tuple([round(v, 3) for v in c.rgb])
                for c in colors
            ]
            color_strings = [" ".join(str(v) for v in c) for c in color_values]
            export = {
                "name": name,
                "colors": color_values,
                "tags": [
                    f"<color name=\"{name}-{i}\" value=\"{v}\" />"
                    for i, v in enumerate(color_strings, start=1)
                ]
            }

        return export