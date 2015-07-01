#!/usr/bin/python3

ord_constant = 48

def single_string_to_int(s):
    n = ord(s) - ord_constant
    return n

def multi_string_to_int(s):
    acc = 0
    for c in s:
        acc = acc * 10        
        acc = acc + single_string_to_int(c)
    return acc

def multi_string_to_float(s):
    decimal_place = s.find('.')
    if decimal_place == -1:
        return multi_string_to_int(s)
    else:
        int_part = multi_string_to_int(s[:decimal_place])
        decimal_part = multi_string_to_int(s[decimal_place+1:]) / 10**len(s[decimal_place+1:])
        return int_part + decimal_part




numbers_and_operators = {40,41,42,43,45,46,47,48,49,50,51,52,53,54,55,56,57}


def get_rid_of_string_rubbish(l):
    if l.count('(') != l.count(')'):
        raise ValueError("All brackets must be opened and closed.")
    a = ''
    for c in l:
        if ord(c) in numbers_and_operators:
            a = a + c
    return a

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
operators = ['+', '-', '*', '/']


# Write a function that deals with the case where 2( or )2

def insert_multiply_where_needed(sum_string):
    new_sum_string = ' '
    considered_string = get_rid_of_string_rubbish(sum_string)
    for a in considered_string:
        if (new_sum_string[-1] == ')' and a in numbers) or (new_sum_string[-1] in numbers and a == '('):
            new_sum_string = new_sum_string + '*' + a
        else:
            new_sum_string = new_sum_string + a
    return new_sum_string[1:]

#print(insert_multiply_where_needed('(1+1)'))



CHARACTERS_IN_SUM = {'1': 'number', '2': 'number', '3': 'number',
                     '4': 'number', '5': 'number', '6': 'number',
                     '7': 'number', '8': 'number', '9': 'number',
                     '0': 'number', '.': 'number',
                     '(': 'bracket', ')': 'bracket',
                     '+': 'operator', '-': 'operator',
                     '*': 'operator', '/': 'operator',
                     ' ': 'other'}


def make_string_into_list(string):
    considered_string = insert_multiply_where_needed(string) + ' '
    new_sum_string = ''
    list_of_sum = []
    for a in considered_string:
        if len(new_sum_string) == 0:
            new_sum_string = new_sum_string + a
        elif CHARACTERS_IN_SUM[new_sum_string[-1]] == CHARACTERS_IN_SUM[a]:
            new_sum_string = new_sum_string + a
        else:
            list_of_sum.append(new_sum_string)
            new_sum_string = a
    return list_of_sum

#print(make_string_into_list('(1+1)'))
#print(make_string_into_list('(12+3) * 4'))


# Find the first ')' and then find the first '(' before that


def make_string_numbers_into_float(sum_list):
    new_sum_list = []
    for a in sum_list:
        if a[0] in numbers:
            new_sum_list = new_sum_list + [multi_string_to_float(a)]
        else:
            new_sum_list = new_sum_list + [a]
    return new_sum_list

#print(make_string_numbers_into_float('(1+1)'))


def rindex(sum_list, character_to_find):
    if character_to_find not in sum_list:
        return -1
    else:
        sum_list.reverse()
        a = sum_list.index(character_to_find)
        return len(sum_list) - a - 1

#print(rindex(['(', 1,'+', 1, ')'], '('))

def take_out_brackets(sum_list):
    if ')' not in sum_list:
        return sum_list
    elif sum_list[0] == '(' and sum_list[-1] == ')':
        end_bracket = rindex(sum_list[:-1], ')')
        open_bracket = rindex(sum_list[:-1], '(')           
    else:
        end_bracket = sum_list.index(')')
        open_bracket = rindex(sum_list[:end_bracket], '(')
        return take_out_brackets(sum_list[:open_bracket] + [sum_list[open_bracket+1:end_bracket]] + sum_list[end_bracket+1:])

#print(take_out_brackets(['(', 1,'+', 1, ')']))


def make_list_into_length_three(sum_list):
    if len(sum_list) == 3:
        return sum_list
    elif '*' in sum_list:
        operator = sum_list.index('*')
        sum_list = sum_list[:operator-1] + [sum_list[operator-1:operator+2]] + sum_list[operator+2:]
        return make_list_into_length_three(sum_list)
    elif '/' in sum_list:
        operator = sum_list.index('/')
        sum_list = sum_list[:operator-1] + [sum_list[operator-1:operator+2]] + sum_list[operator+2:]
        return make_list_into_length_three(sum_list)
    elif '-' in sum_list:
        operator = sum_list.index('-')
        sum_list = sum_list[:operator-1] + [sum_list[operator-1:operator+2]] + sum_list[operator+2:]
        return make_list_into_length_three(sum_list)
    elif '+' in sum_list:
        operator = sum_list.index('+')
        sum_list = sum_list[:operator-1] + [sum_list[operator-1:operator+2]] + sum_list[operator+2:]
        return make_list_into_length_three(sum_list)        

#print(make_list_into_length_three([[1, '+', 1]]))

#print (make_list_into_length_three([['1', '+', '2'], '*', '3', '-', ['4', '+', '5']]))
#print (make_list_into_length_three(['1', '+', '2', '*', '3']))
#print (make_list_into_length_three(['1', '+', '2']))


def make_list_into_tuple(sum_list):
    new_sum_list = make_list_into_length_three(sum_list)
    if isinstance(new_sum_list[0], list) == True and isinstance(new_sum_list[2], list) == True:
        return (make_list_into_tuple(new_sum_list[0]), new_sum_list[1], make_list_into_tuple(new_sum_list[2]))
    elif isinstance(new_sum_list[0], list) == False and isinstance(new_sum_list[2], list) == True:
        return (new_sum_list[0], new_sum_list[1], make_list_into_tuple(new_sum_list[2]))
    elif isinstance(new_sum_list[0], list) == True and isinstance(new_sum_list[2], list) == False:
        return (make_list_into_tuple(new_sum_list[0]), new_sum_list[1], new_sum_list[2])
    else:
        return (new_sum_list[0], new_sum_list[1], new_sum_list[2])



def string_into_tuple_list(sum_string):
    a = make_string_into_list(sum_string)
    a = make_string_numbers_into_float(a)
    a = take_out_brackets(a)
    a = make_list_into_length_three(a)
    return make_list_into_tuple(a)


def eval_tuple(input_tuple):
    left, operator, right = input_tuple
    return eval_individual(left, operator, right)


def eval_individual(left, operator, right):
    if isinstance(left, tuple) == False and isinstance(right, tuple) == False:
        if operator == '*':
            return left * right
        elif operator == '/':
            return left / right
        elif operator == '+':
            return left + right
        elif operator == '-':
            return left - right
    elif isinstance(left, tuple) == False:
        return eval_individual(left, operator, eval_tuple(right))
    elif isinstance(right, tuple) == False:
        return eval_individual(eval_tuple(left), operator, right)
    else:
        return eval_individual(eval_tuple(left), operator, eval_tuple(right))

#print(eval_tuple((1, '+', 1)))

def final_sum(string):
    sum_tuple = string_into_tuple_list(string)
    return eval_tuple(sum_tuple)

print(final_sum('2+3*6'))


