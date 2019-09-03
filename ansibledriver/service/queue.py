from multiprocessing import JoinableQueue
import logging

from ignition.service.framework import Service
from ignition.service.lifecycle import LifecycleDriverCapability
from ignition.model.lifecycle import LifecycleExecuteResponse

logger = logging.getLogger(__name__)

SHUTDOWN_MESSAGE = 'SHUTDOWN'

class RequestQueue(Service):
  def __init__(self):
    self.request_queue = JoinableQueue()

  def next(self):
    try:
      return self.request_queue.get(True)
    except EOFError as e:
      return None
    except OSError as e:
      return None

  def queue_status(self):
    return {
      'status': 'ok',
      'size': self.request_queue.qsize()
    }

  def size(self):
    return self.request_queue.qsize()

  def put(self, request):
    self.request_queue.put(request)

  def shutdown(self):
    self.put(SHUTDOWN_MESSAGE)
    # allow the queue to drain
    #self.request_queue.join()
    # self.request_queue.close()

  def task_done(self):
    self.request_queue.task_done()