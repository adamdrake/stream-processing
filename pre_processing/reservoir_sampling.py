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

We can use the Law of Large Numbers to confirm that the means of the reservoir samples is close to the mean of the
streams.  In other words, the mean of the stream of integers up to 100 is 50, and the mean of multiple reservoir
samples on streams of that length and composition should also be close to 50.

>>> eps = 1
>>> stream_size = 100
>>> sample_size = 20
>>> stream_count = 1000
>>> streams = [[x for x in range(stream_size)] for y in range(stream_count)]
>>> samples = [reservoir_sample(x, sample_size) for x in streams]
>>> means = [sum(x)/len(x) for x in samples]
>>> abs(sum(means)/len(means) - stream_size/2) < eps
True


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
