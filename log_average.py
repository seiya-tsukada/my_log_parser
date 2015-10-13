#! /usr/bin/env python
# coding: utf-8

import os
import sys
import csv
import tempfile

def create_csv_file():
  argvs = sys.argv

  target_file = argvs[1]

  with tempfile.NamedTemporaryFile(delete=False, dir="/tmp") as tf:
    tf.write("request_time,reqmicsec"  + "\n")
    with open(target_file) as f:

      for line in f:
        target_str = None
        target_str = generate_kv_recode(line)

        tf.write(target_str + "\n")

  return tf.name

def generate_kv_recode(line):
  arr_line = line.split("\t")

  for i in arr_line:
    if ("request_time" in i):
      parse_request_time = None
      parse_date_split = None
      parse_date_split = i.split(":")
      parse_request_time = "{0}:{1}:{2}:{3}".format(parse_date_split[1].split("[")[1], parse_date_split[2], parse_date_split[3], parse_date_split[4].split()[0])

    if ("reqmicsec" in i):
      parse_reqmicsec = None
      parse_reqmicsec_split = None
      parse_reqmicsec_split = i.split(":")

      parse_reqmicsec = parse_reqmicsec_split[1]

  target_str = "{0},{1}".format(parse_request_time, parse_reqmicsec)

  return target_str

def reqmicsec_ave(csv_file):

  with open(csv_file, "r") as f:
    reader = csv.reader(f)
    # skip header
    header = next(reader)

    uniq_request_time = list()
    for row in reader:
      uniq_request_time.append(row[0])

  uniq_request_time = sorted(set(uniq_request_time), key=uniq_request_time.index)

  for i in uniq_request_time:
    reqmicsec_average = 0
    num = 0

    with open(csv_file, "r") as f:
      reader = csv.reader(f)
      header = next(reader)

      for row in reader:
        if i == row[0]:
          reqmicsec_average = reqmicsec_average + int(row[1])
          num = num + 1

      reqmicsec_average = reqmicsec_average / num

      print i, reqmicsec_average

if __name__ == "__main__":
  csv_file = create_csv_file()

  reqmicsec_ave(csv_file)

  print csv_file
  os.remove(csv_file)

  exit(0)
