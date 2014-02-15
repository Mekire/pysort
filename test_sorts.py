"""
Runs a series of tests on a number of sorting algorithms found in pysort.py.
Sorting methods which are impractically tested are not included in the
automatic testing but can be tested manually with the test() function.
"""

from __future__ import print_function

import sys
import random
import pysort

from timeit import timeit

if sys.version_info[0] < 3:
    range = xrange


def perform_swaps(sequence, n):
    """Perform n swaps on a list to create a mostly sorted list sample."""
    for _ in range(n):
        length = len(sequence)
        i = random.randrange(length)
        j = (i+1)%length
        sequence[i], sequence[j] = sequence[j], sequence[i]
    return sequence


def test(sort, sequence, count=100):
    """Test against builtin and time the given sort function."""
    builtin = sorted(sequence)
    copy = sequence[:]
    testrun = sort(copy)
    recieved = testrun if testrun else copy
    template = "{} sort worked incorrectly. \nRecieved: {} \nExpected: {}"
    error_message = template.format(sort.__name__, recieved, builtin)
    assert (testrun == builtin or copy == builtin), error_message
    time = timeit(lambda: sort(sequence[:]),number=count)/count
    print("{:>7.5f} : {}".format(time, sort.__name__))


def test_all(list_of_functions, test_sequence, prompt="", count=100):
    """Test a series of sorting methods."""
    print(prompt)
    for sort in list_of_functions:
        test(sort, test_sequence, count)
    print()


def main():
    """Generate a random list and test sorting algorithms using it."""
    my_list = [random.randint(0,100) for _ in range(100)]
    almost_sorted = perform_swaps(my_list[:], 5)
    already_sorted = sorted(my_list)
    all_same = [1 for _ in range(100)]
    sorts = (sorted,
             pysort.bubble_naive,
             pysort.bubble_optimized,
             pysort.bubble_optimized_with_flag,
             pysort.bubble_final_position,
             pysort.insertion,
             pysort.insertion_optimized,
             pysort.insertion_optimized_alt,
             pysort.quick_random,
             pysort.quick_median,
             pysort.quick_inplace_random,
             pysort.quick_inplace_median,
             pysort.quick_inplace_repeat,
             pysort.merge_sort)
    test_all(sorts, my_list, "With a random shuffled list:", 10)
    test_all(sorts, almost_sorted, "With a list that is almost sorted:", 10)
    test_all(sorts, already_sorted, "With a list that is already sorted:", 10)
    test_all(sorts, all_same, "With a list containing all the same item:", 10)


if __name__ == "__main__":
    main()