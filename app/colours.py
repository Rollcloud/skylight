import colorsys


def brighten(colour, factor):
    h, s, v = colorsys.rgb_to_hsv(*colour.colour)

    return Colour(colour=colorsys.hsv_to_rgb(h, s, min(max(v * factor, 0), 1)))


class Colour:
    """
    A class to describe RGB based colours in different formats
    """

    def __init__(self, *args, colour=(0, 0, 0)):
        # use the colour keyword to pass in the raw RGB values between 0.0 and 1.0
        self.colour = colour

        if len(args) == 1:
            description = args[0]
            if isinstance(description, str):
                if description[0] == '#':
                    # description == "#ff00ff"
                    h = description.lstrip('#')
                    self.colour = tuple(
                        int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4)
                    )
                else:
                    # description == "blue"
                    raise NotImplementedError("Cannot process colour names")
            elif isinstance(description, tuple) and len(description) == 3:
                # description == (0, 127, 255): 8 byte RGB
                self.colour = tuple(min(v / 255, 1) for v in description)

        elif len(args) == 3:
            # args == (0, 127, 255): 8 byte RGB
            self.colour = tuple(min(v / 255, 1) for v in args)

    def __getattr__(self, key):
        if key == 'hex':
            return f'#{self.rgb[0]:02x}{self.rgb[1]:02x}{self.rgb[2]:02x}'
        elif key == 'rgb':
            return tuple(int(v * 255) for v in self.colour)
        elif key == 'hsv':
            return tuple(int(v * 255) for v in colorsys.rgb_to_hsv(*self.colour))
        elif key == 'name':
            raise NotImplementedError("Cannot process colour names")
        else:
            raise AttributeError

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return f"Colour{self.rgb}"

    def from_hsv(self, h, s, v):
        self.colour = colorsys.hsv_to_rgb(
            min(h / 255.0, 1.0), min(s / 255.0, 1.0), min(v / 255.0, 1.0)
        )

        return self
