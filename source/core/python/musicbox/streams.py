# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys


class PrefixedStream():

    def __init__(self, stream, prefix):
        self.stream = stream
        self.prefix = prefix

    def write(self, text):
        self.stream.write(self.prefix + text)

    def flush(self):
        self.stream.flush()


class OutputStreamGroup():

    def __init__(self, streams):
        self.streams = streams

    def add_stream(self, stream):
        self.streams.append(stream)

    def write(self, text):
        for stream in self.streams:
            stream.write(text)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def ensure_init():
    if not isinstance(sys.stdout, OutputStreamGroup):
        sys.stdout = OutputStreamGroup([PrefixedStream(sys.stdout, "(Python stdout) ")])
    if not isinstance(sys.stderr, OutputStreamGroup):
        sys.stderr = OutputStreamGroup([PrefixedStream(sys.stderr, "(Python stderr) ")])
