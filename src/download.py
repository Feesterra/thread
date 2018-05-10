"""Downloads pictures from URLs and """
import argparse
import os
import time

from multiprocessing.pool import ThreadPool
import urllib.request
from PIL import Image

parser = argparse.ArgumentParser(description='Saves images from URLs to directory')

parser.add_argument('--dir', type=str, help='directory for saving images', default='/home/sh/')
parser.add_argument('--threads', help='sets number of threads', default=1)
parser.add_argument('--size', help='sets size needed', default='100x100')

args = parser.parse_args()

error_counter = 0


def size_type_convert():
    """Converts argument size to tuple object"""

    args.size = args.size.split('x')
    args.size = tuple(map(int, args.size))
    if len(args.size) != 2:
        raise Exception("Wrong size typing, please, use XXXxXXX format. Example: 200x200")


def file_read(file):
    """Reads file with URLs and makes a list of them

    :param file: path to target file
    :return urls: list of tuples: (number_of line, URL)
    """

    urls = []
    with open(file, 'r') as f:
        for i, line in enumerate(f.readlines()):
            urls.append((i, line))
    return urls


def statistics(saved):
    """Prints statitics for downloaded images"""

    print('Files downloaded: {}\n'.format(saved) + \
          'Errors occured: {}\n'.format(error_counter) + \
          'Total time: {:.2f}'.format(time.time() - init))


def main_func():
    """Does all work for downloading and changing images"""

    saved = 0
    size_type_convert()
    urls = file_read('/home/sh/urllist.txt')
    for i, url in urls:
        try:
            img = Image.open(urllib.request.urlopen(url))
        except Exception:
            global error_counter
            error_counter += 1
            continue

        filename = "{0:05}.jpg".format(i)
        path = os.path.join(args.dir, filename)

        with open(path, 'w') as file:
            img.thumbnail(args.size)
            img.save(file, "JPEG")
            saved += 1
        print("Finished {}".format(path))
    statistics(saved)


if __name__ == '__main__':
    init = time.time()
    if not os.path.exists(args.dir):
        os.mkdir(args.dir)

    pool = ThreadPool(int(args.threads))
    pool.apply_async(main_func)

    pool.close()
    pool.join()
