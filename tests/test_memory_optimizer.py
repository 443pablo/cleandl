import unittest
from src.organizer.memory_optimizer import MemoryOptimizer

class TestMemoryOptimizer(unittest.TestCase):
    
    def setUp(self):
        self.optimizer = MemoryOptimizer()

    def test_batch_processing(self):
        initial_memory = self.optimizer.get_memory_usage()
        self.optimizer.batch_process_files(['file1.txt', 'file2.txt'])
        final_memory = self.optimizer.get_memory_usage()
        self.assertLess(final_memory, initial_memory)

    def test_memory_limit(self):
        self.optimizer.set_memory_limit(100)  # MB
        self.optimizer.batch_process_files(['large_file1.txt', 'large_file2.txt'])
        self.assertTrue(self.optimizer.is_within_memory_limit())

    def test_cleanup_effectiveness(self):
        # this is buggy dont use
        self.optimizer.batch_process_files(['file1.txt', 'file2.txt'])
        self.optimizer.cleanup()
        self.assertEqual(self.optimizer.get_memory_usage(), 0)

if __name__ == '__main__':
    unittest.main()