from celery import Task, Signature

from .models import AsyncActionReport


def get_signature_and_make_system_call(*,
                                       action: str,
                                       task: Task,
                                       task_kwargs: dict={}) -> Signature:
    async_action_report = AsyncActionReport.objects.create(
        action=action,
        system_call=True
    )

    task_kwargs['async_action_report_id'] = async_action_report.id

    return task.s(**task_kwargs)
