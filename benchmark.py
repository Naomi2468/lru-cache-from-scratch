import random
import time
from lru_cache import LRUCache


def run_benchmark(n_ops=300_000, capacity=20_000, key_space=80_000, get_ratio=0.7):
    cache = LRUCache(capacity=capacity)
    keys = [random.randint(1, key_space) for _ in range(n_ops)]
    ops = [random.random() for _ in range(n_ops)]

    t0 = time.perf_counter()
    for i in range(n_ops):
        k = keys[i]
        if ops[i] < get_ratio:
            cache.get(k)
        else:
            cache.put(k, i)
    t1 = time.perf_counter()

    elapsed = t1 - t0
    print("LRU Cache Benchmark")
    print(f"ops={n_ops:,} capacity={capacity:,} key_space={key_space:,} get_ratio={get_ratio:.2f}")
    print(f"time={elapsed:.3f}s  ops/sec={n_ops/elapsed:,.0f}")
    print(f"final cache size={len(cache):,}")


if __name__ == "__main__":
    random.seed(42)
    run_benchmark()

