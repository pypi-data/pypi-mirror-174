import fileinput


def print_lines(delimiter, rm_columns):
    for line in fileinput.input():
        elements = []
        empty_flag = False
        for i in line.rstrip('\n').split(delimiter):
            if i:
                if empty_flag:
                    elements.append(delimiter + i)
                    empty_flag = False
                else:
                    elements.append(i)
            else:
                if empty_flag:
                    elements.append(delimiter)
                    empty_flag = False
                else:
                    empty_flag = True
                    continue

        new_line = []
        for idx, val in enumerate(elements):
            if idx + 1 not in rm_columns:
                new_line.append(val)

        print(delimiter.join(new_line))