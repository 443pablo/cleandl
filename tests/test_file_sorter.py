import os
import unittest
from organizer.file_sorter import FileSorter

class TestFileSorter(unittest.TestCase):
    
    def setUp(self):
        self.file_sorter = FileSorter()
        self.test_directory = 'test_downloads'
        os.makedirs(self.test_directory, exist_ok=True)

    def tearDown(self):
        for filename in os.listdir(self.test_directory):
            file_path = os.path.join(self.test_directory, filename)
            os.remove(file_path)
        os.rmdir(self.test_directory)

    def test_sort_files(self):
        
        with open(os.path.join(self.test_directory, 'test1.txt'), 'w') as f:
            f.write('test')
        with open(os.path.join(self.test_directory, 'test2.jpg'), 'w') as f:
            f.write('test')
        
        self.file_sorter.sort_files(self.test_directory)

        self.assertTrue(os.path.exists(os.path.join(self.test_directory, 'TextFiles/test1.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.test_directory, 'Images/test2.jpg')))

    def test_empty_directory(self):
        result = self.file_sorter.sort_files(self.test_directory)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()