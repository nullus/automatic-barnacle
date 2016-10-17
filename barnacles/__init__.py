#!/usr/bin/env python

from flask import Flask, Response, request
from werkzeug.datastructures import Headers
import os

app = Flask(__name__)

@app.route("/video/<path:path>")
def video_stream(path):
    headers = Headers()
    status = 200
    ranges = None

    if request.headers.has_key("Range"):
        status = 206
        request.headers["Range"]
        range_bytes = request.headers["Range"].split("=")[1]
        ranges = [[i for i in range.split("-")] for range in range_bytes.split(",")]

        if len(ranges) > 1:
            return ("", 416)

    def chunks(start, length, chunk_size=4096):
        with open(path, "rb") as streamfile:
            streamfile.seek(start)
            while length > 0:
                chunk = streamfile.read(min(chunk_size, length))
                if not chunk:
                    break
                length -= len(chunk)
                yield chunk

    start = 0
    size = os.stat(path).st_size
    length = size

    if ranges:
        start = int(ranges[0][0])
        if len(ranges[0]) > 1 and ranges[0][1]:
            end = int(ranges[0][1])
        else:
            end = size - 1

        if end >= size:
            return ("", 416)

        length = end - start + 1

        headers.add('Accept-Ranges', 'bytes')
        headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, end, size))

    headers.add('Content-Length', str(length))
    return Response(chunks(start, length), status=status, headers=headers, mimetype='video/mp4')

@app.route("/play/<path:path>")
def video_player(path):
    player_template = """
<!DOCTYPE html>
<html>
<head>
<title>Test</title>
</head>
<body>
<video id="sampleMovie" src="/video/{0}" type="video/mp4" controls></video>
</body>
"""
    return player_template.format(path)