from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Generic, Iterator, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _Node(Generic[K, V]):
    key: K
    value: V
    prev: Optional["_Node[K, V]"] = None
    next: Optional["_Node[K, V]"] = None


class LRUCache(Generic[K, V]):
    """
    LRU Cache (Least Recently Used) implemented from scratch.

    Data structures:
      - dict: key -> node (O(1) average lookup)
      - doubly linked list: MRU near head, LRU near tail (O(1) reordering)

    Operations:
      - get(key): O(1) average
      - put(key, value): O(1) average
      - delete(key): O(1) average
    """

    def __init__(self, capacity: int):
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self._map: Dict[K, _Node[K, V]] = {}

        # Sentinel nodes to simplify edge cases
        self._head: _Node = _Node(key=None, value=None)  # type: ignore[arg-type]
        self._tail: _Node = _Node(key=None, value=None)  # type: ignore[arg-type]
        self._head.next = self._tail
        self._tail.prev = self._head

    def __len__(self) -> int:
        return len(self._map)

    def _add_after_head(self, node: _Node[K, V]) -> None:
        """Insert node right after head (MRU position)."""
        first = self._head.next
        node.prev = self._head
        node.next = first
        self._head.next = node
        if first is not None:
            first.prev = node

    def _remove_node(self, node: _Node[K, V]) -> None:
        """Detach node from linked list."""
        prev = node.prev
        nxt = node.next
        if prev is not None:
            prev.next = nxt
        if nxt is not None:
            nxt.prev = prev
        node.prev = None
        node.next = None

    def _move_to_mru(self, node: _Node[K, V]) -> None:
        """Mark existing node as most-recently used."""
        self._remove_node(node)
        self._add_after_head(node)

    def _pop_lru(self) -> Optional[_Node[K, V]]:
        """Remove and return least-recently used node."""
        lru = self._tail.prev
        if lru is None or lru is self._head:
            return None
        self._remove_node(lru)
        return lru

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        node = self._map.get(key)
        if node is None:
            return default
        self._move_to_mru(node)
        return node.value

    def put(self, key: K, value: V) -> None:
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._move_to_mru(node)
            return

        new_node = _Node(key=key, value=value)
        self._map[key] = new_node
        self._add_after_head(new_node)

        if len(self._map) > self.capacity:
            lru = self._pop_lru()
            if lru is not None:
                self._map.pop(lru.key, None)

    def delete(self, key: K) -> bool:
        node = self._map.pop(key, None)
        if node is None:
            return False
        self._remove_node(node)
        return True

    def peek_lru(self) -> Optional[Tuple[K, V]]:
        """Return LRU (key, value) without changing order."""
        node = self._tail.prev
        if node is None or node is self._head:
            return None
        return (node.key, node.value)

    def items_mru_to_lru(self) -> Iterator[Tuple[K, V]]:
        cur = self._head.next
        while cur is not None and cur is not self._tail:
            yield (cur.key, cur.value)
            cur = cur.next

