import logging
import time
import os
import csv

report_file = 'report.csv'

replace_dict = {
    '\u2004' : " ",
    '\u2013' : "-"
}

FORMAT = '%(asctime)-15s - %(message)s'
logging.basicConfig(filename='dirscanner.log', level=logging.INFO, format=FORMAT)


def write_csv_row(row):
    with open(report_file, 'a', newline='') as csvfile:
        print(row)

        file = csv.writer(csvfile, delimiter=',')
        try:
            file.writerow(row)
        except Exception as e:
            logging.warning(e)
            logging.warning("{} - {}".format(row.encode('ascii', 'ignore'), e))


def get_newest_file(path):
    newest_file = max(os.listdir(path), key=lambda f: os.path.getmtime("{}/{}".format(path, f)))
    newest_file_mod_time = time.strftime("%d/%m/%Y %I:%M:%S %p",
                                         time.localtime(os.stat(("{}\{}".format(path, newest_file))).st_mtime))
    return [newest_file, newest_file_mod_time]

def get_size(start_path = '.'):
    for ch in ['\u2013', '\u2004']:
        if ch in start_path:

            sanitised_path=start_path.replace(ch,replace_dict[ch])
            logging.info("Sanitising path: {0} | Char {1}".format(sanitised_path, replace_dict[ch]))
        else: sanitised_path = start_path

    total_size = 0
    filenames = []
    dirnames = []
    for x in os.scandir(start_path):
        #print(x.path)

        if x.is_file() is True:
            filenames.append(x.path)
        if x.is_file() is False:
            dirnames.append(x.path)

    for directory in dirnames:
        total_size += get_size(directory)
        #print("in for loop", directory, total_size)

    for fp in filenames:
        try:
            total_size += os.path.getsize(fp)
        except:
            print("Could not read file: ", fp)



    if len(filenames) > 0:
        newest_file = get_newest_file(start_path)
        write_csv_row([sanitised_path, total_size/(1024*1024*1024), newest_file[0], newest_file[1]])
        #print(start_path, total_size, get_newest_file(start_path))

    else:
        write_csv_row([sanitised_path, total_size/(1024*1024*1024), 'Null', 'Null'])
        #print(start_path, total_size, 'Null', 'Null')
    return total_size

try:
    dirs = [line.strip() for line in open("config.txt", 'r')]

except:
    print("config.txt required.")


if __name__ == "__main__":

    for directory in dirs:

        report_file = "{}.csv".format(directory.split("\\")[-1])
        print(report_file)
        get_size(directory)
