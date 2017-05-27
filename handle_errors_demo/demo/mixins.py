from .models import AsyncActionReport


class BaseErrorHandlerMixin:
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        AsyncActionReport.objects.filter(id=kwargs['async_action_report_id'])\
                                 .update(status=AsyncActionReport.FAILED,
                                         error_message=str(exc),
                                         error_traceback=einfo)

    def on_success(self, retval, task_id, args, kwargs):
        AsyncActionReport.objects.filter(id=kwargs['async_action_report_id'])\
                                 .update(status=AsyncActionReport.OK)
