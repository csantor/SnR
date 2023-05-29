import os
import pathlib

DOWNLOAD_PATH = os.environ.get('DOWNLOAD_PATH', str(pathlib.Path(__file__).parent.absolute()) + '/db_files')