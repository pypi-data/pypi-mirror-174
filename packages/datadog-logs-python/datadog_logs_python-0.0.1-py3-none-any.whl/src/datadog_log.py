from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


class DataDog:
    def __init__(self, source, host, service):
        self.source = source
        self.host = host
        self.service = service

    def info(self, logs):
        self.common(logs, 'info')

    def warn(self, logs):
        self.common(logs, 'warn')

    def error(self, logs):
        self.common(logs, 'error')

    def common(self, msg, level):
        body = HTTPLog(
            [
                HTTPLogItem(
                    ddsource=self.source,
                    ddtags="env:dev,version:5.1",
                    hostname=self.host,
                    message=msg,
                    service=self.service,
                    status=level,
                    functionname="hello world"
                ),
            ]
        )
        configuration = Configuration()
        with ApiClient(configuration) as api_client:
            api_instance = LogsApi(api_client)
            response = api_instance.submit_log(body=body)
            print(response)
