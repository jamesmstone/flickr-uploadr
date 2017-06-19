# Flickr-uploadr
A docker image that uploads all media in a dir to flickr

## Example Usage:

`docker run -it -v $HOME/token:/token -e "api_key=keyhere" -e "api_secret=secrethere" -v $(pwd)/image_dir:/images/ jamesmstone/flickr-uploadr`


This uploads the media in  `$(pwd)/image_dir` to flickr 
and stores the users token in  `$HOME/token`
Note you need your own api key and secret
This uses the new `oauth` method of authentication.

## Prereq's

 - [docker](https://www.docker.com/) - Yes that's it!

I find the easiest way to install on linux devices is `$ ` [`wget -O - https://bit.ly/docker-install| bash`](https://gist.github.com/wdullaer/f1af16bd7e970389bad3#gistcomment-1589374)
