import unittest
from src.organizer.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    
    def setUp(self):
        self.scheduler = Scheduler()

    def test_daily_cleanup(self):
        self.scheduler.schedule_daily_cleanup()
        self.assertTrue(self.scheduler.is_cleanup_scheduled)

    def test_manual_cleanup(self):
        self.scheduler.trigger_manual_cleanup()
        self.assertTrue(self.scheduler.cleanup_triggered)

    def test_cleanup_time_setting(self):
        self.scheduler.set_cleanup_time("02:00")
        self.assertEqual(self.scheduler.cleanup_time, "02:00")

if __name__ == '__main__':
    unittest.main()