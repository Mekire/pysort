"""
Various sorting algorithms implemented in python.
This is purely an academic excercise as no sorting implementation written
in python will possibly out perform the builtin implementation of timsort.
Even so, writing algorithms such as these is very helpful in understanding
time complexity and algorithm design.

For an overview of sorting algorithms please see the Wikipedia page:
    http://en.wikipedia.org/wiki/Sorting_algorithm

Free for all purposes.  No warranty expressed or implied.

-Written by Sean J McKiernan
"""

import sys
import random


if sys.version_info[0] < 3:
    range = xrange


class Bubble(object):
    """
    Contains various bubble sort implementations.

    http://en.wikipedia.org/wiki/Bubble_sort
    """

    @staticmethod
    def bubble_naive(array):
        """
        A standard bubble sort implementation with no optimizations.
        Very bad and very slow.

        Inplace: Yes
        Time complexity: always O(n^2)
        """
        length = len(array)-1
        for _ in range(length):
            for i in range(length):
                if array[i] > array[i+1]:
                    array[i],array[i+1] = array[i+1],array[i]

    @staticmethod
    def bubble_optimized(array):
        """
        Performs much better than the naive implementation by itterating
        through one less item in the inner loop each time through the outer
        loop.

        Inplace: Yes
        Time complexity: always O(n^2)
        """
        for passes in range(len(array)-1, 0, -1):
            for i in range(passes):
                if array[i] > array[i+1]:
                    array[i], array[i+1] = array[i+1], array[i]

    @staticmethod
    def bubble_optimized_with_flag(array):
        """
        Performs negligibly worse than the bubble_optimized when the list is
        completely shuffled, but much better on lists that are almost sorted.

        Inplace: Yes
        Time complexity: best O(n), avg and worst O(n^2)
        """
        for passes in range(len(array)-1, 0, -1):
            changed = False
            for i in range(passes):
                if array[i] > array[i+1]:
                    array[i], array[i+1] = array[i+1], array[i]
                    changed = True
            if not changed:
                break

    @staticmethod
    def bubble_final_position(array):
        """
        Performs negligibly worse than the bubble_optimized when the list is
        completely shuffled, but much better on lists that are almost sorted.
        This implementation takes advantage of the fact that quite often
        multiple items find themselves in their final position after an
        iteration.

        Inplace: Yes
        Time complexity: best O(n), avg and worst O(n^2)
        """
        swap_point = len(array)
        while swap_point:
            new_swap = 0
            for i in range(1, swap_point):
                if array[i-1] > array[i]:
                    array[i-1], array[i] = array[i], array[i-1]
                    new_swap = i
            swap_point = new_swap


class Insertion(object):
    """
    Contains various insertion sort implementations.

    http://en.wikipedia.org/wiki/Insertion_sort
    """

    @staticmethod
    def insertion(array):
        """
        Basic insertion sort. Still worst of O(n^2) but much faster than other
        algorithms of the same time complexity like bubble sort.

        Inplace: Yes
        Time complexity: best O(n), avg and worst O(n^2)
        """
        for i in range(1,len(array)):
            while i>0 and array[i]<array[i-1]:
                array[i], array[i-1] = array[i-1], array[i]
                i -= 1

    @staticmethod
    def insertion_optimized(array):
        """
        Improves performance by reducing the number of swaps required.

        Inplace: Yes
        Time complexity: best O(n), avg and worst O(n^2)
        """
        for i,val in enumerate(array):
            while i>0 and val<array[i-1]:
                array[i] = array[i-1]
                i -= 1
            array[i] = val

    @staticmethod
    def insertion_optimized_alt(array):
        """
        Significantly faster than insertion_optimized on a shuffled list.
        Slightly slower on an already sorted list.

        Inplace: Yes
        Time complexity: best O(n), avg and worst O(n^2)
        """
        j = 0
        for i,val in enumerate(array):
            for j in range(i,-1,-1):
                if j>0 and val<array[j-1]:
                    array[j] = array[j-1]
                else:
                    break
            array[j] = val


class Quick(object):
    """
    Contains various quick sort implementations.

    http://en.wikipedia.org/wiki/Quicksort
    """

    @staticmethod
    def quick_random(array):
        """
        Quick sort with random pivot selection.  Far superior to insertion and
        bubble sort in general cases, but quite a bit worse in cases where the
        list is already sorted.

        Inplace: No
        Time complexity: best O(n), avg O(nlogn), worst O(n^2)
        """
        length = len(array)
        if length < 2:
            return array
        pivot = array.pop(random.randrange(length))
        above = []
        below = []
        for item in array:
            if item > pivot:
                above.append(item)
            else:
                below.append(item)
        return Quick.quick_random(below)+[pivot]+Quick.quick_random(above)

    @staticmethod
    def quick_median(array):
        """
        Quick sort with median-of-3 pivot selection.
        Not much noticable difference over random pivot selection.

        Inplace: No
        Time complexity: best O(n), avg O(nlogn), worst O(n^2)
        """
        length = len(array)
        if length < 2:
            return array
        pivot_index = Quick.median_of_three(array, 0, length-1)
        pivot = array.pop(pivot_index)
        above = []
        below = []
        for item in array:
            if item > pivot:
                above.append(item)
            else:
                below.append(item)
        return Quick.quick_median(below)+[pivot]+Quick.quick_median(above)

    @staticmethod
    def quick_inplace_random(array, left=0, right=None):
        """
        In-place quicksort with random pivot selection.

        Uses the helper function partition().

        Inplace: Yes
        Time complexity: best O(n), avg O(nlogn), worst O(n^2)
        """
        if right is None:
            right = len(array)-1
        if left < right:
            pivot_ind = random.randint(left,right)
            pivot_new_ind = Quick.partition(array, left, right, pivot_ind)
            Quick.quick_inplace_random(array, left, pivot_new_ind-1)
            Quick.quick_inplace_random(array, pivot_new_ind+1, right)

    @staticmethod
    def quick_inplace_median(array, left=0, right=None):
        """
        In-place quicksort with median-of-3 pivot selection.

        Uses the helper function median_of_three() and partition().

        Inplace: Yes
        Time complexity: best O(n), avg O(nlogn), worst O(n^2)
        """
        if right is None:
            right = len(array)-1
        if left < right:
            pivot_ind = Quick.median_of_three(array, left, right)
            pivot_new_ind = Quick.partition(array, left, right, pivot_ind)
            Quick.quick_inplace_median(array, left, pivot_new_ind-1)
            Quick.quick_inplace_median(array, pivot_new_ind+1, right)

    @staticmethod
    def quick_inplace_repeat(array, low=0, high=None):
        """
        In-place quicksort with median-of-3 pivot selection.
        Uses an optimization specifically for lists that contain repeated
        elements.  With the other methods a list of all the same item
        automatically causes worst O(n^2) performance.  Here we avoid this at
        the cost of slightly longer average times.

        Uses helper functions median_of_three() and partition_repeat().

        Inplace: Yes
        Time complexity: best O(n), avg O(nlogn), worst O(n^2)
        """
        if high is None:
            high = len(array)-1
        if low < high:
            pivot_ind = Quick.median_of_three(array, low, high)
            left, right = Quick.partition_repeat(array, low, high, pivot_ind)
            Quick.quick_inplace_repeat(array, low, left)
            Quick.quick_inplace_repeat(array, right, high)

    @staticmethod
    def partition(array, left, right, pivot_ind):
        """
        This is the key to the in-place quicksort.

        Used in quick_inplace_random() and quick_inplace_median().
        """
        pivot = array[pivot_ind]
        array[pivot_ind], array[right] = array[right], array[pivot_ind]
        index = left
        for i in range(left,right):
            if array[i] <= pivot:
                array[i], array[index] = array[index], array[i]
                index += 1
        array[index], array[right] = array[right], array[index]
        return index

    @staticmethod
    def partition_repeat(array, left, right, pivot_ind):
        """
        Partitioner that allows quicksort to avoid worst case performance on a
        list that contains numerous repeated elements.

        Used in quick_inplace_repeat().
        """
        pivot = array[pivot_ind]
        index = left
        for i in range(left, right+1):
            if array[i] < pivot:
                array[i], array[index] = array[index], array[i]
                index += 1
        left = index
        for i in range(left, right+1):
            if array[i] == pivot:
                array[i], array[index] = array[index], array[i]
                index += 1
        return left, index

    @staticmethod
    def median_of_three(array, left, right):
        """
        Find the index (with respect to array) of the median of the first,
        last, and middle values.

        Used in quick_median(), quick_inplace_median(), and
        quick_inplace_repeat().
        """
        mid = (left+right)//2
        if array[left] > array[mid]:
            if array[mid] > array[right]:
                return mid
            elif array[left] > array[right]:
                return right
            return left
        elif array[left] > array[right]:
            return left
        elif array[mid] > array[right]:
            return right
        return mid


class Merge(object):
    """
    Contains various merge sort implementations.

    http://en.wikipedia.org/wiki/Merge_sort
    """

    @staticmethod
    def merge_sort(array):
        """
        A basic implementation of merge sort.  Despite enjoying a lower worst
        case time complexity, quick sort often outperforms merge sort in
        practical cases.

        Uses the helper function merge().

        Inplace: No
        Time complexity: all O(nlogn)
        """
        length = len(array)
        if length < 2:
            return array
        middle = length//2
        left = Merge.merge_sort(array[:middle])
        right = Merge.merge_sort(array[middle:])
        return Merge.merge(left, right)

    @staticmethod
    def merge(left, right):
        """Merges the values in left and right in the correct order."""
        new = []
        left_index, right_index = 0, 0
        len_left, len_right = len(left), len(right)
        while left_index < len_left and right_index < len_right:
            if left[left_index] <= right[right_index]:
                new.append(left[left_index])
                left_index += 1
            else:
                new.append(right[right_index])
                right_index += 1
        new += left[left_index:]
        new += right[right_index:]
        return new


class Heap(object):
    """
    Contains various heap sort implementations.

    http://en.wikipedia.org/wiki/Heapsort
    """

    @staticmethod
    def heap_sort(array):
        """
        A basic implementation of heap sort.  As with merge sort, heap sort is
        also often out performed by quick sort in practical cases.

        Uses helper functions heapify() and sift_down()

        Inplace: Yes
        Time complexity: all O(nlogn)
        """
        highest_index = len(array)-1
        Heap.heapify(array, highest_index)
        for end in range(highest_index, 0, -1):
            array[end], array[0] = array[0], array[end]
            Heap.sift_down(array, 0, end-1)

    @staticmethod
    def heapify(array, highest_index):
        """
        Take an array and put it in heap order.  Operates inplace.

        Used in heap_sort().
        Uses sift_down().
        """
        first = (highest_index-1)//2
        for start in range(first, -1, -1):
            Heap.sift_down(array, start, highest_index)

    @staticmethod
    def sift_down(array, start, end):
        """
        Change position of item in list until it is correctly placed in heap.

        Used by heap_sort() (and heapify()).
        """
        root = start
        while root*2+1 <= end:
            child = root*2+1
            swap = root
            if array[swap] < array[child]:
                swap = child
            if child+1 <= end and array[swap] < array[child+1]:
                swap = child+1
            if swap != root:
                array[root], array[swap] = array[swap], array[root]
                root = swap
            else:
                break


class Other(object):
    """
    This class contains various inefficient or novelty/humorous sorting
    methods.  Due to inefficiency these are not included in those automatically
    tested in test_sorts.py.
    """

    @staticmethod
    def bogo(array):
        """
        http://en.wikipedia.org/wiki/Bogosort

        Check if the list is in order; if it is not, shuffle the list.
        This algorithm is so bad that a list of even 10 elements can take
        more than 15 seconds to sort.

        Inplace: Yes
        Time complexity: O(n*n!)
        """
        while any(array[i]>array[i+1] for i in range(len(array)-1)):
            random.shuffle(array)
