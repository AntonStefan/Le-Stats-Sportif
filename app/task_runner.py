"""
The ThreadPool class initializes a thread pool with a specified number of threads
based on the TP_NUM_OF_THREADS environment variable or the hardware concurrency.
Tasks can be submitted to the pool, and the ThreadPool manages job results.
"""
import threading
import concurrent.futures
import os


class ThreadPool:
    """
    ThreadPool class to manage a pool of threads.
    """
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        num_threads = int(os.getenv('TP_NUM_OF_THREADS', os.cpu_count() or 1))
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
        self.job_results = {}  # Assign job_results to ThreadPool instance
        self.results_lock = threading.Lock()  # Create a lock for accessing job_results


    def submit(self, task, job_id, **kwargs):
        """
        Submit a task to the thread pool.
        """
        with self.results_lock:  # Acquire the lock before accessing shared resources
            future = self.executor.submit(task, **kwargs)
            self.job_results[job_id] = future


    def shutdown(self, wait=True):
        """
        Shut down the thread pool gracefully.
        """
        self.executor.shutdown(wait=wait)
