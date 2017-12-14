import sys
import re
import csv
import sys
import logging


logging.basicConfig(#filename = "log.txt",
    level = logging.INFO,
    format = "%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

delimiter = re.compile(r"\s\s+")
#control_chars = re.compile(r"\u202a|\u202b|\u202c")
table_data_start = "پیوست 1"


def normalize_text(in_text, form_map):
    out_text = []
    for c in in_text:
        if ord(c) in range(0x202A, 0x202A + 3):
            ## pass over whitespaces
            pass
        else:
            try:
                ## append regular form of char if found in map
                out_text.append(form_map[c])
            except KeyError:
                ## append the char
                out_text.append(c)
        
    return "".join(out_text)


def init_form_map(file_path):
    form_map = {}
    with open(file_path, newline = "") as f:
        csv_r = csv.reader(f)
        for row in csv_r:
            form_map[row[0]] = row[1]
    return form_map


def parse_text_file(in_file_path, out_file_path):
    is_parsing = False
    in_file = open(in_file_path)
    out_file = open(out_file_path, "w", newline = "")
    fieldnames = ["code", "title", "amount"]
    csv_w = csv.DictWriter(out_file, fieldnames)
    csv_w.writeheader()
    ## map from Persian presentation form to regular form
    form_map = init_form_map("form_map.csv")
    is_error = False
    is_first_row = True
    is_data_section = False
    
    for line in in_file:
        line = line.strip()
        ## not interested in blank lines
        if line == "":
            continue
        line = normalize_text(line, form_map)
        logger.debug(line)
        ## the end token is when we see one (and only one) number
        ## which must be the page number
        is_new_row = False
        parts = delimiter.split(line)
        if (len(parts) == 15):
            is_new_row = True
            is_data_section = True
        if line.isnumeric():
            is_data_section = False
        if not is_first_row and is_new_row:
            csv_w.writerow({"code": code, "title": title, "amount": amount})
        if is_data_section:
            if is_new_row:
                code = parts[-1]
                title = parts[-2]
                amount = parts[0].replace(",", "")
                is_first_row = False
            else:
                title += " " + line
                
        ## determine start and end of the table using special lines
        ## this is the token for beginning of the data section of a table
        # if line == table_data_start:
        #     is_parsing = True
    
    in_file.close()
    out_file.close()


if __name__ == "__main__":
    parse_text_file("1397.txt", "output.csv")

    
