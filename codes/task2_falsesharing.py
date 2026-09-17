import threading
import time

ITERATIONS = 5_000_000


def worker_adjacent(shared_list, index):
    for _ in range(ITERATIONS):
        shared_list[index] += 1


def worker_padded(shared_list, index):
    # Offset by 16 integers (16 * 8 bytes = 128 bytes > 64-byte cache line)
    padded_idx = index * 16
    for _ in range(ITERATIONS):
        shared_list[padded_idx] += 1


def run_test(target_fn, size):
    arr = [0] * size
    threads = [threading.Thread(target=target_fn, args=(arr, i)) for i in range(4)]
    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    return time.perf_counter() - start


if __name__ == '__main__':
    # Запускаем по 3 раза для каждого варианта, чтобы зафиксировать триалы
    print("Running Adjacent (False Sharing)...")
    t_adj_trials = [run_test(worker_adjacent, size=4) for _ in range(3)]

    print("Running Padded (Cache-Aligned)...")
    t_pad_trials = [run_test(worker_padded, size=64) for _ in range(3)]

    med_adj = sorted(t_adj_trials)[1]
    med_pad = sorted(t_pad_trials)[1]

    print(f"Adjacent Trials: {t_adj_trials} | Median: {med_adj:.4f}s")
    print(f"Padded Trials: {t_pad_trials} | Median: {med_pad:.4f}s")
    print(f"Slowdown Factor: {med_adj / med_pad:.2f}x")