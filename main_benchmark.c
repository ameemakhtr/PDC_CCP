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
#define RUNS 5   // every timing is the median of RUNS round-robin runs

// Thread counts used everywhere: 6 = physical cores, 12 = all hardware threads (i7-9750H)
static const int THREADS[] = {1, 2, 4, 6, 8, 12};
#define NUM_THREADS 6
#define NC (1 + 2 * NUM_THREADS + 5)  // timed configurations per graph size

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

// Run one implementation in place: 0 = Sequential, 1 = OpenMP-Standard, 2 = OpenMP-Blocked
void run_algo(int algo, int *dist, int n, int threads, int bsize) {
    if (algo == 0) floyd_warshall_sequential(dist, n);
    else if (algo == 1) floyd_warshall_parallel(dist, n, threads);
    else floyd_warshall_blocked(dist, n, threads, bsize);
}

// Independent oracle (different algorithm): Bellman-Ford from every source vertex.
// ponytail: slow, only used on the small correctness-test graphs
void apsp_bellman_ford(const int *g, int *d, int n) {
    for (int s = 0; s < n; s++) {
        int *ds = d + s * n;
        for (int v = 0; v < n; v++) ds[v] = (v == s) ? 0 : INF;
        int changed = 1;
        while (changed) {
            changed = 0;
            for (int u = 0; u < n; u++) {
                if (ds[u] == INF) continue;
                for (int v = 0; v < n; v++) {
                    int w = g[u * n + v];
                    if (w != INF && ds[u] + w < ds[v]) {
                        ds[v] = ds[u] + w;
                        changed = 1;
                    }
                }
            }
        }
    }
}

// Check every implementation, thread count and block size against the oracle.
// Sizes cover 1 vertex, below / equal / above one block, and non-multiples of B.
void run_correctness_tests(void) {
    int sizes[] = {1, 2, 17, 63, 64, 65, 130, 300};
    double densities[] = {0.02, 0.40, 1.00};
    int blocks[] = {16, 64, 128};
    int max_n = 300, tests = 0;
    size_t bytes = (size_t)max_n * max_n * sizeof(int);
    int *g = malloc(bytes), *ref = malloc(bytes), *out = malloc(bytes);

    for (int si = 0; si < 8; si++)
    for (int di = 0; di < 3; di++)
    for (unsigned int seed = 1; seed <= 3; seed++) {
        int n = sizes[si];
        initialize_graph(g, n, densities[di], seed);
        apsp_bellman_ford(g, ref, n);

        for (int algo = 0; algo < 3; algo++)
        for (int t = 0; t < NUM_THREADS; t++) {
            if (algo == 0 && t > 0) break;      // sequential has no thread count
            for (int b = 0; b < 3; b++) {
                if (algo != 2 && b > 0) break;  // only the blocked version uses B
                memcpy(out, g, (size_t)n * n * sizeof(int));
                run_algo(algo, out, n, THREADS[t], blocks[b]);
                tests++;
                if (!verify_results(ref, out, n)) {
                    printf("  [FAIL] algo=%d n=%d density=%.2f seed=%u threads=%d B=%d\n",
                           algo, n, densities[di], seed, THREADS[t], blocks[b]);
                    exit(1); // ponytail: process ends here, OS frees memory
                }
            }
        }
    }
    printf("  [PASS] %d/%d runs match the independent Bellman-Ford oracle exactly\n\n", tests, tests);
    free(g); free(ref); free(out);
}

// Cybersecurity demo: minimum-effort attack path on a small enterprise network.
// Edge weight = attacker effort to pivot u -> v (lower = easier; illustrative values inspired by CVSS exploitability).
#define NODES 8
int attack_path_demo(void) {
    const char *name[NODES] = {"Phished-PC", "Web-DMZ", "VPN-Gateway", "HR-Workstation",
                               "File-Server", "SQL-Database", "Jump-Host", "Domain-Controller"};
    int edges[][3] = {          // {from, to, effort}
        {0, 3, 2},              // Phished-PC     -> HR-Workstation (reused password)
        {0, 1, 6},              // Phished-PC     -> Web-DMZ
        {1, 5, 3},              // Web-DMZ        -> SQL-Database   (SQL injection)
        {2, 6, 4},              // VPN-Gateway    -> Jump-Host
        {3, 4, 3},              // HR-Workstation -> File-Server    (open SMB share)
        {3, 7, 12},             // HR-Workstation -> Domain-Controller (hard, direct)
        {4, 6, 2},              // File-Server    -> Jump-Host      (stored RDP creds)
        {5, 7, 9},              // SQL-Database   -> Domain-Controller
        {6, 7, 4},              // Jump-Host      -> Domain-Controller (admin session)
    };
    int g[NODES * NODES], d[NODES * NODES];
    for (int i = 0; i < NODES * NODES; i++) g[i] = (i / NODES == i % NODES) ? 0 : INF;
    for (int e = 0; e < 9; e++) g[edges[e][0] * NODES + edges[e][1]] = edges[e][2];
    memcpy(d, g, sizeof(g));
    floyd_warshall_parallel(d, NODES, 4);

    int src = 0, dst = 7, hops = 0, u = src;
    printf("  Minimum-effort attack path (effort %d):\n    %s", d[src * NODES + dst], name[u]);
    while (u != dst) {  // next hop v satisfies w(u,v) + dist(v,dst) == dist(u,dst)
        for (int v = 0; v < NODES; v++) {
            int w = g[u * NODES + v];
            if (v != u && w != INF && d[v * NODES + dst] != INF &&
                w + d[v * NODES + dst] == d[u * NODES + dst]) { u = v; break; }
        }
        printf(" -> %s", name[u]);
        hops++;
    }
    printf("\n  Blast radius from %s (effort <= 7):", name[src]);
    for (int v = 0; v < NODES; v++)
        if (v != src && d[src * NODES + v] <= 7) printf(" %s(%d)", name[v], d[src * NODES + v]);
    printf("\n");

    // Self-check against the hand-computed answer: 2 + 3 + 2 + 4 = 11 over 4 hops,
    // and VPN-Gateway has no incoming edge so it must stay unreachable.
    if (d[src * NODES + dst] != 11 || hops != 4 || d[src * NODES + 2] != INF) {
        printf("  [FAIL] attack-path demo gave a wrong answer\n");
        return 0;
    }
    printf("  [PASS] matches hand-computed answer\n\n");
    return 1;
}

static int cmp_double(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

// One timed run on a fresh copy of the graph; the result must equal ref (no fast-but-wrong timings)
double time_once(int algo, const int *base, int *work, const int *ref, int n, int threads, int bsize) {
    memcpy(work, base, (size_t)n * n * sizeof(int));
    double start = omp_get_wtime();
    run_algo(algo, work, n, threads, bsize);
    double t = omp_get_wtime() - start;
    if (!verify_results(ref, work, n)) {
        printf("  [FAIL] wrong result: algo=%d n=%d threads=%d B=%d\n", algo, n, threads, bsize);
        exit(1);
    }
    return t;
}

double median(double *t, int k) {
    qsort(t, k, sizeof(double), cmp_double);
    return t[k / 2];
}

// Print one result row and append it to the CSV.
// Parallel overhead  T_o = p * T_p - T_seq   (time spent not doing useful work)
// Karp-Flatt metric  e   = (1/speedup - 1/p) / (1 - 1/p)   (measured serial fraction, p > 1)
void report_row(FILE *csv, int n, const char *name, int th, double t, double t_seq) {
    double speedup = t_seq / t;
    double efficiency = (speedup / th) * 100.0;
    double overhead = th * t - t_seq;
    double karp_flatt = (th > 1) ? (1.0 / speedup - 1.0 / th) / (1.0 - 1.0 / th) : 0.0;
    char sp_buf[16], eff_buf[16];
    snprintf(sp_buf, sizeof(sp_buf), "%.2fx", speedup);
    snprintf(eff_buf, sizeof(eff_buf), "%.1f%%", efficiency);
    printf("%-8d %-20s %-8d %-12.4f %-9s %-11s %-12.4f %.4f\n", n, name, th, t, sp_buf, eff_buf, overhead, karp_flatt);
    fprintf(csv, "%d,%s,%d,%.5f,%.4f,%.2f,%.5f,%.4f\n", n, name, th, t, speedup, efficiency, overhead, karp_flatt);
}

int main(int argc, char *argv[]) {
    printf("======================================================================\n");
    printf("  NED University of Engineering & Technology - CIS Department\n");
    printf("  PDC Complex Computing Problem: Floyd-Warshall Optimization Benchmarks\n");
    printf("  Students: Ameem Akhtar (CR-23013), Minhal Rizvi (CR-23017)\n");
    printf("            Muhammad Usman (CR-23038), Maaz Wasim (CR-23041)\n");
    printf("======================================================================\n\n");

    printf("[1/3] Correctness: all implementations vs independent Bellman-Ford oracle...\n");
    run_correctness_tests();

    printf("[2/3] Cybersecurity application: attack-graph analysis...\n");
    if (!attack_path_demo()) return 1;

    if (argc > 1 && strcmp(argv[1], "--quick") == 0) return 0; // tests + demo only

    int sizes[] = {500, 1000, 1500, 2000};
    int block_sizes[] = {16, 32, 64, 128, 256};

    FILE *f_csv = fopen("benchmark_results.csv", "w");
    FILE *f_blk = fopen("block_size_results.csv", "w");
    if (!f_csv || !f_blk) {
        perror("Failed to open CSV output");
        return 1;
    }
    fprintf(f_csv, "Size,Implementation,Threads,ExecutionTime_Sec,Speedup,Efficiency_Pct,Overhead_Sec,KarpFlatt\n");
    fprintf(f_blk, "Size,BlockSize,Threads,ExecutionTime_Sec,Speedup\n");

    printf("[3/3] Scalability benchmarks (median of %d round-robin runs, every result verified)...\n", RUNS);
    printf("%-8s %-20s %-8s %-12s %-9s %-11s %-12s %s\n", "Vertices", "Algorithm", "Threads", "Time (sec)", "Speedup", "Efficiency", "Overhead(s)", "Karp-Flatt");
    printf("--------------------------------------------------------------------------------------------\n");

    for (int s = 0; s < 4; s++) {
        int n = sizes[s];
        size_t bytes = (size_t)n * n * sizeof(int);
        int *base_graph = malloc(bytes), *work_graph = malloc(bytes), *ref = malloc(bytes);
        initialize_graph(base_graph, n, 0.40, 100 + s);

        // Untimed sequential run: gives the reference result and warms up the CPU and caches
        memcpy(ref, base_graph, bytes);
        floyd_warshall_sequential(ref, n);

        // Configurations in table order: sequential, standard x threads,
        // blocked x threads, then the block-size study (8 threads, B varied)
        int algo[NC], th[NC], bs[NC], c = 0;
        algo[c] = 0; th[c] = 1; bs[c++] = 0;
        for (int t = 0; t < NUM_THREADS; t++) { algo[c] = 1; th[c] = THREADS[t]; bs[c++] = 0; }
        for (int t = 0; t < NUM_THREADS; t++) { algo[c] = 2; th[c] = THREADS[t]; bs[c++] = BLOCK_SIZE; }
        for (int b = 0; b < 5; b++) { algo[c] = 2; th[c] = 8; bs[c++] = block_sizes[b]; }

        // Round-robin: each round times every configuration once, so slow drift in CPU
        // clock speed (turbo, temperature, power plan) affects all of them equally
        double times[NC][RUNS], med[NC];
        for (int r = 0; r < RUNS; r++)
            for (int i = 0; i < NC; i++)
                times[i][r] = time_once(algo[i], base_graph, work_graph, ref, n, th[i], bs[i]);
        for (int i = 0; i < NC; i++) med[i] = median(times[i], RUNS);

        double t_seq = med[0];
        report_row(f_csv, n, "Sequential", 1, t_seq, t_seq);
        for (int i = 1; i < NC - 5; i++)
            report_row(f_csv, n, algo[i] == 1 ? "OpenMP-Standard" : "OpenMP-Blocked", th[i], med[i], t_seq);
        for (int i = NC - 5; i < NC; i++) {
            char label[24];
            snprintf(label, sizeof(label), "Blocked B=%d", bs[i]);
            printf("%-8d %-20s %-8d %-12.4f %.2fx\n", n, label, 8, med[i], t_seq / med[i]);
            fprintf(f_blk, "%d,%d,8,%.5f,%.4f\n", n, bs[i], med[i], t_seq / med[i]);
        }
        printf("--------------------------------------------------------------------------------------------\n");

        free(base_graph);
        free(work_graph);
        free(ref);
    }

    fclose(f_csv);
    fclose(f_blk);
    printf("\nDone. Data exported to benchmark_results.csv and block_size_results.csv\n");
    return 0;
}
