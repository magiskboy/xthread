import time
import unittest
from unittest import mock
from xthread import Thread


WAIT_TIME = 0.1


class ThreadTestCase(unittest.TestCase):
    def test_thread_running(self):
        target = mock.Mock(return_value=42)
        on_result = mock.Mock()
        thread = Thread(target=target, on_result=on_result)
        time.sleep(WAIT_TIME)

        self.assertTrue(thread.is_active)
        self.assertTrue(thread.is_running)
        self.assertFalse(thread.is_paused)

        thread.pause()
        self.assertTrue(thread.is_active)
        self.assertTrue(thread.is_paused)
        self.assertFalse(thread.is_running)

        thread.stop()
        self.assertFalse(thread.is_active)
        self.assertFalse(thread.is_running)
        self.assertFalse(thread.is_paused)

        target.assert_called_with(thread)
        on_result.assert_called_with(42)

    def test_without_error_handler(self):
        error = ValueError()
        target = mock.Mock(side_effect=error)

        thread = Thread(target=target)
        time.sleep(WAIT_TIME)
        thread.stop()


    def test_catch_error(self):
        error = ValueError()
        target = mock.Mock(side_effect=error)
        error_handler = mock.Mock()

        thread = Thread(target=target, on_error=error_handler)
        time.sleep(WAIT_TIME)
        thread.stop()

        error_handler.assert_called_with(error)

    def test_pause_unpause(self):
        target = mock.Mock()
        pause_handler = mock.Mock()
        unpause_handler = mock.Mock()

        thread = Thread(
            target=target,
            on_paused=pause_handler,
            on_unpaused=unpause_handler,
        )
        time.sleep(WAIT_TIME)
        thread.pause()
        thread.unpause()

        pause_handler.assert_called_with(thread)
        unpause_handler.assert_called_with(thread)

    def test_start_stop(self):
        target = mock.Mock()
        stopped_handler = mock.Mock()
        started_handler = mock.Mock()

        thread = Thread(
            target=target,
            on_stopped=stopped_handler,
            on_started=started_handler,
            autostart=True,
        )
        time.sleep(WAIT_TIME)
        thread.stop()
        time.sleep(WAIT_TIME)

        started_handler.assert_called_with(thread)
        stopped_handler.assert_called_with(thread)


if __name__ == '__main__':
    unittest.main()
