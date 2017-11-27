from functools import wraps
from collections import Iterable

from celery import Signature


def chainable(chain_wannabe):
    """
    USAGE:
    To decorate functions that want to behave like Celery chains.

    WHY?:
    The purpose of the chains is to make something like this `chain(t1, t2, ..., tn)`

    In some case you may want to have a `chain` inside the "mother" `chain` (t1 = chain()).

    The problem is that the task after the inner chain task will be called *immediately* after
    the call (`.delay()`) of the inner chain because it always returns:
    1) None -> if the chain task doesn't return anything
    2) (Celery.AsyncAction, foo) -> if the chain task return something (foo)
    """
    @wraps(chain_wannabe)
    def wrapper(*args, **kwargs):
        signatures = chain_wannabe(*args, **kwargs)
        error_msg = 'Functions decorated with `chainable` must return Signature instances.'

        if not isinstance(signatures, Iterable):
            raise ValueError(error_msg)

        for task_sig in chain_wannabe(*args, **kwargs):
            if not isinstance(task_sig, Signature):
                raise ValueError(error_msg)

        return signatures
    return wrapper
