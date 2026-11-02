/**
 * Parallel and Distributed Computing (PDC) - Complex Computing Problem (CCP)
 * Title: Performance Optimization of Floyd-Warshall APSP using OpenMP & Cache Blocking
 * Author: Ameem Akhtar (CR-23013), Minhal Rizvi (CR-23017), Muhammad Usman (CR-23038), Maaz Wasim (CR-23041)
 * Instructor: Dr. Saad Qasim Khan, Assistant Professor, CIS, NED University
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#define INF 1000000000
#define BLOCK_SIZE 64

// Initialize graph with random weights and given edge density
void initialize_graph(int *matrix, int n, double density, unsigned int seed) {
    srand(seed);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) {
                matrix[i * n + j] = 0;
            } else {
                double r = (double)rand() / RAND_MAX;
                if (r < density) {
                    matrix[i * n + j] = (rand() % 100) + 1; // Edge weight 1 to 100
                } else {
                    matrix[i * n + j] = INF;
                }
            }
        }
    }
}

// Sequential Floyd-Warshall
void floyd_warshall_sequential(int *dist, int n) {
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            int dik = dist[i * n + k];
            if (dik == INF) continue;
            for (int j = 0; j < n; j++) {
                int dkj = dist[k * n + j];
                if (dkj != INF && dik + dkj < dist[i * n + j]) {
                    dist[i * n + j] = dik + dkj;
                }
            }
        }
    }
}

// OpenMP Standard Parallel Floyd-Warshall (Row-wise parallelization)
void floyd_warshall_parallel(int *dist, int n, int num_threads) {
    omp_set_num_threads(num_threads);
    for (int k = 0; k < n; k++) {
        #pragma omp parallel for schedule(static)
        for (int i = 0; i < n; i++) {
            int dik = dist[i * n + k];
            if (dik == INF) continue;
            for (int j = 0; j < n; j++) {
                int dkj = dist[k * n + j];
                if (dkj != INF && dik + dkj < dist[i * n + j]) {
                    dist[i * n + j] = dik + dkj;
                }
            }
        }
    }
}

// Helper inline kernel for a single block computation in Blocked FW
static inline void fw_kernel(int *dist, int n, int bi, int bj, int bk, int bsize) {
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

// Cache-Blocked OpenMP Parallel Floyd-Warshall
void floyd_warshall_blocked(int *dist, int n, int num_threads, int bsize) {
    omp_set_num_threads(num_threads);
    int num_blocks = (n + bsize - 1) / bsize;

    for (int k_b = 0; k_b < num_blocks; k_b++) {
        int bk = k_b * bsize;

        // Phase 1: Diagonal Block
        fw_kernel(dist, n, bk, bk, bk, bsize);

        // Phase 2: Row & Column cross-blocks
        #pragma omp parallel for schedule(static)
        for (int b = 0; b < num_blocks; b++) {
            if (b != k_b) {
                // Column block
                fw_kernel(dist, n, b * bsize, bk, bk, bsize);
                // Row block
                fw_kernel(dist, n, bk, b * bsize, bk, bsize);
            }
        }

        // Phase 3: Remaining Independent Blocks
        #pragma omp parallel for collapse(2) schedule(static)
        for (int i_b = 0; i_b < num_blocks; i_b++) {
            for (int j_b = 0; j_b < num_blocks; j_b++) {
                if (i_b != k_b && j_b != k_b) {
                    fw_kernel(dist, n, i_b * bsize, j_b * bsize, bk, bsize);
                }
            }
        }
    }
}

// Verify that two distance matrices match exactly
int verify_results(const int *m1, const int *m2, int n) {
    for (int i = 0; i < n * n; i++) {
        if (m1[i] != m2[i]) {
            return 0; // Mismatch found
        }
    }
    return 1; // Exactly identical
}

int main(int argc, char *argv[]) {
    printf("======================================================================\n");
    printf("  NED University of Engineering & Technology - CIS Department\n");
    printf("  PDC Complex Computing Problem: Floyd-Warshall Optimization Benchmarks\n");
    printf("  Students: Ameem Akhtar (CR-23013), Minhal Rizvi (CR-23017)\n");
    printf("            Muhammad Usman (CR-23038), Maaz Wasim (CR-23041)\n");
    printf("======================================================================\n\n");

    // Correctness verification check on V=300
    int test_n = 300;
    int *orig = (int *)malloc(test_n * test_n * sizeof(int));
    int *seq_res = (int *)malloc(test_n * test_n * sizeof(int));
    int *par_res = (int *)malloc(test_n * test_n * sizeof(int));
    int *blk_res = (int *)malloc(test_n * test_n * sizeof(int));

    initialize_graph(orig, test_n, 0.40, 42);
    memcpy(seq_res, orig, test_n * test_n * sizeof(int));
    memcpy(par_res, orig, test_n * test_n * sizeof(int));
    memcpy(blk_res, orig, test_n * test_n * sizeof(int));

    printf("[1/3] Running Correctness Verification Test (V=%d)...\n", test_n);
    floyd_warshall_sequential(seq_res, test_n);
    floyd_warshall_parallel(par_res, test_n, 4);
    floyd_warshall_blocked(blk_res, test_n, 4, BLOCK_SIZE);

    int par_ok = verify_results(seq_res, par_res, test_n);
    int blk_ok = verify_results(seq_res, blk_res, test_n);

    if (par_ok && blk_ok) {
        printf("  [PASS] Sequential, Standard OpenMP, and Blocked OpenMP results match 100%%!\n\n");
    } else {
        printf("  [FAIL] Result mismatch detected! (Par: %d, Blk: %d)\n", par_ok, blk_ok);
        return 1;
    }

    free(orig);
    free(seq_res);
    free(par_res);
    free(blk_res);

    // Benchmark Matrix Sizes
    int sizes[] = {500, 1000, 1500, 2000};
    int num_sizes = 4;
    int threads[] = {1, 2, 4, 8};
    int num_threads = 4;

    FILE *f_csv = fopen("benchmark_results.csv", "w");
    if (!f_csv) {
        perror("Failed to open benchmark_results.csv");
        return 1;
    }
    fprintf(f_csv, "Size,Implementation,Threads,ExecutionTime_Sec,Speedup,Efficiency_Pct\n");

    printf("[2/3] Executing Scalability Benchmarks...\n");
    printf("%-8s %-20s %-8s %-15s %-10s %-12s\n", "Vertices", "Algorithm", "Threads", "Time (sec)", "Speedup", "Efficiency");
    printf("------------------------------------------------------------------------------\n");

    for (int s = 0; s < num_sizes; s++) {
        int n = sizes[s];
        int *base_graph = (int *)malloc(n * n * sizeof(int));
        int *work_graph = (int *)malloc(n * n * sizeof(int));
        initialize_graph(base_graph, n, 0.40, 100 + s);

        // Sequential Baseline Time
        memcpy(work_graph, base_graph, n * n * sizeof(int));
        double t_seq_start = omp_get_wtime();
        floyd_warshall_sequential(work_graph, n);
        double t_seq = omp_get_wtime() - t_seq_start;

        char sp_buf[16], eff_buf[16];
        snprintf(sp_buf, sizeof(sp_buf), "%.2fx", 1.0);
        snprintf(eff_buf, sizeof(eff_buf), "%.1f%%", 100.0);
        printf("%-8d %-20s %-8d %-15.4f %-10s %-11s\n", n, "Sequential", 1, t_seq, sp_buf, eff_buf);
        fprintf(f_csv, "%d,Sequential,1,%.5f,1.0000,100.00\n", n, t_seq);

        // Standard OpenMP Parallel for threads 1, 2, 4, 8
        for (int t = 0; t < num_threads; t++) {
            int th = threads[t];
            memcpy(work_graph, base_graph, n * n * sizeof(int));
            double t_start = omp_get_wtime();
            floyd_warshall_parallel(work_graph, n, th);
            double t_par = omp_get_wtime() - t_start;
            double speedup = t_seq / t_par;
            double efficiency = (speedup / th) * 100.0;

            snprintf(sp_buf, sizeof(sp_buf), "%.2fx", speedup);
            snprintf(eff_buf, sizeof(eff_buf), "%.1f%%", efficiency);
            printf("%-8d %-20s %-8d %-15.4f %-10s %-11s\n", n, "OpenMP-Standard", th, t_par, sp_buf, eff_buf);
            fprintf(f_csv, "%d,OpenMP-Standard,%d,%.5f,%.4f,%.2f\n", n, th, t_par, speedup, efficiency);
        }

        // Blocked OpenMP Parallel for threads 4 and 8
        for (int t = 2; t < num_threads; t++) {
            int th = threads[t];
            memcpy(work_graph, base_graph, n * n * sizeof(int));
            double t_start = omp_get_wtime();
            floyd_warshall_blocked(work_graph, n, th, BLOCK_SIZE);
            double t_blk = omp_get_wtime() - t_start;
            double speedup = t_seq / t_blk;
            double efficiency = (speedup / th) * 100.0;

            snprintf(sp_buf, sizeof(sp_buf), "%.2fx", speedup);
            snprintf(eff_buf, sizeof(eff_buf), "%.1f%%", efficiency);
            printf("%-8d %-20s %-8d %-15.4f %-10s %-11s\n", n, "OpenMP-Blocked", th, t_blk, sp_buf, eff_buf);
            fprintf(f_csv, "%d,OpenMP-Blocked,%d,%.5f,%.4f,%.2f\n", n, th, t_blk, speedup, efficiency);
        }
        printf("------------------------------------------------------------------------------\n");

        free(base_graph);
        free(work_graph);
    }

    fclose(f_csv);
    printf("\n[3/3] Benchmarks Completed Successfully. Data exported to benchmark_results.csv\n");
    return 0;
}
