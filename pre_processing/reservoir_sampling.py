"""
This is an example of a basic sampling algorithm called reservoir sampling.  It will fill a buffer, or reservoir,
to a pre-defined size and then randomly replace elements with decreasing probability as it continues to sample from
the stream.  The result is a representative sample of the stream using a pre-determined amount of memory.

According to the NIST, this is an in-memory version of the algorithm originally printed by Knuth in 1997:

Donald E. Knuth, The Art of Computer Programming, Addison-Wesley, volumes 1 and 2, 2nd edition, 1997.

He credits Alan G. Waterman.

In application, this sample would be continuously collected and held in memory for access by other processes or would
be returned at the end of parsing the arbitrarily-large stream.

Reservoir sampling is equivalent to solving the problem of picking K entries with uniform probability from a stream of
unknown size.

"""

import random


def reservoir_sample(input_iterator, sample_size):

    """
    :param input_iterator: The stream of values from which you want to sample.
    :param sample_size:  The size of the sample to create
    :return: A uniformly-distributed sample from the stream
    """

    sample = []

    for i, element in enumerate(input_iterator):
        if i < sample_size:
            sample.append(element)
        elif i >= sample_size and random.random() < sample_size/(i+1):
            replace = random.randint(0, len(sample) - 1)
            sample[replace] = element

    return sample
