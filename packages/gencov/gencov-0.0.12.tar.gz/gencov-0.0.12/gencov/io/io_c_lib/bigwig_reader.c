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
        "extract coverage from bigwig\n"
        "\n"
        "usage:\n"
        "    IN_FILE OUT_FILE MODE BIN_SIZE DEF_VALUE\n"
        "    input.bigwig /dev/stdout values 10 0\n"
        "\n"
        "arguments:\n"
        "    IN_FILE    path to input bigwig\n"
        "    OUT_FILE   path to output binary file to store result\n"
        "    MODE       report mode (intervals or values)\n"
        "    BIN_SIZE   bin size in base pairs (10, only used if mode is values))\n"
        "    DEF_VALUE  default value for nan (only used if mode is values)\n"
        "\n"
        "read from stdin:\n"
        "    WINDOW     window as chr-id start end";

    for (int i = 0; i < argc; i += 1) {
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            fprintf(stderr, "%s\n", help);
            return 0;
        }
    }
    if (argc != 6) {
        fprintf(stderr, "invalid number of arguments\n");
        return 1;
    }
    char *input_path = argv[1];
    char *output_path = argv[2];
    char *mode = argv[3];
    int bin_size = atoi(argv[4]);
    float def_value = atof(argv[5]);
    int return_mode;
    if (check_file_exists(input_path) != 0) {
        fprintf(stderr, "file not found: %s\n", input_path);
        return 1;
    }
    
    if (strcmp(mode, "intervals") == 0) {
        return_mode = 0;
    } else if (strcmp(mode, "values") == 0) {
        return_mode = 1;
        if (bin_size <= 0) {
            fprintf(stderr, "invalid bin size: %s\n", argv[3]);
            return 1;
        }
    } else {
        fprintf(stderr, "unsupported mode: %s\n", mode);
        return 1;
    }

    if (bwInit(1<<17) != 0) {
        fprintf(stderr, "received an error in bwInit\n");
        return 1;
    }

    if (!bwIsBigWig(input_path, NULL)) {
        fprintf(stderr, "not a bigwig file: %s\n", input_path);
        return 1;
    }

    bigWigFile_t *input_file = bwOpen(input_path, NULL, "r");
    if (!input_file) {
        fprintf(stderr, "failed to open %s\n", input_path);
        return 1;
    }

    FILE *output_file = fopen(output_path, "w");
    if (!output_file) {
        fprintf(stderr, "failed to open %s\n", output_path);
        return 1;
    }

    bwOverlappingIntervals_t *intervals = NULL;
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
        if (return_mode == 0) {
            intervals = bwGetOverlappingIntervals(input_file, chr_name, start, end);
            if (!intervals) {
                fprintf(stderr, "invalid window: %s\n", raw_window);
                return 1;
            }
            fwrite(&intervals->l, sizeof(uint32_t), 1, output_file);
            for (int index = 0; index < intervals->l; index += 1) {
                fwrite(&intervals->start[index], sizeof(uint32_t), 1, output_file);
                fwrite(&intervals->end[index], sizeof(uint32_t), 1, output_file);
                fwrite(&intervals->value[index], sizeof(float), 1, output_file);
            }
        } else {
            intervals = bwGetValues(input_file, chr_name, start, end, 1);
            if (!intervals) {
                fprintf(stderr, "invalid window: %s\n", raw_window);
                return 1;
            }
            int bin_count = -(-(end - start) / bin_size);
            float *window_values = malloc(sizeof(float) * bin_count);
            int from_index = 0;
            for (int index = 0; index < bin_count; index += 1) {
                float value = intervals->value[from_index];
                if (isnan(value)) value = def_value;
                window_values[index] = value;
                from_index += bin_size;
            }
            fwrite(window_values, sizeof(float), bin_count, output_file);
            free(window_values);
        }
        bwDestroyOverlappingIntervals(intervals);
    }

    fclose(output_file);

    bwClose(input_file);
    bwCleanup();
    return 0;

}
