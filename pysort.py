import sys
import random


if sys.version_info[0] < 3:
    range = xrange


#Bubble sorts.
def bubble_naive(sequence):
    """
    A standard bubble sort implementation with no optimizations.
    Very bad and very slow.

    Inplace: Yes
    Time complexity: always O(n^2)
    """
    length = len(sequence)-1
    for _ in range(length):
        for i in range(length):
            if sequence[i] > sequence[i+1]:
                sequence[i],sequence[i+1] = sequence[i+1],sequence[i]


def bubble_optimized(sequence):
    """
    Performs much better than the naive implementation by itterating through
    one less item in the inner loop each time through the outer loop.

    Inplace: Yes
    Time complexity: always O(n^2)
    """
    for passes in range(len(sequence)-1, 0, -1):
        for i in range(passes):
            if sequence[i] > sequence[i+1]:
                sequence[i], sequence[i+1] = sequence[i+1], sequence[i]


def bubble_optimized_with_flag(sequence):
    """
    Performs negligibly worse than the bubble_optimized when the list is
    completely shuffled, but much better on lists that are almost sorted.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    for passes in range(len(sequence)-1, 0, -1):
        changed = False
        for i in range(passes):
            if sequence[i] > sequence[i+1]:
                sequence[i], sequence[i+1] = sequence[i+1], sequence[i]
                changed = True
        if not changed:
            break


def bubble_final_position(sequence):
    """
    Performs negligibly worse than the bubble_optimized when the list is
    completely shuffled, but much better on lists that are almost sorted.
    This implementation takes advantage of the fact that quite often multiple
    items find themselves in their final position after an iteration.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    swap_point = len(sequence)
    while swap_point:
        new_swap = 0
        for i in range(1, swap_point):
            if sequence[i-1] > sequence[i]:
                sequence[i-1], sequence[i] = sequence[i], sequence[i-1]
                new_swap = i
        swap_point = new_swap


#Insertion sorts.
def insertion(sequence):
    """
    Basic insertion sort. Still worst of O(n^2) but much faster than other
    algorithms of the same time complexity like bubble sort.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    for i in range(1,len(sequence)):
        while i>0 and sequence[i]<sequence[i-1]:
            sequence[i], sequence[i-1] = sequence[i-1], sequence[i]
            i -= 1


def insertion_optimized(sequence):
    """
    Improves performance by reducing the number of swaps required.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    for i,val in enumerate(sequence):
        while i>0 and val<sequence[i-1]:
            sequence[i] = sequence[i-1]
            i -= 1
        sequence[i] = val


def insertion_optimized_alt(sequence):
    """
    Significantly faster than insertion_optimized on a shuffled list.
    Slightly slower on an already sorted list.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    j = 0
    for i,val in enumerate(sequence):
        for j in range(i,-1,-1):
            if j>0 and val<sequence[j-1]:
                sequence[j] = sequence[j-1]
            else:
                break
        sequence[j] = val


#Quick sorts.
def quick_random(sequence):
    """
    Quick sort with random pivot selection.  Far superior to insertion and
    bubble sort in general cases, but quite a bit worse in cases where the list
    is already sorted.

    Inplace: No
    Time complexity: best O(n), avg O(nlogn), worst O(n^2)
    """
    length = len(sequence)
    if length < 2:
        return sequence
    pivot = sequence.pop(random.randrange(length))
    above = []
    below = []
    for item in sequence:
        if item > pivot:
            above.append(item)
        else:
            below.append(item)
    return quick_random(below)+[pivot]+quick_random(above)


def quick_median(sequence):
    """
    Quick sort with median-of-3 pivot selection.
    Not much noticable difference over random pivot selection.

    Inplace: No
    Time complexity: best O(n), avg O(nlogn), worst O(n^2)
    """
    length = len(sequence)
    if length < 2:
        return sequence
    pivot_index = median_of_three(sequence, 0, length-1)
    pivot = sequence.pop(pivot_index)
    above = []
    below = []
    for item in sequence:
        if item > pivot:
            above.append(item)
        else:
            below.append(item)
    return quick_median(below)+[pivot]+quick_median(above)


def quick_inplace_random(sequence, left=0, right=None):
    """
    In-place quicksort with random pivot selection.

    Inplace: Yes
    Time complexity: best O(n), avg O(nlogn), worst O(n^2)
    """
    if right is None:
        right = len(sequence)-1
    if left < right:
        pivot_ind = random.randint(left,right)
        pivot_new_ind = partition(sequence, left, right, pivot_ind)
        quick_inplace_random(sequence, left, pivot_new_ind-1)
        quick_inplace_random(sequence, pivot_new_ind+1, right)


def quick_inplace_median(sequence, left=0, right=None):
    """
    In-place quicksort with median-of-3 pivot selection.

    Inplace: Yes
    Time complexity: best O(n), avg O(nlogn), worst O(n^2)
    """
    if right is None:
        right = len(sequence)-1
    if left < right:
        pivot_ind = median_of_three(sequence, left, right)
        pivot_new_ind = partition(sequence, left, right, pivot_ind)
        quick_inplace_median(sequence, left, pivot_new_ind-1)
        quick_inplace_median(sequence, pivot_new_ind+1, right)


def partition(sequence, left, right, pivot_ind):
    """This is the key to the in-place quicksort."""
    pivot = sequence[pivot_ind]
    sequence[pivot_ind], sequence[right] = sequence[right], sequence[pivot_ind]
    store_ind = left
    for i in range(left,right):
        if sequence[i] <= pivot:
            sequence[i], sequence[store_ind] = sequence[store_ind], sequence[i]
            store_ind += 1
    sequence[store_ind], sequence[right] = sequence[right], sequence[store_ind]
    return store_ind


def median_of_three(sequence, left, right):
    """Find the index (with respect to sequence) of the middle of three."""
    mid = (left+right)//2
    values = {sequence[left] : left,
              sequence[mid] : mid,
              sequence[right] : right}
    median = max(min(sequence[left],sequence[mid]),
                 min(max(sequence[left],sequence[mid]),sequence[right]))
    return values[median]


#Inefficient/novelty sorts.
def bogo(sequence):
    """
    Check if the list is in order; if it is not, shuffle the list.
    Not intended to be a realistic method of sorting.

    This algorithm is so bad that a list of even 10 elements can take
    more than 15 seconds to sort (as such it is not included in the
    algorithms automatically tested in test_sorts.py).

    Inplace: Yes
    Time complexity: O(n*n!)
    """
    while any(sequence[i]>sequence[i+1] for i in range(len(sequence)-1)):
        random.shuffle(sequence)
    return sequence


