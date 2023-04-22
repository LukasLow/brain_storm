file_data_list = []

def open_file(filename):
    file_data = open(filename)
    for line in file_data.read().splitlines():  # splits the data into lines
        file_data_list.append(line.split())     # splits the lines into items
    del file_data_list[0]                       # delete header


# noch einen table machen
file_table = []
def print_table():
    for item in file_data_list:
        file_table.append(item)
        file_table.append("\n")
    return file_table

print_table()
print(file_table)
#print(f"{file_data_list[0]}\n{file_data_list[1]}")

open_file(r"chartIn.txt")
print(file_data_list)



def extract_each(number):   # if the question comes up: is there a window seat available?
    return [item[number] for item in file_data_list]    # returns the value of each row for the given index (aisle)



elements_in_list= len(file_data_list[0]) - 1
h = int(elements_in_list / 2)

#print(elements_in_list)
#print(h)

n = 2
m = -2




# generalisieren!
window_seats = extract_each(1) + extract_each(-1)  # [row A + row F] ## done
aisle_seats = extract_each(h) + extract_each(-h)  # [row C + row D] ## done


#middle_list = extract_each(1)
#print(middle_list[2:-2])


#middle_length = h*2 - 4
#print(middle_length)

#middle_seats = extract_each(2) + extract_each(-2)  # [row B + row E]


# for len window bis aisle *2
middle_seats = [extract_each(2)] + [extract_each(-2)]  # [row B + row E]

#middle_list = file_data_list[] for item in file_data_list]

#counter = 0
#while counter != middle_length:
 #   extract_each(n) + extract_each(m)
#
 #   counter += 1

print(file_data_list[3][1])

print(window_seats)
print(middle_seats)
print(aisle_seats)



def reserved_seats_window():
    if "X" in window_seats:
        index_window = window_seats.index("X")
        return print(index_window)
    else:
        print("All seats are still available.\n")

#file_data.close()


# soll alle Dateien einlesen können (chartIn 1-4)
# mit dictionaries?

