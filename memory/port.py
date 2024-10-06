from enum import auto, Enum


class Port(Enum):
    SCREEN_SET_PIXEL_X = 240
    SCREEN_SET_PIXEL_Y = auto()
    SCREEN_DRAW_PIXEL = auto()
    SCREEN_CLEAR_PIXEL = auto()
    SCREEN_LOAD_PIXEL = auto()
    SCREEN_PUSH = auto()
    SCREEN_CLEAR = auto()
    CHAR_WRITE = auto()
    CHAR_PUSH = auto()
    CHAR_CLEAR = auto()
    NUMBER_SHOW = auto()
    NUMBER_CLEAR = auto()
    NUMBER_SET_SIGNED = auto()
    NUMBER_SET_UNSIGNED = auto()
    LOAD_RNG = auto()
    LOAD_CONTROLLER = auto()

    @staticmethod
    def get_port(name: str) -> "Port":
        try:
            return Port[name]
        except KeyError:
            print(f"Port {name} not found")
            raise KeyError

    @staticmethod
    def output_value_matters(port) -> bool:
        return not (port in output_value_useless_ports)

output_value_useless_ports = [
    Port.SCREEN_DRAW_PIXEL,
    Port.SCREEN_CLEAR_PIXEL,
    Port.SCREEN_LOAD_PIXEL,
    Port.SCREEN_PUSH,
    Port.SCREEN_CLEAR,

    Port.CHAR_PUSH,
    Port.CHAR_CLEAR,

    Port.NUMBER_CLEAR,
    Port.NUMBER_SET_SIGNED,
    Port.NUMBER_SET_UNSIGNED,

    Port.LOAD_RNG,
    Port.LOAD_CONTROLLER,
]
