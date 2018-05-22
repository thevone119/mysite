# -*- coding: utf-8 -*-
import queue
import threading
import time
import threadpool
#实现先进先执行的线程处理机制，方便对大量的数据进行线程处理
#没有采用线程池，线程数太多，可能有内存问题？
#实现线程的阻塞，达到多少定义的N个线程，则调用会阻塞

# 引入锁
THREAD_L = threading.Lock()

class MyThreadPool:
    threadFactory = threading.Thread
    currentThread = staticmethod(threading.currentThread)

    def __init__(self, maxsize=20, name=None):
        self.q = queue.Queue(maxsize)
        self.workingq = queue.Queue(maxsize)
        self.max = maxsize
        self.name = name

    def callInThread(self, func, *args, **kw):
        self.workingq.put(1)
        o = (func, args, kw, None)
        self.q.put(o)
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
        except Exception as e:
            print("线程执行错误",function,e)
            success = False
            if onResult is None:
                pass

            else:
                pass
        finally:
            self.workingq.get()
            pass
        del function, args, kwargs

        if onResult is not None:
            try:
                onResult(success, result)
            except:
                # context.call(ctx, log.err)
                pass

        del onResult

    #等待结束
    def wait(self):
        while True:
            if self.workingq.empty():
                return
            time.sleep(0.1)

class MyThreadPool2:
    def __init__(self, maxsize=20, q_size=20,resq_size=200,name=None):
        #self.workingq = queue.Queue(maxsize)
        self.tpool = threadpool.ThreadPool(maxsize,q_size=q_size,resq_size=resq_size)

    def callInThread(self, func, *args, **kw):
        alist = []
        for a in args:
            alist.append(a)
        requests = threadpool.makeRequests(func,args_list=alist)
        [self.tpool.putRequest(req) for req in requests]


    def wait(self):
        self.tpool.wait()

if __name__ == '__main__':
    def testfunc1(str=None):
        time.sleep(2)
        print("test")
        return False

    pool = MyThreadPool(10)

    for i in range(1,1000):
        print("call:", i)
        pool.callInThread(testfunc1)

    pool.wait()


    print("wait:")
