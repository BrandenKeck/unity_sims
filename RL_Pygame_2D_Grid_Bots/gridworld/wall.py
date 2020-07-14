class wall():

    # Initialize wall properties
    def __init__(self, img, x, y):

        self.img = img

        self.x = x
        self.y = y
        self.pos_x = 25 * x
        self.pos_y = 25 * y
