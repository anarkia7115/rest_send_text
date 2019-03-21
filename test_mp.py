import unittest
import multiprocessing as mp
from multiprocessing import Pool, Queue
import time
from functools import partial
import pipeline

STOP_SIGNAL = "KILL"
PROCESS_NUM = 12

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
                break
            f.write(str(m) + '\n')
            f.flush()
        f.close()
    
    def test_mp_compute_ner(self):
        # initialize
        process_num = PROCESS_NUM

        manager = mp.Manager()
        q = manager.Queue()
        p = Pool(process_num)

        # start up listener (file writer)
        print("starting listener")
        output_file = "./data/test_mp_write1"
        import pipeline
        watcher = p.apply_async(pipeline.get_from_queue_and_write, 
            args=(q, output_file, STOP_SIGNAL))

        # start up worker (put data into queue)
        print("starting worker")
        nrows = 100
        key_column_name = 'nct_id'

        pipeline.load_and_compute_ner_multi_process(nrows, key_column_name, p, q)
        # merge
        print("job finished!")
        print("sending end signal")
        q.put(STOP_SIGNAL)
        p.close()
        p.join()

    def test_mp_write_to_one_file(self):
        # initialize
        process_num = PROCESS_NUM

        manager = mp.Manager()
        q = manager.Queue()
        p = Pool(process_num)

        # start up listener (file writer)
        print("starting listener")
        output_file = "./data/test_mp_write1"
        watcher = p.apply_async(pipeline.get_from_queue_and_write, 
            args=(q, output_file))

        # start up worker (put data into queue)
        print("starting worker")
        p.map(partial(self.dummy_worker, some_q=q), range(10))

        # merge
        print("job finished!")
        print("sending end signal")
        q.put(STOP_SIGNAL)
        p.close()
        p.join()

    def test_process_write(self):
        output_file = "./data/test_mp_write2"
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

    def test_hello_world(self):
        print("hello, world!")

        

