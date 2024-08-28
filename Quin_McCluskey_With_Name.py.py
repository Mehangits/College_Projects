import numpy

NAME = "MEHAN"
VARIABLE = 4


def Binary(n):
    s = bin(n)
    s1 = s[2:]
    return (s1)


def standardize_binary(n, num_var):
    if len(n) < num_var:
        extra_zero = num_var - len(n)
        for i in range(extra_zero):
            n = '0' + n
        return n
    else:
        return n


def generate_minterms_ASCII(name):
    minterms = set()
    for char in name:
        ascii_code = ord(char)
        ascii_digits = set(int(digit) for digit in str(ascii_code))
        minterms.update(ascii_digits)
    return list(minterms)


def make_binary_list(minterms_list, var):
    binary_list = []
    temp = ''
    for n in minterms_list:
        temp = standardize_binary(Binary(n), var)
        binary_list.append(temp)
    return binary_list


def count_one(string):
    count = 0
    for n in string:
        if n == '1':
            count = count + 1
    return count


def order_list(binary_list, var):
    final_list = []
    new_list = []
    for n in range(var + 1):
        for m in binary_list:
            if count_one(m) == n:
                new_list.append(m)

    return new_list


def group_list(order_lists, var):
    ones = var + 1
    final_list = []
    for n in range(ones):
        final_list.append([])

    # group like one's in each mini list
    for n in range(ones):
        for m in order_lists:
            if count_one(m) == n:
                final_list[n].append(m)
    final_list = [n for n in final_list if n != []]
    return final_list


# terms = generate_minterms_ASCII(NAME)
terms = generate_minterms_ASCII(NAME)
print(terms)

new_list = make_binary_list(terms, VARIABLE)
print(new_list)

ordered = order_list(new_list, VARIABLE)
print(ordered)

grouped_list = group_list(ordered, VARIABLE)
print(grouped_list)

# Figure out which has one bit difference
terms_bin_pair = {}
for n in terms:
    for m in new_list:
        if standardize_binary(Binary(n), VARIABLE) == m:
            terms_bin_pair[m] = n
print(terms_bin_pair)


def binary_difference(bin1, bin2):
    count = 0
    new_bin = ''
    new1 = bin1
    new2 = bin2
    new3 = ''
    for i in range(len(bin1)):
        if bin1[i] == bin2[i]:
            continue
        else:
            new3 = new1[:i] + "_" + new2[i + 1:]
            count = count + 1
    if count == 1:
        new_bin = new3
        return new_bin
    else:
        return ''


def compare_bits(pair_list, block_list):
    single_diff_dict = dict()
    group_len = int(len(block_list))
    for i in range(group_len):
        first = i
        next_val = i + 1
        if next_val > group_len - 1:
            break
        else:
            for bin1 in block_list[first]:
                check_sum = 0
                for bin2 in block_list[next_val]:
                    temp1 = str(pair_list[bin1])
                    temp2 = str(pair_list[bin2])
                    one_diff_bin = str(binary_difference(bin1, bin2))
                    if one_diff_bin != '':
                        final_pair = temp1 + '+' + temp2
                        single_diff_dict[one_diff_bin] = final_pair
                    # else:
                    #     check_sum = check_sum + 1
                    # if len(block_list[next_val]) == check_sum:
                    #     single_diff_dict[bin1] = temp1
    return single_diff_dict


def make_new_list(bin_pair, var):
    new_list = []
    for n in bin_pair.keys():
        new_list.append(n)
    order_new_list = order_list(new_list, var)
    grouped_order_list = group_list(order_new_list, var)
    return grouped_order_list


# first iteration
compared_dict = compare_bits(terms_bin_pair, grouped_list)
print(compared_dict)
grouped_list_1 = make_new_list(compared_dict, VARIABLE)
print(grouped_list_1)

print("###########################################################################################")
#
# # second iteration
# compared_dict_2 = compare_bits(compared_dict, grouped_list_1)
# print(compared_dict_2)
# grouped_list_2 = make_new_list(compared_dict_2, VARIABLE)
# print(grouped_list_2)
#
# print("############################################################################################")
#
# # third iteration
# compared_dict_3 = compare_bits(compared_dict_2, grouped_list_2)
# print(compared_dict_3)
# grouped_list_3 = make_new_list(compared_dict_3, VARIABLE)
# print(grouped_list_3)


# NOW WE NEED TO FORM THE TABLE
# VARIABLES A,B,C,D
# A:0, B:1, C:2, D:3

input_dict_1 = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
input_dict_2 = {0: 'a', 1: 'b', 2: 'c', 3: 'd'}
tabel_bits_list = []
# convert the newest list into normal list

for i in range(len(grouped_list_1)):
    for j in grouped_list_1[i]:
        tabel_bits_list.append(j)

# Convert the values into its letters
table_minterms_list = []


def convert_bit_minterm(bits, Ref1, ref2):
    temp_list = []
    temp_final = ''
    for i in range(len(bits)):
        if bits[i] == '1':
            temp_list.append(Ref1[i])
        if bits[i] == '0':
            temp_list.append(ref2[i])
    for i in temp_list:
        temp_final = str(temp_final) + str(i)
    return temp_final


for i in tabel_bits_list:
    table_minterms_list.append(convert_bit_minterm(i, input_dict_1, input_dict_2))


# make a new dictionary for the numbers and bits pair with bits being key and numbers as list
def convert_num_to_list_values(bits, dict_pairs):
    new_list = []
    for i in dict_pairs[bits]:
        if i != '+':
            new_list.append(i)
    return new_list


# new dict for list and bits pair
list_bits_pair = {}

for i in tabel_bits_list:
    list_bits_pair[i] = convert_num_to_list_values(i, compared_dict)
print(tabel_bits_list)
print(table_minterms_list)
print(list_bits_pair)

FINAL_TABLE = []

for i in range(len(table_minterms_list)):
    temp = []
    temp.append(table_minterms_list[i])
    temp.append(list_bits_pair[tabel_bits_list[i]])
    for j in range(len(terms)):
        temp.append('0')
    FINAL_TABLE.append(temp)
for i in FINAL_TABLE:
    print(i)

# Make dict pair for the terms and indices of the final table
indices_terms_pair = {}
for i in range(len(FINAL_TABLE[0])):
    if i == 0 and i == 1:
        random_temp_for_this = 1
    else:
        indices_terms_pair[str((terms[i - 2]))] = i
print(indices_terms_pair)

print("####################################################################")
# start adding x to the given area############################
def put_x(solo_list, indices_dict):
    for i in solo_list[1]:
        solo_list[indices_dict[i]] = 'X'
    return solo_list


UPDATED_FINAL_TABLE = []
for i in FINAL_TABLE:
    UPDATED_FINAL_TABLE.append(put_x(i, indices_terms_pair))
for i in UPDATED_FINAL_TABLE:
    print(i)
print("################################################################################3")


###############################################################
# Now we need to put a y for those essential prime in each column
def count_x_in_column(final_table, position):
    count = 0
    for i in final_table:
        if i[position] == 'X':
            count = count + 1
    return count


def add_y_in_row(final_table):
    temp_table = final_table
    for i in temp_table:
        for j in range(2, len(i)):
            if i[j] == 'X':
                if count_x_in_column(final_table, j) == 1:
                    i[j] = 'Y'
                else:
                    pass
            else:
                pass
    return temp_table


UPDATED_FINAL_TABLE_2 = add_y_in_row(UPDATED_FINAL_TABLE)
for i in UPDATED_FINAL_TABLE_2:
    print(i)

print("###################################################################################")


##############################################################
# now we need to remove the row which has no Y in it

def count_y(table_row):
    count = 0
    for i in range(2, len(table_row)):
        if table_row[i] == 'Y':
            count = count + 1
        else:
            pass
    return count


def remove_row_without_y(whole_table):
    temp_row = whole_table
    new_table = []
    for row in temp_row:
        count = count_y(row)
        if count == 0:
            pass
        else:
            new_table.append(row)
    return new_table


UPDATED_FINAL_TABLE_3 = remove_row_without_y(UPDATED_FINAL_TABLE_2)
for i in UPDATED_FINAL_TABLE_3:
    print(i)

# now we need to finalize the answer
print(f"The boolean logic for the ASCII number of the name {NAME} is: {UPDATED_FINAL_TABLE_3[0][0]} + {UPDATED_FINAL_TABLE_3[1][0]} + {UPDATED_FINAL_TABLE_3[2][0]}")
print("Where lower case letters represents the complement of the original input")
print("Example: a = A complement")
