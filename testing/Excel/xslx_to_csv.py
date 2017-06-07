#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlrd
import csv

# https://stackoverflow.com/questions/9884353/xls-to-csv-converter

def csv_from_excel():
    wb = xlrd.open_workbook('xslx_to_csv.xlsx')
    sh = wb.sheet_by_index(0)
    your_csv_file = open('xslx_to_csv.csv', 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_NONE, delimiter=";")
    #wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        #wr.writerow(sh.row_values(rownum))
        wr.writerow([unicode(entry).encode("utf-8") for entry in sh.row_values(rownum)])

    your_csv_file.close()

if __name__ == "__main__":
    csv_from_excel()

