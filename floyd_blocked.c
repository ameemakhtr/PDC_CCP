/**
 * Cache-Blocked (Tiled) Parallel Floyd-Warshall Algorithm using OpenMP
 * Course: Parallel and Distributed Computing (PDC)
 * Department: Computer and Information Systems Engineering, NED University
 */

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define INF 1000000000
#define BLOCK_SIZE 64

static inline void fw_block_kernel(int *dist, int n, int bi, int bj, int bk, int bsize) {
    int i_end = (bi + bsize < n) ? (bi + bsize) : n;
    int j_end = (bj + bsize < n) ? (bj + bsize) : n;
    int k_end = (bk + bsize < n) ? (bk + bsize) : n;

    for (int k = bk; k < k_end; k++) {
        for (int i = bi; i < i_end; i++) {
            int dik = dist[i * n + k];
            if (dik == INF) continue;
            for (int j = bj; j < j_end; j++) {
                int dkj = dist[k * n + j];
                if (dkj != INF && dik + dkj < dist[i * n + j]) {
                    dist[i * n + j] = dik + dkj;
                }
            }
        }
    }
}

void floyd_warshall_blocked(int *dist, int n, int num_threads, int bsize) {
    omp_set_num_threads(num_threads);
    int num_blocks = (n + bsize - 1) / bsize;

    for (int k_b = 0; k_b < num_blocks; k_b++) {
        int bk = k_b * bsize;

        // Phase 1: Diagonal Block
        fw_block_kernel(dist, n, bk, bk, bk, bsize);

        // Phase 2: Row & Column cross-blocks
        #pragma omp parallel for schedule(static)
        for (int b = 0; b < num_blocks; b++) {
            if (b != k_b) {
                // Column block
                fw_block_kernel(dist, n, b * bsize, bk, bk, bsize);
                // Row block
                fw_block_kernel(dist, n, bk, b * bsize, bk, bsize);
            }
        }

        // Phase 3: Remaining Independent Blocks
        #pragma omp parallel for collapse(2) schedule(static)
        for (int i_b = 0; i_b < num_blocks; i_b++) {
            for (int j_b = 0; j_b < num_blocks; j_b++) {
                if (i_b != k_b && j_b != k_b) {
                    fw_block_kernel(dist, n, i_b * bsize, j_b * bsize, bk, bsize);
                }
            }
        }
    }
}
