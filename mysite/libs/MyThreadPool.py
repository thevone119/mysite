# -*- coding: utf-8 -*-
import queue
import threading
import time
#实现先进先执行的线程处理机制，方便对大量的数据进行线程处理
#没有采用线程池，线程数太多，可能有内存问题？
#实现线程的阻塞，达到多少定义的N个线程，则调用会阻塞
class MyThreadPool:
    threadFactory = threading.Thread
    currentThread = staticmethod(threading.currentThread)

    def __init__(self, maxsize=20, name=None):
        self.q = queue.Queue(maxsize)
        self.workingq = queue.Queue(maxsize)
        self.max = maxsize
        self.name = name

    def callInThread(self, func, *args, **kw):
        o = (func, args, kw, None)
        self.q.put(o)
        self.workingq.put(1)
        name = "PoolThread-%s" % (self.name or id(self))
        newThread = self.threadFactory(target=self._worker, name=name)
        newThread.start()





    def _worker(self):
        ct = self.currentThread()
        o = self.q.get()
        function, args, kwargs, onResult = o
        del o
        try:
            result = function(*args, **kwargs)
            success = True
        except:
            success = False
            if onResult is None:
                pass

            else:
                pass
        finally:
            self.workingq.get()
        del function, args, kwargs

        if onResult is not None:
            try:
                onResult(success, result)
            except:
                # context.call(ctx, log.err)
                pass

        del onResult


    def wait(self):
        while True:
            if self.workingq.empty():
                return
            else:
                time.sleep(0.1)




if __name__ == '__main__':
    def testfunc1():
        time.sleep(2)
        print("test")
        return False

    pool = MyThreadPool(10)

    for i in range(1,10000):
        pool.callInThread(testfunc1)
        print("call:",i)

    pool.wait()
    print("wait:")
