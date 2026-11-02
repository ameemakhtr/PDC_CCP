/**
 * Sequential Floyd-Warshall All-Pairs Shortest Path (APSP)
 * Course: Parallel and Distributed Computing (PDC)
 * Department: Computer and Information Systems Engineering, NED University
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define INF 1000000000

// Initialize adjacency matrix representing network graph
void initialize_graph(int *matrix, int n, double density, unsigned int seed) {
    srand(seed);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) {
                matrix[i * n + j] = 0;
            } else {
                double r = (double)rand() / RAND_MAX;
                if (r < density) {
                    matrix[i * n + j] = (rand() % 100) + 1; // edge weight 1 to 100
                } else {
                    matrix[i * n + j] = INF; // no direct edge
                }
            }
        }
    }
}

// Classical Sequential Floyd-Warshall Algorithm
void floyd_warshall_sequential(int *dist, int n) {
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            int dik = dist[i * n + k];
            if (dik == INF) continue; // Skip redundant updates
            
            for (int j = 0; j < n; j++) {
                int dkj = dist[k * n + j];
                if (dkj != INF && dik + dkj < dist[i * n + j]) {
                    dist[i * n + j] = dik + dkj;
                }
            }
        }
    }
}
