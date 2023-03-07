import os
import logging
import shutil
import configparser
import argparse

# set logging file to /tmp/copy-data.log
logging.basicConfig(filename='/tmp/copy-data.log', level=logging.DEBUG)

def process_line(db_name,db_path ,data_dir):

    logging.info('db_name: {}, db_path: {}'.format(db_name, db_path))
    if not os.path.exists(db_path):
        logging.info('creating directory: {}'.format(db_path))
        # create the directory
        os.makedirs(db_path)
    logging.info('data_dir: {}'.format(data_dir))
    # join the data_dir path to the db_path
    source_db_path = os.path.join(data_dir, db_path[1:])
    logging.info('source_db_path: {}'.format(source_db_path))
    # force the copy of each file and directory
    # db_name to upper
    db_name = db_name.upper()
    if db_name not in ['IRISSYS', 'IRISLIB', 'IRISTEMP', 'IRISLOCALDATA', 'IRISAUDIT', 'ENSLIB', 'HSLIB', 'HSSYS' ]:
        # copy the directory
        logging.info('copying directory: {} to {}'.format(source_db_path, db_path))
        shutil.copytree(source_db_path, db_path, symlinks=True, ignore=None, dirs_exist_ok=True)
    elif db_name in ['IRISSYS', 'HSSYS', 'IRISLOCALDATA','IRISAUDIT','IRISTEMP']:
        # overwrite the file IRIS.DAT with the file from the data_dir
        logging.info('copying file: {} to {}'.format(os.path.join(source_db_path, 'IRIS.DAT'), os.path.join(db_path, 'IRIS.DAT')))
        shutil.copyfile(os.path.join(source_db_path, 'IRIS.DAT'), os.path.join(db_path, 'IRIS.DAT'))

def copy_data(iris_cpf_file, data_dir):
    # parse the iris.cpf file with configparser
    config = configparser.ConfigParser(strict=False, allow_no_value=True)
    config.read(iris_cpf_file)
    # get the [Databases] section
    dbs = config['Databases']
    for db_name, db_path in dbs.items():
        process_line(db_name, db_path, data_dir)

def csp_copy(data_dir):
    # copy the csp folders to the data_dir
    csp_folders = 'usr/irissys/csp/'
    root = '/'
    src = os.path.join(data_dir, csp_folders)
    dst = os.path.join(root, csp_folders)
    logging.info('copying directory: {} to {}'.format(src, dst))
    shutil.copytree(src, dst, symlinks=True, ignore=None, dirs_exist_ok=True)

def python_copy(data_dir):
    # copy the python folders to the data_dir
    python_folders = 'usr/irissys/lib/python/'
    root = '/'
    src = os.path.join(data_dir, python_folders)
    dst = os.path.join(root, python_folders)
    logging.info('copying directory: {} to {}'.format(src, dst))
    shutil.copytree(src, dst, symlinks=True, ignore=None, dirs_exist_ok=True)

if __name__ == '__main__':
    # parse the command line arguments with argparse
    parser = argparse.ArgumentParser(description='Copy data from a directory to the IRIS data directory')
    # add the argument for the iris.cpf in the first position or -c or --cpf
    parser.add_argument('-c', '--cpf', help='path to the iris.cpf file')
    # add the argument for the data directory -d or --data_dir or can be at the second position
    parser.add_argument('-d', '--data_dir', help='path to the directory where the data files are located')
    # parse the arguments for csp folders
    parser.add_argument('--csp', help='path to the csp folders')
    # parse the arguments for python libs
    parser.add_argument('-p','--python', help='path to the python libs')

    args = parser.parse_args()
    # get the iris.cpf file
    iris_cpf_file = args.cpf
    # get the data directory
    data_dir = args.data_dir
    copy_data(iris_cpf_file, data_dir)
    # if the csp folders are defined, copy them to the data directory
    if args.csp:
        csp_copy(data_dir)
    # if the python folders are defined, copy them to the data directory
    if args.python:
        python_copy(data_dir)

