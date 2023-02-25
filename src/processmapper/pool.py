from dataclasses import dataclass, field
from processmapper.painter import Painter
from processmapper.lane import Lane
import processmapper.constants as Configs


@dataclass
class Pool:
    name: str = field(init=True)
    # font: str = field(init=True, default=None)
    # font_size: int = field(init=True, default=None)
    # font_colour: str = field(init=True, default=None)

    x: int = field(init=False, default=0)
    y: int = field(init=False, default=0)
    width: int = field(init=False, default=0)
    height: int = field(init=False, default=0)
    painter: Painter = field(init=False)

    _lanes: list = field(init=False, default_factory=list)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        ...

    def set_draw_position(self, x: int, y: int, painter: Painter) -> tuple:
        self.x = x
        self.y = y
        self.painter = painter
        last_lane_y = self._lanes[-1].y
        last_lane_height = self._lanes[-1].height

        self.width, self.height = (
            Configs.POOL_TEXT_WIDTH,
            last_lane_y + last_lane_height - self.y,
        )
        return self.x, self.y, self.width, self.height

    def draw(self):
        self.painter.draw_box(
            self.x,
            self.y,
            self.width,
            self.height,
            "#d9d9d9",
        )
        ### Draw the lane text box
        self.painter.draw_box_with_vertical_text(
            self.x,
            self.y,
            Configs.POOL_TEXT_WIDTH,
            self.height,
            "#333333",
            self.name,
            text_alignment="centre",
            text_font="arial",
            text_font_size=12,
            text_font_colour="white",
        )

    def add_lane(self, lane_name: str) -> Lane:
        lane = Lane(lane_name)
        self._lanes.append(lane)
        return lane
