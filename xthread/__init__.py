from typing import Callable, Optional, Any
import threading

__version__ = "0.0.2"


class Thread:
    """Thread API supports some features such as pause/unpause
    and terminate non-preemtively
    """

    def __init__(
        self,
        target: Callable[["Thread"], Any], 
        args = None, 
        kwargs = None, 
        on_result: Optional[Callable[[Any], Any]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        on_paused: Optional[Callable[["Thread"], None]] = None,
        on_unpaused: Optional[Callable[["Thread"], None]] = None,
        on_started: Optional[Callable[["Thread"], None]] = None,
        on_stopped: Optional[Callable[["Thread"], None]] = None,
        autostart: Optional[bool] = True,
        pause_timeout: Optional[float] = None,
    ):
        self.__on_paused = on_paused
        self.__on_unpaused = on_unpaused
        self.__on_started = on_started
        self.__on_stopped = on_stopped
        self.__on_error = on_error
        self.__on_result = on_result

        self.__pause_timeout = pause_timeout

        self.__is_running = threading.Event() 

        self.__resume = threading.Event()
        self.__resume.set()

        execution = self.__cycle_execution(target, args, kwargs)
        self.__thread = threading.Thread(target=execution, daemon=True)

        if autostart:
            self.start()

    def start(self):
        self.__is_running.set()
        self.__thread.start()
        
        if self.__on_started:
            self.__on_started(self)

    def stop(self):
        self.__is_running.clear()

    def pause(self):
        self.__resume.clear()

        if self.__on_paused:
            self.__on_paused(self)

    def unpause(self):
        self.__resume.set()

        if self.__on_unpaused:
            self.__on_unpaused(self)

    @property
    def is_active(self):
        return self.__is_running.is_set()

    @property
    def is_paused(self):
        return self.is_active and not self.__resume.is_set()

    @property
    def is_running(self):
        return self.is_active and not self.is_paused

    def __cycle_execution(self, target, args=None, kwargs=None):
        args = args or tuple()
        kwargs = kwargs or dict()

        def wrapper():
            while self.__is_running.is_set():
                try:
                    result = target(self, *args, **kwargs)
                    self.__resume.wait(self.__pause_timeout)

                except Exception as e:
                    if self.__on_error:
                        self.__on_error(e)
                    else:
                        raise e

                else:
                    if self.__on_result:
                        self.__on_result(result)

            if self.__on_stopped:
                self.__on_stopped(self)

        return wrapper    

