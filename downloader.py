# module for download documents announcements
import os
import urllib.request
from urllib.error import URLError

def download_document(download_url, path_store, file_name):
    ''' Download a specific pdf alocated in
        download_url and store in path_store with a specific
        file_name.
    '''

    try:

        response = urllib.request.urlopen(download_url)
        file = open(path_store+file_name,'wb')
        file.write(response.read())
        file.close()
    
    except URLError as e:

        print(e)
        pass            # Flag: that document pdf url of that announcement don´t work
                        # build store fail information somewhere...

if __name__=="__main__":
    pass
