# search_file_by_column
A simple utility for indexing and retrieving lines based on the value of a column.

This is a quick hack to allow multiple lookups based on the value of a column in a white-space delimited file without having to first sort your input. Initial index creation will be slow, but subsequent lookups should be relatively quick.

## Usage

    search_file_by_column.py [-h] [-s STRING] [-z INDEX_SIZE] FILE COL

    Index and retrieve file entries by column.

    positional arguments:
      FILE                  Input filename
      COL                   Column of file to search/index. Default=1

    optional arguments:
      -h, --help            show this help message and exit
      -s STRING, --string STRING
                            String to search for
      -z INDEX_SIZE, --index_size INDEX_SIZE
                            Size of index. Default = 2^24
