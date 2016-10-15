SETLOCAL ENABLEDELAYEDEXPANSION
FOR %%I IN (*) DO (
SET deststring=%%I
SET deststring=!deststring:mp4=wav!
ffmpeg -i %%I -ac 1 -acodec pcm_s16le -ar 22050 -vn -sn -y ../audio/!deststring!
)