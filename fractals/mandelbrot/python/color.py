class Color:

    BLACK  = (0,0,0)
    WHITE  = (255,255,255)
    RED    = (255,0,0)
    ORANGE = (255,128,0)
    YELLOW = (255,255,0)
    GREEN  = (0,255,0)
    BLUE   = (0,0,255)
    INDIGO = (128,0,255)
    VIOLET = (255,0,255)

    RAINBOW = [
        RED,
        ORANGE,
        YELLOW,
        GREEN,
        BLUE,
        INDIGO,
        VIOLET
    ]

    BW = [BLACK, WHITE]

    # Default Color Palette
    PALETTE = RAINBOW.copy()

    @classmethod
    def set_pallete(self, new_palette):
        Color.PALETTE = new_palette.copy()

    @classmethod
    def rotate_pallete(self):
        c = Color.PALETTE.pop(1)
        Color.PALETTE.append(c)

    @classmethod
    def randomize_pallete(self):
        pass

    @classmethod
    def to_RGB(self, value):
        return Color.PALETTE[value % len(Color.PALETTE)]
