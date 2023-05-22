#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[])
{
    int pid;
    char key;

    pid = atoi(argv[1]);
    key = argv[2][0];

    unsigned int seed = pid + key;

    srand(seed);

    unsigned int result = rand();

    printf("%d\n", result);

    exit(result);
}

