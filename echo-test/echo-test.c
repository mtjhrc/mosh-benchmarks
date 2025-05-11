#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <stdbool.h>
#include <stdio.h>

#define BUFFER_SIZE 1024
#define CLEAR_SCREEN "\033[H\033[J"  // ANSI escape sequence to clear the screen

void write_all(int fd, const char *buffer, size_t count) {
    size_t total_written = 0;
    while (total_written < count) {
        ssize_t bytes_written = write(fd, buffer + total_written, count - total_written);
        if (bytes_written < 0) {
            perror("write");
            exit(1);
        }
        total_written += bytes_written;
    }
}

void enable_raw_mode(struct termios *original_termios) {
    struct termios raw;

    if (tcgetattr(STDIN_FILENO, original_termios) == -1) {
        perror("tcgetattr");
        exit(1);
    }

    raw = *original_termios;
    raw.c_lflag &= ~(ECHO | ICANON); 
    raw.c_cc[VMIN] = 1;             
    raw.c_cc[VTIME] = 0;

    // Set the modified attributes
    if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw) == -1) {
        perror("tcsetattr");
        exit(1);
    }
}

void disable_raw_mode(const struct termios *original_termios) {
    // Restore the original terminal attributes
    if (tcsetattr(STDIN_FILENO, TCSAFLUSH, original_termios) == -1) {
        perror("tcsetattr");
        exit(1);
    }
}

void read_input() {
    char c;

    while (1) {
        ssize_t bytes_read = read(STDIN_FILENO, &c, 1);
        if (bytes_read < 0) {
            perror("read");
            exit(1);
        }

        if (c == '\n') {
            break;
        }
        if (c == 'q') {
            exit(0);
        }

        write_all(STDOUT_FILENO, &c, 1);
    }
}

int main() {
    struct termios original_termios;
    int input_count = 0;
    const char *frame_detect[] = {"aaaa", "bbbb"};

    // Enable raw mode
    enable_raw_mode(&original_termios);

    while (true) {
        char ready_message[BUFFER_SIZE];
        int ready_len = snprintf(ready_message, BUFFER_SIZE, "[READY %d %s]\n", input_count, frame_detect[input_count % 2]);
        write_all(STDOUT_FILENO, CLEAR_SCREEN, strlen(CLEAR_SCREEN));
        write_all(STDOUT_FILENO, ready_message, ready_len);
        read_input();
        input_count++;
    }

    // Restore original terminal settings
    disable_raw_mode(&original_termios);

    return 0;
}
