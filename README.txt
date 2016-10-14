[Purpose]
This application will scan a folder and all subfolders, sub-subfolders etc and generated a CSV file containing the following data for all folders scanned.

Directory Path, Directory size in GB, Most Recently Modified filename, Most Recently Modified file timestamp

[How to use]

Configure the application in config.json:
 KEY:
    "directory_list_file": - This is the file the scanner will load file paths from. DEFAULT: "scanlist.txt"
    "output_folder": - This is the subdirectory the scanner will output CSV's to. Full file paths are not yet supported. DEFAULT: "infodump-output"
    "exception_log_file": - This the file the scanner will output runtime logging events, information and errors. DEFAULT: "infodump.log"
    "report_file_size_in": - Choose "B" to report in Byes, "KB" for Kilobytes, "MB" for Megabytes or "GB" for Gigabytes. DEFAULT: "GB"

Place a file named "scanlist.txt" in the same directory as the executable.
In scanlist.txt, add folder paths 1 line per item like the example file.