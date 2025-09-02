"""
Some example code (not executed) from
http://stackoverflow.com/questions/11983938/python-appending-to-same-file-from-multiple-threds
General advice is that files should only be processed in one thread
(communicating to other threads). Perhaps more simply,locking the files will
work.

This is in the context of graphing older filed data while still running the logger.
"""
from __future__ import print_function
import threading
import Queue

class PrintThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def printfiles(self, p):
        for path, dirs, files in os.walk(p):
            for f in files:
                print(f, file=output)

    def run(self):
        while True:
            result = self.queue.get()
            self.printfiles(result)
            self.queue.task_done()

class ProcessThread(threading.Thread):
    def __init__(self, in_queue, out_queue):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            path = self.in_queue.get()
            result = self.process(path)
            self.outqueue.put(result)
            self.in_queue.task_done()

    def process(self, path):
	#Do the processing job here    
        return


pathqueue = Queue.Queue()
resultqueue = Queue.Queue()
paths = getThisFromSomeWhere()

output = codecs.open('file', 'a')

# spawn threads to process
for i in range(0, 5):
    t = ProcessThread(pathqueue, resultqueue)
    t.setDaemon(True)
    t.start()

# spawn threads to print
t = PrintThread(resultqueue)
t.setDaemon(True)
t.start()

# add paths to queue
for path in paths:
    pathqueue.put(path)

# wait for queue to get empty
pathqueue.join()
resultqueue.join()