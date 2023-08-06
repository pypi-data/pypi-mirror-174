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

    #ifdef _WIN32
        #include <io.h>
        #include <fcntl.h>
        setmode(fileno(stdin), O_BINARY);
        setmode(fileno(stdout), O_BINARY);
    #endif
    
    char *help =
        "read bbi file (bigwig or bigbed) header\n"
        "\n"
        "usage:\n"
        "    IN_FILE OUT_FILE MODE\n"
        "    input.bigwig /dev/stdout chr_sizes\n"
        "\n"
        "arguments:\n"
        "    IN_FILE   path to input bigwig\n"
        "    OUT_FILE  path to output binary file to store result (- for stdout)\n"
        "    MODE      data to get (chr_sizess)";

    for (int i = 0; i < argc; i += 1) {
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            fprintf(stderr, "%s\n", help);
            return 0;
        }
    }
    if (argc != 1 + 3) {
        fprintf(stderr, "invalid number of arguments\n");
        return 1;
    }
    char *input_path = argv[1];
    char *output_path = argv[2];
    char *mode = argv[3];
    if (check_file_exists(input_path) != 0) {
        fprintf(stderr, "file not found: %s\n", input_path);
        return 1;
    }

    if (bwInit(1<<17) != 0) {
        fprintf(stderr, "error during bigwig or bigbed initialization\n");
        return 1;
    }

    bigWigFile_t *input_file = bwOpen(input_path, NULL, "r");
    if (!input_file) {
        fprintf(stderr, "failed to open %s\n", input_path);
        return 1;
    }

    FILE *output_file = (strcmp(output_path, "-") == 0) ? stdout : fopen(output_path, "w");
    if (!output_file) {
        fprintf(stderr, "failed to open %s\n", output_path);
        return 1;
    }

    if (strcmp(mode, "chr_sizes") == 0) {
        uint64_t chr_count = input_file->cl->nKeys;
        fwrite(&chr_count, sizeof(uint64_t), 1, output_file);
        for (uint64_t chr_index = 0; chr_index < chr_count; chr_index += 1) {
            char *chr_id = input_file->cl->chrom[chr_index];
            uint32_t chr_size = input_file->cl->len[chr_index];
            uint64_t chr_id_size = strlen(chr_id);
            fwrite(&chr_id_size, sizeof(uint64_t), 1, output_file);
            fputs(chr_id, output_file);
            fwrite(&chr_size, sizeof(uint32_t), 1, output_file);
        }
    } else {
        fprintf(stderr, "unsupported mode: %s\n", mode);
        return 1;
    }

    fclose(output_file);
    bwClose(input_file);
    bwCleanup();
    return 0;

}
