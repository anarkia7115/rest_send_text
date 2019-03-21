import unittest
import multiprocessing as mp
from multiprocessing import Pool, Queue
import time
from functools import partial

STOP_SIGNAL="KILL"

class TestMultiProcess(unittest.TestCase): 

    @staticmethod
    def dummy_worker(content, some_q):
        print("dummy working")
        time.sleep(1)
        some_q.put(content)
        return content

    @staticmethod
    def dummy_listener(some_q, output_file):
        f = open(output_file, 'w')
        while True:
            print("waiting~")
            m = some_q.get()
            if m == STOP_SIGNAL:
                f.write('killed')
                break
            f.write(str(m) + '\n')
            f.flush()
        f.close()
    
    def test_mp_write_to_one_file(self):
        import multiprocessing, logging
        mpl = multiprocessing.log_to_stderr()
        mpl.setLevel(multiprocessing.SUBDEBUG)

        # initialize
        process_num = 2
        q = mp.Queue()
        p = Pool(process_num)

        # start up listener (file writer)
        print("starting listener")
        output_file = "./test_mp_write"
        from pipeline import get_from_queue_and_write
        watcher = p.apply_async(
            self.dummy_listener, 
            args=(q, output_file))

        # start up worker (put data into queue)
        print("starting worker")
        jobs = []

        for i in range(2):
            job = p.apply_async(self.dummy_worker, (i, q))
            jobs.append(job)

        p.map(
            partial(
                self.dummy_worker, 
                some_q=q), 
            range(10)
        )

        for job in jobs:
            job.get()

        # merge
        print("job finished!")
        print("sending end signal")
        q.put(STOP_SIGNAL)
        p.close()
        p.join()

    def test_process_write(self):
        output_file = "./test_mp_write"
        i = 123
        q = mp.Queue()

        listener_process = mp.Process(target=self.dummy_listener, args=(q, output_file))
        worker_process = mp.Process(target=self.dummy_worker, args=(i, q))
        print("listener started")
        listener_process.start()
        print("worker started")
        worker_process.start()
        worker_process.join()

        q.put(STOP_SIGNAL)
        listener_process.join()

        

