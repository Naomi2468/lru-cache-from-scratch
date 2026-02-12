# LRU Cache from Scratch (O(1) Get/Put)

This repository implements an **LRU (Least Recently Used) cache** from scratch in Python.

## Why LRU?
LRU is a classic caching strategy used in systems such as:
- web caches
- database buffer pools
- OS page replacement
- application-level memoization

## Core Idea (Data Structures)
To achieve **O(1)** average-time operations, we combine:

1. **Hash Map (dict)**: `key -> node`  
   - O(1) average lookup by key

2. **Doubly Linked List** (recency order)  
   - Most Recently Used (MRU) near the head  
   - Least Recently Used (LRU) near the tail  
   - O(1) remove/insert when updating recency

## Complexity (Why O(1))
- `get(key)`:
  - dict lookup: O(1) average
  - move node to MRU: O(1) pointer updates
- `put(key, value)`:
  - dict lookup/insert: O(1) average
  - insert/move node in list: O(1)
  - eviction (if needed): remove tail node: O(1)
- `delete(key)`:
  - dict remove: O(1) average
  - list remove: O(1)

✅ Therefore, each operation is **O(1) average time**.

## Project Files
- `lru_cache.py` — main implementation
- `test_lru_cache.py` — unit tests
- `benchmark.py` — simple performance benchmark

## Run Tests
```bash
python test_lru_cache.py

## Run Benchmark
python benchmark.py

## Example Benchmark Output
ops=300,000 capacity=20,000 key_space=80,000 get_ratio=0.70
time=0.233s  ops/sec=1,289,344
final cache size=20,000


