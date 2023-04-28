import os
import shutil
import socket
import urllib
import urllib.request
import zipfile

def read_url(url: str):
    buffer = None
    while buffer is None:
        try:
            buffer = urllib.request.urlopen(url, timeout=5)
        except socket.timeout:
            print("* Connection timeout detected")
    return buffer.read()


def get_file_urls():
    main_page = read_url("http://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm")
    dem3_files = set()
    for line in main_page.decode().split('\n'):
        if "http://viewfinderpanoramas.org/dem3/" in line:
            start = line.index('http')
            end = line.index('" alt')
            dem3_files.add(line[start: end])
    
    result = list(dem3_files)
    result.sort()
    return result


def get_zip(url):
    filename = url.rpartition("/")[2]
    
    try:
        content = read_url(url)
        file = open(filename, "wb")
        file.write(content)
        file.close()
        print(url, "downloaded")
        return filename
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(url, "does not exists")
            return None
        else:
            raise


def extract_hgt(zip_path, drop=True):
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall()

    if drop:
        os.remove(zip_path)


def flatten_hgt(outpath="HGT"):
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    for path in os.listdir():
        if path != outpath and path != "__pycache__" and os.path.isdir(path):
            for file in os.listdir(path):
                shutil.move(os.path.join(path, file), outpath)
            os.rmdir(path)


if __name__ == "__main__":
    for url in get_file_urls():
        filename = get_zip(url)
        if filename is not None:
            extract_hgt(filename)
            print("Last zip extracted")
    
    flatten_hgt()
