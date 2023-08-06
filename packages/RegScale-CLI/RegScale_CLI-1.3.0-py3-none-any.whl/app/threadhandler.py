#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

"""Thread handler to create and start threads"""
from typing import Tuple
from concurrent.futures import ThreadPoolExecutor
from math import ceil


def create_threads(process, args: Tuple, thread_count: int, max_threads: int):
    """
    function to create x threads using ThreadPoolExecutor
    """
    # check to see if we need to go over the max threads
    if thread_count > max_threads:
        # get total # of thread groups
        thread_groups = ceil(thread_count / max_threads)
        threads_per_group = ceil(thread_count / thread_groups)
        with ThreadPoolExecutor(max_workers=threads_per_group) as executor:
            # iterate through each thread group and start the threads
            for thread in range(1, thread_groups):
                # start the number of threads allowed per group
                for i in range(threads_per_group):
                    executor.submit(process, args, i * thread)
    # start the number of threads in thread_count
    else:
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            # iterate and start the threads that were requested
            for thread in range(thread_count):
                executor.submit(process, args, thread)
