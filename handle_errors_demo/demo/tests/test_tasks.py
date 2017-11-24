from unittest import TestCase, mock


class FetchDataAndStoreItTests(TestCase):
    @mock.patch('handle_errors_demo.demo.tasks.fetch_data.s')
    @mock.patch('handle_errors_demo.demo.tasks.store_data.s')
    def test_task_updates_async_action_report_on_success(self,
                                                         fetch_data_mock,
                                                         store_data_mock):
        fetch_data_mock.return_value = mock.MagicMock(fetched_data={})
        store_data_mock.return_value = 1
