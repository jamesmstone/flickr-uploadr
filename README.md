# Flickr-uploadr
A docker image that uplaods all media in a dir to flickr

## Example Usage:

`docker run -it -v $HOME/token:/token -e "api_key=keyhere" -e "api_secret=secrethere" -v $(pwd)/image_dir:/images/ jamesmstone/flickr-uploadr`


This uploads the media in  `$(pwd)/image_dir` to flickr 
and stores the users token in  `$HOME/token`
Note you need your own api key and secret
This uses the new oauth lib.
