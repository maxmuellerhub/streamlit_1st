import ftplib
import os
from datetime import datetime


def get_last_file(ftp_server, username, password, directory='/')  ->str : 
    """Get the last file on an ftp server. Returns '' if no file fond """
    ftp = ftplib.FTP(ftp_server)
    ftp.login(user=username, passwd=password)
    ftp.cwd(directory)

    # Get a list of files
    files = list(ftp.mlsd())
    files.sort(key=lambda item: item[1]["modify"], reverse=True)           # "modifiy" immer in UTC
    files = list(filter(lambda f: f[0].endswith(".csv"), files))
    last_file = files[0][0]
    if last_file:                                                                                                                                                                    
        with open(last_file, 'wb') as f:
            ftp.retrbinary('RETR ' + last_file, f.write)
        print(f'Downloaded {last_file}')
    else:
        last_file = ''
        print('No files found.')
    ftp.quit()
    return last_file


def upload_file(ftp_server, username, password, filename, directory='/'):
    """Uploads a file to an ftp server"""
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
if __name__=="__main__":
    import streamlit as st

    ftp_server = st.secrets["STOR_URL"]
    username = st.secrets["STOR_USERNAME"]
    password = st.secrets["STOR_PW"]
    directory = '/'

    get_last_file(ftp_server, username, password, directory)