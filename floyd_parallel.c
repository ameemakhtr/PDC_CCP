/**
 * Parallel Floyd-Warshall Algorithm using OpenMP
 * Course: Parallel and Distributed Computing (PDC)
 * Department: Computer and Information Systems Engineering, NED University
 */

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define INF 1000000000

void floyd_warshall_parallel(int *dist, int n, int num_threads) {
    omp_set_num_threads(num_threads);
    
    // Outer loop k must remain sequential due to loop-carried dependency
    for (int k = 0; k < n; k++) {
        // Inner loops i and j can be parallelized safely across threads
        #pragma omp parallel for schedule(static)
        for (int i = 0; i < n; i++) {
            int dik = dist[i * n + k];
            if (dik == INF) continue; // Early pruning of unreachable nodes
            
            for (int j = 0; j < n; j++) {
                int dkj = dist[k * n + j];
                if (dkj != INF && dik + dkj < dist[i * n + j]) {
                    dist[i * n + j] = dik + dkj;
                }
            }
        }
    }
}
