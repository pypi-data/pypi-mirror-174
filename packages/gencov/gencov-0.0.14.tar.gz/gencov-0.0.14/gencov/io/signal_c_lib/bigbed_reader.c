#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>
#include <math.h>
#include "bigWig.h"


int check_file_exists(char *path) {
    FILE *stream = fopen(path, "r");
    if (stream) {
        fclose(stream);
        return 0;
    } else {
        return 1;
    }
}


int main(int argc, char *argv[]) {

    char *help =
        "extract coverage from bigbed\n"
        "\n"
        "usage:\n"
        "    IN_FILE OUT_FILE\n"
        "    input.bigbed /dev/stdout\n"
        "\n"
        "arguments:\n"
        "    IN_FILE    path to input bigwig\n"
        "    OUT_FILE   path to output binary file to store result\n"
        "\n"
        "read from stdin:\n"
        "    WINDOW     window as chr-id start end";

    for (int i = 0; i < argc; i += 1) {
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            fprintf(stderr, "%s\n", help);
            return 0;
        }
    }
    if (argc != 3) {
        fprintf(stderr, "invalid number of arguments\n");
        return 1;
    }
    char *input_path = argv[1];
    char *output_path = argv[2];
    if (check_file_exists(input_path) != 0) {
        fprintf(stderr, "file not found: %s\n", input_path);
        return 1;
    }
    
    if (bwInit(1<<17) != 0) {
        fprintf(stderr, "received an error in bwInit\n");
        return 1;
    }

    if (!bbIsBigBed(input_path, NULL)) {
        fprintf(stderr, "not a bigbed file: %s\n", input_path);
        return 1;
    }

    bigWigFile_t *input_file = bbOpen(input_path, NULL);
    if (!input_file) {
        fprintf(stderr, "failed to open %s\n", input_path);
        return 1;
    }

    FILE *output_file = fopen(output_path, "w");
    if (!output_file) {
        fprintf(stderr, "failed to open %s\n", output_path);
        return 1;
    }

    bbOverlappingEntries_t *intervals = NULL;
    char raw_window[128];
    while (fgets(raw_window, sizeof(raw_window), stdin)) {
        raw_window[strcspn(raw_window, "\r\n")] = 0;
        char chr_name[32];
        int start, end;
        if (sscanf(raw_window, "%31s %d %d", chr_name, &start, &end) != 3) {
            fprintf(stderr, "invalid window format: %s\n", raw_window);
            return 1;
        }
        if (start > end) {
            fprintf(stderr, "invalid window: %s\n", raw_window);
            return 1;
        }
        intervals = bbGetOverlappingEntries(input_file, chr_name, start, end, 0);
        if (!intervals) {
            fprintf(stderr, "invalid window: %s\n", raw_window);
            return 1;
        }
        fwrite(&intervals->l, sizeof(uint32_t), 1, output_file);
        for (int index = 0; index < intervals->l; index += 1) {
            fwrite(&intervals->start[index], sizeof(uint32_t), 1, output_file);
            fwrite(&intervals->end[index], sizeof(uint32_t), 1, output_file);
        }
        bbDestroyOverlappingEntries(intervals);
    }

    fclose(output_file);

    bwClose(input_file);
    bwCleanup();
    return 0;

}
