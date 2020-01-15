import datetime


class Teapot:
    def __init__(self, seconds):
        self.seconds = seconds
        self.is_currently_brewing = False
        self.start_time = None
        self.additions = None

    def is_busy(self):
        if self.is_currently_brewing and self._when() < datetime.datetime.now():
            self._stop()
        return self.is_currently_brewing

    def _start(self, additions):
        self.start_time = datetime.datetime.now()
        self.is_currently_brewing = True
        self.additions = additions

    def brew_start(self, additions = None):
        if self.is_busy():
            return 503
        self._start(additions)
        return 202

    def _stop(self):
        self.start_time = None
        self.is_currently_brewing = False
        self.additions = None

    def brew_stop(self):
        if not self.is_busy():
            return 400
        self._stop()
        return 201

    def _when(self):
        return self.start_time + datetime.timedelta(seconds=self.seconds)

    def when(self):
        if self.is_busy():
            return self._when()
        return None
