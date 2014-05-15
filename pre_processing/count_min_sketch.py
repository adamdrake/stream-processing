"""
cmsketch.py

An implementation of count-min sketching from the paper due to Cormode and
Muthukrishnan 2005

Code based on work by Joseph Kibe

https://tech.shareaholic.com/2012/12/03/the-count-min-sketch-how-to-count-over-large-keyspaces-when-about-right-is-good-enough/

with some refactoring to remove the numpy dependency and achieve Python 3 compatibility.

From the Wikipedia Entry:

The Count–min sketch (or CM sketch) is a probabilistic sub-linear space streaming algorithm which can be used to
summarize a data stream in many different ways. The algorithm was invented in 2003 by
Graham Cormode and S. Muthu Muthukrishnan.[1]

Count–min sketches are somewhat similar to Bloom filters; the main distinction is that Bloom filters represent sets,
while CM sketches represent multisets and frequency tables.
"""

import sys
import random
import math
import heapq

BIG_PRIME = 9223372036854775783


class Sketch:
    def __init__(self, delta, epsilon, k):
        """
        Setup a new count-min sketch with parameters delta, epsilon and k

        The parameters delta and epsilon control the accuracy of the
        estimates of the sketch

        Cormode and Muthukrishnan prove that for an item i with count a_i, the
        estimate from the sketch a_i_hat will satisfy the relation

        a_hat_i <= a_i + epsilon * ||a||_1

        with probability at least 1 - delta, where a is the the vector of all
        all counts and ||x||_1 is the L1 norm of a vector x

        Parameters
        ----------
        delta : float
            A value in the unit interval that sets the precision of the sketch
        epsilon : float
            A value in the unit interval that sets the precision of the sketch
        k : int
            A positive integer that sets the number of top items counted

        Examples
        --------
        >>> s = Sketch(10**-7, 0.005, 40)

        Raises
        ------
        ValueError
            If delta or epsilon are not in the unit interval, or if k is
            not a positive integer
        """

        if delta <= 0 or delta >= 1:
            raise ValueError("delta must be between 0 and 1, exclusive")
        if epsilon <= 0 or epsilon >= 1:
            raise ValueError("epsilon must be between 0 and 1, exclusive")
        if k < 1:
            raise ValueError("k must be a positive integer")

        self.w = int(math.ceil(math.exp(1) / epsilon))
        self.d = int(math.ceil(math.log(1 / delta)))
        self.k = k
        self.hash_functions = [self.__generate_hash_function() for i in range(self.d)]
        self.count = [[int(0) for x in range(self.w)] for y in range(self.d)]
        self.heap, self.top_k = [], {}  # top_k => [estimate, key] pairs

    def update(self, key, increment):
        """
        Updates the sketch for the item with name of key by the amount
        specified in increment

        Parameters
        ----------
        key : string
            The item to update the value of in the sketch
        increment : integer
            The amount to update the sketch by for the given key

        Examples
        --------
        >>> s = Sketch(10**-7, 0.005, 40)
        >>> s.update('http://www.cnn.com/', 1)
        """

        for row, hash_function in enumerate(self.hash_functions):
            column = hash_function(abs(hash(key)))
            self.count[row][column] += increment

        self.update_heap(key)

    def update_heap(self, key):
        """
        Updates the class's heap that keeps track of the top k items for a
        given key

        For the given key, it checks whether the key is present in the heap,
        updating accordingly if so, and adding it to the heap if it is
        absent

        Parameters
        ----------
        key : string
            The item to check against the heap
        """
        estimate = self.get(key)

        if not self.heap or estimate >= self.heap[0][0]:
            if key in self.top_k:
                old_pair = self.top_k.get(key)
                old_pair[0] = estimate
                heapq.heapify(self.heap)
            else:
                if len(self.top_k) < self.k:
                    heapq.heappush(self.heap, [estimate, key])
                    self.top_k[key] = [estimate, key]
                else:
                    new_pair = [estimate, key]
                    old_pair = heapq.heappushpop(self.heap, new_pair)
                    del self.top_k[old_pair[1]]
                    self.top_k[key] = new_pair

    def get(self, key):
        """
        Fetches the sketch estimate for the given key

        Parameters
        ----------
        key : string
            The item to produce an estimate for

        Returns
        -------
        estimate : int
            The best estimate of the count for the given key based on the
            sketch

        Examples
        --------
        >>> s = Sketch(10**-7, 0.005, 40)
        >>> s.update('http://www.cnn.com/', 1)
        >>> s.get('http://www.cnn.com/')
        1
        >>> s.update('http://www.cnn.com/', 10)
        >>> s.get('http://www.cnn.com/')
        11
        """
        value = sys.maxsize
        for row, hash_function in enumerate(self.hash_functions):
            column = hash_function(abs(hash(key)))
            value = min(self.count[row][column], value)

        return value

    def __random_parameter(self):
        """
        Needed to provide two numbers to generate the pairwise-independent hash functions
        """
        return random.randrange(0, BIG_PRIME - 1)

    def __generate_hash_function(self):
        """
        Returns a hash function from a family of pairwise-independent hash
        functions
        """

        a, b = self.__random_parameter(), self.__random_parameter()
        return lambda x: (a * x + b) % BIG_PRIME % self.w

if __name__ == '__main__':
    print("blah")