import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 13

df = pd.read_csv('benchmark_results.csv')
print(df)

# Plot 1: Execution Time vs Matrix Size (Vertices)
plt.figure(figsize=(8, 5), dpi=300)
sizes = sorted(df['Size'].unique())

# Sequential
seq_times = df[df['Implementation'] == 'Sequential']['ExecutionTime_Sec'].values
plt.plot(sizes, seq_times, marker='o', linewidth=2, color='#c0392b', label='Sequential (1 thread)')

# OpenMP 2 threads
t2_times = df[(df['Implementation'] == 'OpenMP-Standard') & (df['Threads'] == 2)]['ExecutionTime_Sec'].values
plt.plot(sizes, t2_times, marker='s', linewidth=2, color='#e67e22', label='OpenMP Parallel (2 threads)')

# OpenMP 4 threads
t4_times = df[(df['Implementation'] == 'OpenMP-Standard') & (df['Threads'] == 4)]['ExecutionTime_Sec'].values
plt.plot(sizes, t4_times, marker='^', linewidth=2, color='#2980b9', label='OpenMP Parallel (4 threads)')

# OpenMP 8 threads
t8_times = df[(df['Implementation'] == 'OpenMP-Standard') & (df['Threads'] == 8)]['ExecutionTime_Sec'].values
plt.plot(sizes, t8_times, marker='D', linewidth=2, color='#27ae60', label='OpenMP Parallel (8 threads)')

# Blocked OpenMP 8 threads
blk_times = df[(df['Implementation'] == 'OpenMP-Blocked') & (df['Threads'] == 8)]['ExecutionTime_Sec'].values
if len(blk_times) > 0:
    plt.plot(sizes, blk_times, marker='*', markersize=10, linewidth=2.5, linestyle='--', color='#8e44ad', label='Cache-Blocked OpenMP (8 threads)')

plt.title('Floyd-Warshall Execution Time vs Graph Size (V)', fontweight='bold', pad=12)
plt.xlabel('Number of Vertices (V)')
plt.ylabel('Execution Time (seconds)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(frameon=True, facecolor='#f8f9fa', framealpha=0.9)
plt.tight_layout()
plt.savefig('runtime_comparison.png')
plt.close()
print("Generated runtime_comparison.png")

# Plot 2: Speedup vs Thread Count
plt.figure(figsize=(8, 5), dpi=300)
threads = [1, 2, 4, 8]
plt.plot(threads, threads, 'k--', label='Ideal Linear Speedup ($S = p$)', alpha=0.7)

for size in [500, 1000, 1500, 2000]:
    sub = df[(df['Size'] == size) & (df['Implementation'] == 'OpenMP-Standard')]
    if not sub.empty:
        plt.plot(sub['Threads'], sub['Speedup'], marker='o', linewidth=2, label=f'V = {size}')

plt.title('Speedup Analysis Across Thread Counts ($S = T_1 / T_p$)', fontweight='bold', pad=12)
plt.xlabel('Number of Threads (p)')
plt.ylabel('Speedup Factor')
plt.xticks(threads)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(frameon=True, facecolor='#f8f9fa', framealpha=0.9)
plt.tight_layout()
plt.savefig('speedup_analysis.png')
plt.close()
print("Generated speedup_analysis.png")

# Plot 3: Parallel Efficiency vs Thread Count
plt.figure(figsize=(8, 5), dpi=300)
for size in [500, 1000, 1500, 2000]:
    sub = df[(df['Size'] == size) & (df['Implementation'] == 'OpenMP-Standard')]
    if not sub.empty:
        plt.plot(sub['Threads'], sub['Efficiency_Pct'], marker='s', linewidth=2, label=f'V = {size}')

plt.axhline(100, color='gray', linestyle=':', label='100% Ideal Efficiency')
plt.title('Parallel Efficiency vs Thread Count ($E = S / p \\times 100\\%$)', fontweight='bold', pad=12)
plt.xlabel('Number of Threads (p)')
plt.ylabel('Efficiency (%)')
plt.xticks(threads)
plt.ylim(0, 110)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(frameon=True, facecolor='#f8f9fa', framealpha=0.9)
plt.tight_layout()
plt.savefig('efficiency_plot.png')
plt.close()
print("Generated efficiency_plot.png")

# Plot 4: Standard OpenMP vs Blocked OpenMP Performance
plt.figure(figsize=(8, 5), dpi=300)
bar_width = 0.35
indices = np.arange(len(sizes))

std_8 = df[(df['Implementation'] == 'OpenMP-Standard') & (df['Threads'] == 8)]['ExecutionTime_Sec'].values
blk_8 = df[(df['Implementation'] == 'OpenMP-Blocked') & (df['Threads'] == 8)]['ExecutionTime_Sec'].values

plt.bar(indices - bar_width/2, std_8, bar_width, label='Standard OpenMP (8 threads)', color='#3498db', edgecolor='black', linewidth=0.5)
plt.bar(indices + bar_width/2, blk_8, bar_width, label='Blocked OpenMP (8 threads, B=64)', color='#9b59b6', edgecolor='black', linewidth=0.5)

plt.title('Standard OpenMP vs Cache-Blocked OpenMP (8 Threads)', fontweight='bold', pad=12)
plt.xlabel('Number of Vertices (V)')
plt.ylabel('Execution Time (seconds)')
plt.xticks(indices, [f'V={s}' for s in sizes])
plt.grid(True, linestyle='--', alpha=0.6, axis='y')
plt.legend(frameon=True, facecolor='#f8f9fa', framealpha=0.9)
plt.tight_layout()
plt.savefig('cache_blocking_comparison.png')
plt.close()
print("Generated cache_blocking_comparison.png")
