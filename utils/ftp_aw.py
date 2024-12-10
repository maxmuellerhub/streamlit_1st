import ftplib
import os
from datetime import datetime

def get_last_file(ftp_server, username, password, directory='/'):
    ftp = ftplib.FTP(ftp_server)
    ftp.login(user=username, passwd=password)
    ftp.cwd(directory)

    # Get a list of files
    files = list(ftp.mlsd())
    files.sort(key=lambda item: item[1]["modify"], reverse=True)
    last_file = files[0][0]

    # Download the latest file
    if last_file:
        with open(last_file, 'wb') as f:
            ftp.retrbinary('RETR ' + last_file, f.write)
        print(f'Downloaded {last_file}')
    else:
        print('No files found.')

    ftp.quit()

def upload_file(ftp_server, username, password, filename, directory='/'):
    ftp = ftplib.FTP(timeout=30)
    ftp.connect(ftp_server)
    ftp.login(user=username, passwd=password)
    ftp.cwd(directory)
    with open(filename,'rb') as file:
        ftp.storbinary(
            "STOR " + str(file.name),
            file,
            blocksize=8192,
            )
    ftp.quit()

def filter_file_by_extension(files):
    extension = [".png", ".gif", ".jpg", ".jpeg", ".pdf"]
    filtered_file = []
    for file in files:
        if file.endswith(tuple(extension)):
            filtered_file.append(file)
    return filtered_file

# Usage
"""
ftp_server = 'ftp.strato.de'
username = 'sftp_witzmanns@witzmanns.de'
password = 'tenniSFtp246!'
directory = '/'

get_last_file(ftp_server, username, password, directory)
"""