import flickrapi
import webbrowser
import os

import sys

import pkg_resources

api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')

flickr = flickrapi.FlickrAPI(api_key, api_secret, token_cache_location='/token')

print('Step 1: authenticate')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms='write'):
    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms='write')
    print(authorize_url)
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = str(input('Verifier code: '))

    # Trade the request token for an access token
    print(flickr.get_access_token(verifier))

print('Step 2: use Flickr')


class FileWithCallback(object):
    def __init__(self, filename, callback):
        self.file = open(filename, 'rb')
        self.callback = callback
        # the following attributes and methods are required
        self.len = os.path.getsize(filename)
        self.fileno = self.file.fileno
        self.tell = self.file.tell

    def read(self, size):
        if self.callback:
            self.callback(self.tell() * 100 // self.len)
        return self.file.read(size)


def callback(progress):
    bar_size = 50
    p = int((progress / 100) * bar_size)
    bar = ('#' * p) + (' ' * (bar_size - p))
    sys.stdout.write('\r' + str(progress) + '% [' + bar + ']')
    sys.stdout.flush()


photo = pkg_resources.resource_filename(__name__, 'test.png')
params = {}
dir = '/images/'
for full_filename in os.listdir('/images'):
    filename_split = full_filename.split('.')

    if len(filename_split) == 2:
        ext = filename_split[1].lower()
    else:
        ext = ''
    if ext in ['png', 'jpeg', 'jpg', 'avi', 'mp4', 'gif', 'tiff', 'svg', 'mov', 'wmv', 'ogv', 'mpg', 'mp2', 'mpeg',
               'mpe', 'mpv']:
        try:
            print(full_filename)
            sys.stdout.flush()
            params['filename'] = dir + full_filename
            params['fileobj'] = FileWithCallback(params['filename'], callback)

            uploadResp = flickr.upload(filename=params['filename'], fileobj=params['fileobj'], is_public=0, is_friend=0,
                                       is_family=1)
            callback(100)
            photo_id = uploadResp.findall('photoid')[0].text
            print(' success! flickr photo id= ' + photo_id)
            sys.stdout.flush()
        except:
            try:
                print("FAILED " + full_filename + "trying once again")
                sys.stdout.flush()
                params['filename'] = dir + full_filename
                params['fileobj'] = FileWithCallback(params['filename'], callback)

                uploadResp = flickr.upload(filename=params['filename'],
                                           fileobj=params['fileobj'],
                                           is_public=0,
                                           is_friend=0,
                                           is_family=1
                                           )
                callback(100)
                photo_id = uploadResp.findall('photoid')[0].text
                print(' success! flickr photo id: ' + photo_id)
                sys.stdout.flush()
            except:
                print("FAILED " + full_filename + " for the last time")
                pass
