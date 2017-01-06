# Transcoding

Grab a puppies

    curl -o input.mp4 'http://downloads.4ksamples.com/downloads/PUPPIES%20BATH%20IN%204K%20(ULTRA%20HD)(Original_H.264-AAC)%20(4ksamples.com).mp4'

Transcode (iPhone 6ish)

    ffmpeg -i input.mp4 -f mp4 -preset veryfast -tune film -profile:v high -level 4.2 -c:v h264 -c:a aac -crf 23 -movflags +faststart -vf scale=-1:1080 output.mp4

# To-do/Fixme

- Find a way to unify configuration for database URL (specified in alembic.ini and ...)
