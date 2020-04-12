from abc import ABC, abstractmethod


class Task(ABC):
    # Content of this task
    @abstractmethod
    def run(self):
        raise NotImplementedError()
