from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from datetime import datetime
import json
import os


def print_log(msg):
    now = datetime.now()
    current_time = now.strftime("%b %d, %Y %H:%M:%S")
    print(current_time, msg)


print_log('Start service')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = '//'.join([ROOT_DIR, 'config.json'])

# Create download folder
download_path = '//'.join([ROOT_DIR, 'download'])
is_exists_path = os.path.exists(download_path)

if not is_exists_path:
    os.mkdir(download_path)

# read configuration file
with open(config_path) as config_file:
    config = json.load(config_file)
    config = config['share_point']

SHAREPOINT_USERNAME = config['username']
print_log('username *****')
SHAREPOINT_PASSWORD = config['password']
print_log('password *****')
SHAREPOINT_URL = config['url']
print_log('url ' + SHAREPOINT_URL)
SHAREPOINT_SITE = config['site']
print_log('site ' + SHAREPOINT_SITE)
SHAREPOINT_FOLDER = config['folder']
print_log('folder ' + SHAREPOINT_FOLDER)

authcookie = Office365(SHAREPOINT_URL, username=SHAREPOINT_USERNAME,
                       password=SHAREPOINT_PASSWORD).GetCookies()
site = Site(SHAREPOINT_SITE, version=Version.v2016, authcookie=authcookie)

folder = site.Folder(SHAREPOINT_FOLDER)
allfiles = folder.files
print_log('read folder files success')


def download_file(file_name, data):
    try:
        print_log('download file ' + file_name)
        with open(file_name, 'wb') as f:
            f.write(data)
            f.close()
        return True
    except:
        print_log('Cannot download file ' + file_name)
    return False


def delete_file(file_name):
    print_log('delete file ' + file_name)
    folder.delete_file(file_name)


for file in allfiles:
    file_name = file['Name']
    destination_file = '//'.join([download_path, file_name])
    print_log('destination file ' + destination_file)

    fdata = folder.get_file(file_name)
    print_log('read file object success')

    # Download file from Sharepoint
    status = download_file(destination_file, fdata)
    print_log('download status ' + str(status))

    # Delete file when download success
    if (status):
        delete_file(file_name)

print_log('End service')
