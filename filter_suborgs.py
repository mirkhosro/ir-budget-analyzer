import sys
import re
import csv
import sys
import logging

## set up logging
logging.basicConfig(#filename = "log.txt",
    level = logging.DEBUG,
    format = "%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

LEVEL1_CODE_LEN = 6

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        logger.error("The input CSV file name should be specified.")
        sys.exit(1)

    ## first arg is assumed to be the input csv file
    in_file_path = sys.argv[1]
    try:
        in_file = open(in_file_path, newline = "")
        csv_r = csv.reader(in_file)
        ## first output file is for level 1 org budgets
        out_file_1 = open(in_file_path + "_level1.csv", "w", newline = "")
        csv_w1 = csv.writer(out_file_1)
        csv_w1.writerow(["code", "title", "amount_mR", "amount_bT"])
        ## second output file is for level 2 org budgets
        out_file_2 = open(in_file_path + "_level2.csv", "w", newline = "")
        csv_w2 = csv.writer(out_file_2)
        csv_w2.writerow(["code", "sub_code", "subtitle", "title", "amount_mR", "amount_bT"])
        ## discard header
        next(csv_r)
        sup_title = ""
        for row in csv_r:
            ## check if level 1 org budget
            code = row[0]
            title = row[1]
            amount_mR = int(row[2])
            amount_bT = round(amount_mR / 10000, 1)
            if len(code) >= LEVEL1_CODE_LEN:
                csv_w1.writerow([code, title, amount_mR, amount_bT])
                ## record the super org title and code for sub-orgs
                sup_title = title
                sup_code = code
            else:
                ## it's a level 2 org budget
                csv_w2.writerow([sup_code, code, title, sup_title, amount_mR, amount_bT])
    except Exception as ex:
        logger.error(ex)
        sys.exit(1)
    finally:
        in_file.close()
        out_file_1.close()
        out_file_2.close()
                
