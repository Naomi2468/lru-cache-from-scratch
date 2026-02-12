import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_put_get(self):
        c = LRUCache(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        self.assertEqual(c.get("a"), 1)
        self.assertEqual(c.get("b"), 2)

    def test_eviction(self):
        c = LRUCache(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)  # evict a
        self.assertIsNone(c.get("a"))
        self.assertEqual(c.get("b"), 2)
        self.assertEqual(c.get("c"), 3)

    def test_get_updates_recency(self):
        c = LRUCache(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        _ = c.get("a")  # a becomes MRU, b becomes LRU
        c.put("c", 3)   # should evict b
        self.assertIsNone(c.get("b"))
        self.assertEqual(c.get("a"), 1)
        self.assertEqual(c.get("c"), 3)

    def test_put_updates_value_and_recency(self):
        c = LRUCache(capacity=2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("a", 10)  # update + move a to MRU
        c.put("c", 3)   # evict b
        self.assertEqual(c.get("a"), 10)
        self.assertIsNone(c.get("b"))
        self.assertEqual(c.get("c"), 3)

    def test_delete(self):
        c = LRUCache(capacity=2)
        c.put("a", 1)
        self.assertTrue(c.delete("a"))
        self.assertFalse(c.delete("a"))
        self.assertIsNone(c.get("a"))

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(0)
        with self.assertRaises(ValueError):
            LRUCache(-5)


if __name__ == "__main__":
    unittest.main()

