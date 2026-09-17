import time
import multiprocessing as mp
import numpy as np

def compute_heavy(n):
    x = 1.0001
    for _ in range(n):
        x = (x * 1.000001) + 0.00001
    return x

def memory_heavy(size):
    arr = np.ones(size, dtype=np.float64)
    arr = arr * 2.0 + 1.0
    return arr[0]

if __name__ == '__main__':
    print("=== Compute-Bound Suite (Register Math) ===")
    t1_comp = 0
    for w in [1, 2, 4]:
        t0 = time.perf_counter()
        with mp.Pool(w) as p:
            p.map(compute_heavy, [25_000_000] * w)
        elapsed = time.perf_counter() - t0
        if w == 1: t1_comp = elapsed
        print(f"Workers: {w} | Time: {elapsed:.4f}s | Scaling: {elapsed/t1_comp:.2f}x")

    print("\n=== Memory-Bound Suite (DRAM Bandwidth Saturation) ===")
    t1_mem = 0
    for w in [1, 2, 4]:
        t0 = time.perf_counter()
        with mp.Pool(w) as p:
            p.map(memory_heavy, [50_000_000] * w)
        elapsed = time.perf_counter() - t0
        if w == 1: t1_mem = elapsed
        print(f"Workers: {w} | Time: {elapsed:.4f}s | Degradation: {elapsed/t1_mem:.2f}x")