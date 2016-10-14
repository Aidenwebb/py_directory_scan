import json
import logging
import time
import os
import csv

# Configure logging

FORMAT = '%(asctime)-15s - %(message)s'

# Configure program
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        logging.basicConfig(filename=config['execution_log_file'], level=logging.INFO, format=FORMAT)

except:

    with open('config.json','w') as f:
        config = {'output_folder': 'infodump-output', 'execution_log_file': 'infodump.log', 'directory_list_file': 'scanlist.txt', 'report_file_size_in': 'GB'}
        json.dump(config, f, indent=2, sort_keys=True)
        logging.basicConfig(filename=config['execution_log_file'], level=logging.INFO, format=FORMAT)
        logging.info("Config not found. Writing default config file")

try:
    dirs_to_scan = [line.strip() for line in open(config['directory_list_file'], 'r')]

except:
    raise FileNotFoundError("{0} file containing list of directories to scan is required".format(config['directory_list_file']))

if config['report_file_size_in'] == 'B':
    f_size_multiplier = 1
elif config['report_file_size_in'] == 'KB':
    f_size_multiplier = 1024
elif config['report_file_size_in'] == 'MB':
    f_size_multiplier = 1024*1024
elif config['report_file_size_in'] == 'GB':
    f_size_multiplier = 1024 * 1024 * 1024
elif config['report_file_size_in'] == 'TB':
    f_size_multiplier = 1024 * 1024 * 1024 * 1024
else:
    raise KeyError('"report_file_size_in" value in config.json must be "B", "MB", "GB", or "TB')


replace_dict = {
    '\u2004' : " ",
    '\u2013' : "-"
}


class ScanFolder(object):

    def __init__(self, directory_path):

        def split_path(path):

            path = path.rstrip('/')

            if (':' in path.split("/")[-1]) or (path.split("/")[-1] == ''):
                spath = "Disk Root - {}".format(path.split("/")[0].replace(':', ''))
            else:
                spath = path.split("/")[-1]

            return spath

        self.directory_path = directory_path
        self.report_file = ".\{0}\{1}.csv".format(config['output_folder'], split_path(directory_path))
        self.total_size = 0

        # Write headings
        self.write_csv_row('Directory Path', 'Directory Size', 'File Name', 'File Size', 'File cTime', 'File mTime', 'File aTime')

    def write_csv_row(self, dir_path, dir_size, file_name='', file_size='', file_ctime='', file_mtime='', file_atime=''):
        with open(self.report_file, 'a', newline='') as csvfile:
            data = [dir_path, dir_size, file_name, file_size, file_ctime, file_mtime, file_atime]

            print(data)

            file = csv.writer(csvfile, delimiter=',')
            try:
                file.writerow(data)
            except Exception as e:
                logging.error(e)
                logging.error("{0} - {1} ".format(data, e))

    def get_folder_size(self):
        self.total_size = self._get_size(self.directory_path)

    def _get_size(self, start_path='.'):
        for ch in ['\u2013', '\u2004']:
            if ch in start_path:

                sanitised_path = start_path.replace(ch, replace_dict[ch])
                logging.info("Sanitising path: {0} | Char {1}".format(sanitised_path, replace_dict[ch]))
            else:
                sanitised_path = start_path

        total_size = 0
        filenames = []
        dirnames = []
        for x in os.scandir(start_path):
            # print(x.path)

            if x.is_file() is True:
                filenames.append(x.path)
            if x.is_file() is False:
                dirnames.append(x.path)

        for directory in dirnames:
            total_size += self._get_size(directory)
            # print("in for loop", directory, total_size)

        for fp in filenames:
            try:
                file_size = os.path.getsize(fp)
                total_size += file_size
                file_c_time = time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime(os.path.getctime(fp)))
                file_m_time = time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime(os.path.getmtime(fp)))
                file_a_time = time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime(os.path.getatime(fp)))
                print(file_size)
                print(file_size / f_size_multiplier)

                self.write_csv_row(sanitised_path, '', os.path.basename(fp), file_size / f_size_multiplier, str(file_c_time), str(file_m_time), str(file_a_time))
            except Exception as e:
                print(e)
                print("Could not read file: ", fp)

        if len(filenames) > 0:
            self.write_csv_row(sanitised_path, total_size / f_size_multiplier, 'Directory contains files')

        else:
            self.write_csv_row(sanitised_path, total_size / f_size_multiplier, 'No files in directory')
        return total_size

if __name__ == "__main__":

    if not os.path.exists(config['output_folder']):
        os.makedirs(config['output_folder'])

    logging.info("Starting directory scanner with config {0}".format(config))
    logging.info("Scan list: {0}".format(dirs_to_scan))

    for directory in dirs_to_scan:
        print(directory)
        directory = directory.replace('\\','/')
        print(directory)
        try:
            logging.info('Starting scan of {0}'.format(directory))
            dir = ScanFolder(directory)
            print(dir.directory_path)
            print(dir.report_file)
            dir.get_folder_size()
            logging.info('Completed scan of {0}. Total size: {1} Bytes'.format(directory, dir.total_size))
        except Exception as e:
            logging.critical("Top level failure: {}".format(e))

logging.info("Directory scanner completed successfully")