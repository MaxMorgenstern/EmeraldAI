#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlrd
import csv

def ToCsv(excelFile, outputFile):
    wb = xlrd.open_workbook(excelFile)
    sh = wb.sheet_by_index(0)
    yourCsvFile = open(outputFile, 'wb')
    wr = csv.writer(yourCsvFile, quoting=csv.QUOTE_NONE, delimiter=";")

    for rownum in xrange(sh.nrows):
        wr.writerow([unicode(entry).encode("utf-8") for entry in sh.row_values(rownum)])

    yourCsvFile.close()
