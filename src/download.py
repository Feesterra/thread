"""Downloads pictures from URLs and saves them to a particular directory"""

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
saved = 0


def size_type_convert():
    """Converts argument size to tuple object"""

    args.size = args.size.split('x')
    args.size = tuple(map(int, args.size))
    if len(args.size) != 2:
        raise Exception("Wrong size typing, please, use XXXxXXX format. Example: 200x200")


size_type_convert()


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
    """Prints statistics for downloaded images"""

    print('Files downloaded: {}\n'.format(saved) + \
          'Errors occured: {}\n'.format(error_counter) + \
          'Total time: {:.2f}'.format(time.time() - init))


def main_func(url):
    """Downloads picture from url and saves it

    :param url: tuple(picture number, url)
    """

    global saved

    if not os.path.exists(args.dir):
        os.mkdir(args.dir)

    try:
        img = Image.open(urllib.request.urlopen(url[1]))
    except Exception:
        global error_counter
        error_counter += 1

    filename = "{0:05}.jpg".format(url[0])
    path = os.path.join(args.dir, filename)

    with open(path, 'wb') as file:
        img.thumbnail(args.size)
        img.save(file, "JPEG")

        saved += 1
    print("Finished {}".format(path))


if __name__ == '__main__':
    init = time.time()
    urls = file_read('/home/sh/urllist.txt')

    x = int(args.threads)

    pool = ThreadPool(x)
    pool.map(main_func, urls)

    pool.close()
    pool.join()

    statistics(saved)
