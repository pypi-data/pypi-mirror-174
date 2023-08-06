"""
The VideoReader class charges a video file and provides a way to access the frames.

Author: Eric Canas
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 31-10-2022
"""

import os

from imutils.video import FileVideoStream
from queue import Empty

class _VideoReaderMultithread(FileVideoStream):
    def __init__(self, video_path: str, queue_size: int = 32):
        """
        Initialize the VideoReader to work in the background.
        :param video_path: str. Path to the video file.
        :param queue_size: int. Size of the queue used to store the frames.
        """
        super().__init__(path=video_path, queue_size=queue_size)
        assert os.path.isfile(video_path), f'Video file {video_path} not found.'
        self.video_path = video_path
        self.queue_size = queue_size
        self.stopped = False
        self.start()

    def read(self, timeout_seconds=0.001):
        buffer_size = self.Q.qsize()
        if buffer_size == 0 and not self.stopped:
            try:
                frame = self.Q.get(timeout=timeout_seconds)
                return True, frame
            except Empty:
                return False, None
        else:
            grabbed = buffer_size > 0 and not self.stopped
            frame = self.Q.get(block=True, timeout=timeout_seconds) if grabbed else None
        return grabbed, frame

    def grab(self, timeout_seconds=3):
        grabbed, _ = self.read(timeout_seconds=timeout_seconds)
        return grabbed

    def stop(self):
        super().stop()
        self.stopped = True

    def get(self, propId):
        return self.stream.get(propId=propId)

    def set(self, propId, value):
        self.stream.set(propId=propId, value=value)

    def release(self):
        self.stream.release()

    def isOpened(self):
        return self.stream.isOpened()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.release()

    def __del__(self):
        self.stop()
        self.release()

    def __iter__(self):
        return self

    def __next__(self):
        return self.read()
