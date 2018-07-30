#!/usr/bin/env python

"""
Process file containing video and transcode to iPhone compatible AVC/H.264
"""

from argparse import ArgumentParser
from contextlib import contextmanager
import functools
import logging
import rarfile
import subprocess
import os
import tempfile


# TODO: 
# Refactor VideoReader/Encoder to only use on-disk files
# Create 

LOG = logging.getLogger(__name__)


class VideoReader(object):
    def __init__(self):
        pass

    def __call__(self):
        raise NotImplementedError

    def video_filename(self):
        raise NotImplementedError

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

    def input_args(self):
        return []


class FileVideoReader(VideoReader):
    def __init__(self, filename):
        self.filename = filename

    @contextmanager
    def __call__(self):
        # return open(self.filename, mode='rb')
        yield self.filename

    def video_filename(self):
        return self.filename


class RarTempVideoReader(VideoReader):
    def __init__(self, filename):
        self.rarfile = rarfile.RarFile(filename)

    @contextmanager
    def __call__(self):
        tempfile_name = None
        try:
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file, self.rarfile.open(self.video_filename()) as video_file:
                tempfile_name = temp_file.name
                for block in iter(functools.partial(video_file.read, 65536), b''):
                    temp_file.write(block)
            # Yield outside the context manager, because Windows concurrent file access 
            yield tempfile_name
        finally:
            os.unlink(tempfile_name)

    def video_filename(self):
        for info in self.rarfile.infolist():
            if self.is_video_filename(info.filename):
                return info.filename
        raise ValueError('no video file found')


@contextmanager
def context_list(r):
    if len(r) == 0:
        yield []
    else:
        with r[0]() as head, context_list(r[1:]) as tail:
            yield [head] + tail


class ConcatVideoReader(VideoReader):
    def __init__(self, filenames):
        self.readers = [VideoReader.create(i) for i in filenames]

    @contextmanager
    def __call__(self):
        tempfile_name = None
        try:
            with context_list(self.readers) as filenames:
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                    for filename in filenames:
                        temp_file.write("file '{0}'\n".format(filename))
                    tempfile_name = temp_file.name
                # Yield outside the context manager, because Windows concurrent file access 
                yield tempfile_name
        except:
            LOG.exception("Failed ConcatVideoReader")
        finally:
            os.unlink(tempfile_name)

    def input_args(self):
        return ['-f', 'concat', '-safe', '0']

    def video_filename(self):
        return self.readers[0].video_filename()


class VideoEncoder(object):
    # FFMPEG_EXE = 'C:\\Users\\test\\Desktop\\ffmpeg\\bin\\ffmpeg.exe'
    FFMPEG_EXE = 'ffmpeg'

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

    def __init__(self, reader, output, scale=None, extra_ffmpeg_args=None):
        self.reader = reader
        self.output = output
        self.extra_ffmpeg_args = extra_ffmpeg_args if extra_ffmpeg_args is not None else []
        if scale:
            self.extra_ffmpeg_args += ['-vf', 'scale=' + scale]

    def encode(self):
         with self.reader() as infile:
            subprocess.check_call(
                [self.FFMPEG_EXE] + 
                self.reader.input_args() + 
                ['-i', infile] + 
                self.FFMPEG_ARGS + 
                self.extra_ffmpeg_args +
                [self.output])


class VideoFileConverter(object):
    def __init__(self, input_filenames, output_pathname, **kwargs):
        self.input_filenames = input_filenames
        self.output_pathname = output_pathname
        self.additional_arguments = kwargs

    def convert(self):
        for input_file, output_file in zip(self.input_files, self._output_filenames()):
            VideoEncoder(input_file, output_file, self.additional_arguments.get('scale')).encode()

    def _output_filenames(self):
        for input_file in self.input_files:
            basename = os.path.basename(input_file.video_filename())
            yield os.path.join(self.output_pathname, basename[:basename.rindex('.')] + '.mp4')

    @property
    def input_files(self):
        raise NotImplementedError()


class SingleVideoFileConverter(VideoFileConverter):
    @property
    def input_files(self):
        return [VideoReader.create(i) for i in self.input_filenames]


class ConcatVideoFileConverter(VideoFileConverter):
    @property
    def input_files(self):
        return [ConcatVideoReader(self.input_filenames)]
    

def main():
    logging.basicConfig()

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='+', help="Input files")
    parser.add_argument('-o', '--output', required=True, help="Output path")
    parser.add_argument('-s', '--scale')
    parser.add_argument('-c', '--concat', action='store_true', default=False)
    args = parser.parse_args()
    
    if not args.concat:
        SingleVideoFileConverter(args.input, args.output, scale=args.scale).convert()
    else:
        ConcatVideoFileConverter(args.input, args.output, scale=args.scale).convert()


if __name__ == "__main__":
    main()
