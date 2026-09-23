"""Runtime instrumentation used by the playground grader."""


class TrackedSequence:
    """A minimal mutable sequence that records how student code touches it.

    The object behaves sufficiently like a Python sequence for the List 01
    tasks, while exposing counters controlled by the grader.
    """

    def __init__(self, values):
        self._data = list(values)
        self.reads = 0
        self.writes = 0
        self.slice_reads = 0
        self.iter_starts = 0

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        if isinstance(key, slice):
            self.slice_reads += 1
            result = self._data[key]
            self.reads += len(result)
            return result

        self.reads += 1
        return self._data[key]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise TypeError("slice writes are intentionally unsupported")
        self.writes += 1
        self._data[key] = value

    def __iter__(self):
        self.iter_starts += 1
        for value in self._data:
            self.reads += 1
            yield value

    def snapshot(self):
        return list(self._data)

    def reset_counters(self):
        self.reads = 0
        self.writes = 0
        self.slice_reads = 0
        self.iter_starts = 0
