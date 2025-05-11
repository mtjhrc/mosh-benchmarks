#include <ncurses.h>

constexpr int TILE_WIDTH = 4;
constexpr int TILE_HEIGHT = TILE_WIDTH / 2;

constexpr int COLOR_AAA = 1;
constexpr int COLOR_BBB = 2;

constexpr int COLORPAIR_AAA = 1;
constexpr int COLORPAIR_BBB = 2;
constexpr int COLORPAIR_BLACK = 3;
const char *color_schemes[] = {"aaa", "bbb"};

void drawCheckerboard(int colorpair, int rows, int cols) {
    for (int row = 0; row < rows; ++row) {
        for (int col = 0; col < cols; ++col) {
            int isBlack = (row + col) % 2;

            if (isBlack) {
                attron(COLOR_PAIR(COLORPAIR_BLACK));
            } else {
                attron(COLOR_PAIR(colorpair));
            }

            for (int i = 0; i < TILE_WIDTH / 2; ++i) {
                for (int j = 0; j < TILE_WIDTH; ++j) {
                    mvprintw(row * (TILE_WIDTH / 2) + i, col * TILE_WIDTH + j, "x");
                }
            }

            if (isBlack) {
                attroff(COLOR_PAIR(colorpair));
            } else {
                attroff(COLOR_PAIR(2));
            }
        }
    }

    attron(COLOR_PAIR(COLORPAIR_BLACK));
    //mvprintw(0, 0, "%s", color_schemes[colorpair - 1]);
    mvprintw(LINES-1, COLS-4, "%s", color_schemes[colorpair - 1]);
    attroff(COLOR_PAIR(COLORPAIR_BLACK));
}

int main() {
    initscr();
    start_color();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    curs_set(0);
    init_pair(COLORPAIR_BLACK, COLOR_WHITE, COLOR_BLACK);
    init_pair(COLORPAIR_AAA, COLOR_WHITE, COLOR_GREEN);
    init_pair(COLORPAIR_BBB, COLOR_WHITE, COLOR_RED);

    int color = COLORPAIR_AAA;
    while (true) {
        int rows = (LINES * 2 + TILE_WIDTH - 1) / TILE_WIDTH;
        int cols = (COLS + TILE_WIDTH - 1) / TILE_WIDTH;

        drawCheckerboard(color, rows, cols);
        refresh();

        int ch = getch();
        if (ch == 'q') {
            break;
        } else if (ch == 'n') {
            color = 3 - color;
        }
    }

    endwin();
    return 0;
}