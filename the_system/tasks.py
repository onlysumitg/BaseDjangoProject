from __future__ import absolute_import, unicode_literals
import random
from BaseDjangoProject import celery_app 
import celery

class MyTask(celery.Task):
 def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@celery_app.task(name="sum_two_numbers")
def add(x, y):
    print("calling add")
    return x + y


@celery_app.task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total


@celery_app.task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)