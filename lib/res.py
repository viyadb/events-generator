import os
import codecs


def load_file(path):
    '''Load file from current script directory, and return its lines'''
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '.res', path)
    with codecs.open(file_path, encoding='utf-8') as f:
        return f.read().splitlines()
