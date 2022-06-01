from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
import json, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = '//'.join([ROOT_DIR, 'config.json'])

# Create download folder
download_path = '//'.join([ROOT_DIR, 'download'])
os.mkdir(download_path)

# read configuration file
with open(config_path) as config_file:
    config = json.load(config_file)
    config = config['share_point']

SHAREPOINT_USERNAME = config['username']
SHAREPOINT_PASSWORD = config['password']
SHAREPOINT_URL = config['url']
SHAREPOINT_SITE = config['site']
SHAREPOINT_FOLDER = config['folder']

authcookie = Office365(SHAREPOINT_URL, username=SHAREPOINT_USERNAME, password=SHAREPOINT_PASSWORD).GetCookies()
site = Site(SHAREPOINT_SITE, version=Version.v2016, authcookie=authcookie)

folder = site.Folder(SHAREPOINT_FOLDER)
allfiles= folder.files

def download_file(file_name, data):
    try:
        with open(file_name, 'wb') as f:
            f.write(data)
            f.close()
        return True
    except:
        print('Cannot download file ' + file_name)
    return False

def delete_file(file_name):
    folder.delete_file(file_name)
     
for file in allfiles:
    file_name = file['Name']
    destination_file = '//'.join([download_path, file_name])
    
    fdata = folder.get_file(file_name)

    # Download file from Sharepoint
    status = download_file(destination_file, fdata)
    print(destination_file, status)

    # Delete file when download success
    if (status):
        delete_file(file_name)
