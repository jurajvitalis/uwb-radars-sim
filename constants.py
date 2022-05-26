TICKRATE = 3

CANVAS_WIDTH = 420
CANVAS_HEIGHT = 420

ROOM_OFFSET = 10

PLOT_WIDTH = 400
PLOT_HEIGHT = 400

SCALE = 50

TX_X = 0
TX_Y = 0

X1 = -4
X2 = -1.5
X3 = 1.5
X4 = 4

Y1 = 4
Y2 = 0
Y3 = 0
Y4 = 4

WALL_NORTH_Y = ROOM_OFFSET
WALL_EAST_X = CANVAS_WIDTH - ROOM_OFFSET
WALL_SOUTH_Y = CANVAS_HEIGHT - ROOM_OFFSET
WALL_WEST_X = ROOM_OFFSET

TX_X_POS_CANVAS = CANVAS_WIDTH // 2
TX_Y_POS_CANVAS = CANVAS_HEIGHT - ROOM_OFFSET

RX1_X_POS_CANVAS = TX_X_POS_CANVAS + (X1 * SCALE)
RX1_Y_POS_CANVAS = WALL_SOUTH_Y - (Y1 * SCALE)

RX2_X_POS_CANVAS = TX_X_POS_CANVAS + (X2 * SCALE)
RX2_Y_POS_CANVAS = WALL_SOUTH_Y - (Y2 * SCALE)

RX3_X_POS_CANVAS = TX_X_POS_CANVAS + (X3 * SCALE)
RX3_Y_POS_CANVAS = WALL_SOUTH_Y - (Y3 * SCALE)

RX4_X_POS_CANVAS = TX_X_POS_CANVAS + (X4 * SCALE)
RX4_Y_POS_CANVAS = WALL_SOUTH_Y - (Y4 * SCALE)

GRID_COLOR = '#868482'
TX_COLOR = '#b40000'
RX_COLOR = '#14aaff'