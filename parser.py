import sys
import re
import csv
import sys
import logging


logging.basicConfig(filename = "log.txt", filemode = "w",
    level = logging.DEBUG,
    format = "%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

delimiter = re.compile(r"\s\s+")
#control_chars = re.compile(r"\u202a|\u202b|\u202c")
table_data_start = "پیوست 1"


def normalize_text(in_text: str, form_map) -> str:
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
        
    return ("".join(out_text)).strip()


def init_form_map(file_path):
    form_map = {}
    with open(file_path, newline = "") as f:
        csv_r = csv.reader(f)
        for row in csv_r:
            form_map[row[0]] = row[1]
    return form_map

def clean_text(in_text: str) -> str:
    out_text = in_text
    out_text = re.sub("\s\s+", " ", out_text)
    out_text = out_text.replace(" ،", "،").replace("،", "، ")
    out_text = out_text.replace("( ", "(").replace("(", " (")
    out_text = out_text.replace(" )", ")").replace(")", ") ")
    out_text = re.sub("\s\s+", " ", out_text)
    return out_text

    
def parse_text_file(in_file_path: str, out_file_path: str, from_page: int, to_page: int, col_count: int):
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
    cur_page = 1
    
    for line in in_file:
        line = line.strip()
        ## not interested in blank lines
        if line == "":
            continue

        logger.debug(line)
        line = normalize_text(line, form_map)
        logger.debug(line)
        ## the end token is when we see one (and only one) number
        ## which must be the page number
        if line.isnumeric():
            is_data_section = False
            cur_page = int(line) + 1

        if cur_page >= from_page and cur_page <= to_page + 1:
            is_new_row = False
            parts = delimiter.split(line)
            if (len(parts) >= col_count):
                is_new_row = True
                is_data_section = True
            if not is_first_row and is_new_row:
                title = clean_text(title)
                csv_w.writerow({"code": code, "title": title, "amount": amount})
                if cur_page > to_page:
                    break
            if is_data_section:
                if is_new_row:
                    code = parts[-1]
                    title = " ".join(parts[(col_count - 2):-1])
                    title = title
                    amount = parts[0].replace(",", "")
                    is_first_row = False
                else:
                    title += " " + line
                    
    in_file.close()
    out_file.close()


if __name__ == "__main__":
    from_page = 64
    to_page = 189
    col_count = 15
    parse_text_file("1397.txt", "output.csv", from_page, to_page, col_count)

    
