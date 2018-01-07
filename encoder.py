#!/usr/bin/env python

"""
Process rarfile containing video and transcode to iPhone compatible AVC/H.264
"""

from argparse import ArgumentParser
from contextlib import contextmanager
import functools
import rarfile
import subprocess
from pprint import pprint
import os
import tempfile


class VideoReader(object):
    def __init__(self):
        pass

    def __call__(self):
        raise NotImplementedError

    def video_filename(self):
        raise NotImplementedError

    def is_stream(self):
        return True

    @classmethod
    def create(cls, filename, *args, **kwargs):

        if filename.lower().endswith('.rar'):
            return RarTempVideoReader(filename, *args, **kwargs)
        elif cls.is_video_filename(filename):
            return FileVideoReader(filename, *args, **kwargs)
        else:
            raise ValueError('No reader defined', filename)

    @staticmethod
    def is_video_filename(filename):
        video_file_extensions = [
            'm4v',
            'mp4',
            'wmv',
            'avi',
            'mpg',
        ]
        return filename.lower().split('.')[-1] in video_file_extensions    


class FileVideoReader(VideoReader):
    def __init__(self, filename):
        self.filename = filename

    def __call__(self):
        return open(self.filename, mode='rb')

    def video_filename(self):
        return self.filename


class RarVideoReader(VideoReader):
    def __init__(self, filename):
        self.rarfile = rarfile.RarFile(filename)

    def __call__(self):
        return self.rarfile.open(self.video_filename())

    def video_filename(self):
        for info in self.rarfile.infolist():
            if self.is_video_filename(info.filename):
                return info.filename
        raise ValueError('no video file found')


class RarTempVideoReader(VideoReader):
    def __init__(self, filename):
        self.rarfile = rarfile.RarFile(filename)
        self.temp_filename = None

    @contextmanager
    def __call__(self):
        # This does seem a bit bogus
        try:
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file, self.rarfile.open(self.video_filename()) as video_file:
                self.temp_filename = temp_file.name
                for block in iter(functools.partial(video_file.read, 65536), ''):
                    temp_file.write(block)
            yield self.temp_filename
        finally:
            os.unlink(self.temp_filename)

    def video_filename(self):
        for info in self.rarfile.infolist():
            if self.is_video_filename(info.filename):
                return info.filename
        raise ValueError('no video file found')

    def input_filename(self):
        return self.temp_filename

    def is_stream(self):
        return False


class VideoEncoder(object):
    FFMPEG_EXE = 'C:\\Users\\test\\Desktop\\ffmpeg\\bin\\ffmpeg.exe'

    FFMPEG_ARGS = [
        '-f', 'mp4',
        '-preset', 'veryfast',
        '-tune', 'film',
        '-profile:v', 'high',
        '-level', '4.2',
        '-c:v', 'h264',
        '-c:a', 'aac',
        '-crf', '23',
        '-movflags', '+faststart'
    ]

    def __init__(self, reader, output, scale=None):
        self.reader = reader
        self.output = output
        self.extra_ffmpeg_args = []
        if scale:
            self.extra_ffmpeg_args += ['-vf', 'scale=' + scale]

    def output_filename(self):
        video_filename = '.'.join(os.path.basename(self.reader.video_filename()).split('.')[:-1]) + '.mp4'
        return os.path.join(self.output, video_filename)

    def encoding_command(self):
        return (
            [self.FFMPEG_EXE, '-i', self.reader.input_filename() if not self.reader.is_stream() else '-'] + 
            self.FFMPEG_ARGS + 
            self.extra_ffmpeg_args +
            [self.output_filename()]
        )

    def encode(self):
        if self.reader.is_stream():
            with self.reader() as infile:
                process = subprocess.Popen(self.encoding_command(), stdin=subprocess.PIPE)
                for block in iter(functools.partial(infile.read, 65536), ''):
                    process.stdin.write(block)
                process.stdin.close()
            return process.wait()
        else:
            with self.reader() as infile:
                subprocess.check_call(self.encoding_command())


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='+', help="Input files")
    parser.add_argument('-o', '--output', required=True, help="Output path")
    parser.add_argument('-s', '--scale')
    args = parser.parse_args()
    
    for input_filename in args.input:
        VideoEncoder(VideoReader.create(input_filename), args.output, scale=args.scale).encode()

if __name__ == "__main__":
    main()
