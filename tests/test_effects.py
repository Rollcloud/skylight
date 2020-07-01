from pytest import approx

from app.colours import Colour
from app.effects import Cloud


class TestCloud:
    def setup(self):
        self.leds = range(10)
        self.cloud = Cloud(0, width=8, edge=3, opacity=0.3)

    def test_cloud_opacities(self):
        opacities = [self.cloud.opacity_at(x) for x in self.leds]
        assert opacities == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.cloud.position = 1

        opacities = [self.cloud.opacity_at(x) for x in self.leds]
        assert opacities == approx([0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        self.cloud.position = 5

        opacities = [self.cloud.opacity_at(x) for x in self.leds]
        assert opacities == approx([0.3, 0.3, 0.3, 0.2, 0.1, 0, 0, 0, 0, 0])

        self.cloud.position = 9

        opacities = [self.cloud.opacity_at(x) for x in self.leds]
        assert opacities == approx([0, 0, 0.1, 0.2, 0.3, 0.3, 0.3, 0.2, 0.1, 0])

        self.cloud.position = 17

        opacities = [self.cloud.opacity_at(x) for x in self.leds]
        assert opacities == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def test_cloud_colours(self):
        self.cloud.position = 9
        colours = self.cloud.calc_colours(self.leds, Colour('#ffffff'))

        assert [c.hex for c in colours] == [
            '#ffffff',
            '#ffffff',
            '#e5e5e5',
            '#cccccc',
            '#b2b2b2',
            '#b2b2b2',
            '#b2b2b2',
            '#cccccc',
            '#e5e5e5',
            '#ffffff',
        ]
