#!/usr/bin/python3

import fractions

NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
OPERATORS = ['+', '-', '*', '/', '^']


def sum_must_always_end_in_a_number(sum_list):
    if isinstance(sum_list[-1], fractions.Fraction):
        return sum_list
    else:
        return sum_must_always_end_in_a_number(sum_list[:-1])

def deal_with_decimals(string_number):
    if '.' not in string_number:
        return string_number
    new_number = ''
    dec_ind = False
    for idx in string_number:
        if idx in NUMBERS and idx != '.':
            new_number += idx
        elif idx == '.' and dec_ind == False:
            new_number += idx
            dec_ind = True
    if new_number[-1] == '.':
        new_number += '0'
    return new_number

#print(deal_with_decimals('0'))
#print(deal_with_decimals('.'))
#print(deal_with_decimals('0.0'))
#print(deal_with_decimals('.0.'))
#print(deal_with_decimals('0.0.0'))


def tidy_up_sum(sum_list):
    if not sum_list:
        return [0]
    new_sum_list = []
    neg_ind = False
    for idx, item in enumerate(sum_list):
        if idx == 0 and item[-1] in OPERATORS:
            if item[-1] == '-':
                neg_ind = True
        elif item[-1] in NUMBERS:
            new_item = deal_with_decimals(item)
            if not neg_ind:
                new_sum_list = new_sum_list + [fractions.Fraction(new_item)]
            else:
                new_sum_list = new_sum_list + [-fractions.Fraction(new_item)]
                neg_ind = False
        else:
            if len(item) > 1 and item[-1] == '-':
                new_sum_list = new_sum_list + [item[-2]]
                neg_ind = True
            else:
                    new_sum_list = new_sum_list + [item[-1]]
    if not new_sum_list:
        return [0]
    else:
        return sum_must_always_end_in_a_number(new_sum_list)


#print(tidy_up_sum(['.']))


def make_list_into_length_three(sum_list):
    if len(sum_list) < 3:
        return [sum_list[0]] + ['+', 0]
    elif len(sum_list) == 3:
        return sum_list
    elif '^' in sum_list:
        operator = sum_list.index('^')
        sum_list = sum_list[:operator-1] + [sum_list[operator-1:operator+2]] + sum_list[operator+2:]
    elif '/' in sum_list:
        operator = sum_list.index('/')
        sum_list = sum_list[:operator-1] + [sum_list[operator-1:operator+2]] + sum_list[operator+2:]
        return make_list_into_length_three(sum_list)
    elif '*' in sum_list:
        operator = sum_list.index('*')
        sum_list = sum_list[:operator-1] + [sum_list[operator-1:operator+2]] + sum_list[operator+2:]
        return make_list_into_length_three(sum_list)
    elif '+' in sum_list:
        operator = sum_list.index('+')
        sum_list = sum_list[:operator-1] + [sum_list[operator-1:operator+2]] + sum_list[operator+2:]
        return make_list_into_length_three(sum_list)
    elif '-' in sum_list:
        operator = sum_list.index('-')
        sum_list = sum_list[:operator-1] + [sum_list[operator-1:operator+2]] + sum_list[operator+2:]
        return make_list_into_length_three(sum_list)        

#print(make_list_into_length_three(tidy_up_sum(['-', '1', '+-', '1', '*', '3'])))
#print(make_list_into_length_three([1]))



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
    a = tidy_up_sum(sum_string)
    a = make_list_into_length_three(a)
    return make_list_into_tuple(a)

#print(string_into_tuple_list(['-', '1', '+-', '1', '*', '3']))

def eval_tuple(input_tuple):
    left, operator, right = input_tuple
    return eval_individual(left, operator, right)


def eval_individual(left, operator, right):
    if isinstance(left, tuple) == False and isinstance(right, tuple) == False:
        if operator == '^':
            return left ** right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                return 'zeroerror'
            else:
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

def final_sum_string(string):
    sum_tuple = string_into_tuple_list(string)
    return str(eval_tuple(sum_tuple))

#print(string_into_tuple_list(['-', '12', '*+-', '1']))
#print(eval_tuple((-12, '+', -1)))
#print(final_sum_string(['..1']))
#print(final_sum(['1', '+', '2', '+', '3']))
#print(final_sum(['..1']))
