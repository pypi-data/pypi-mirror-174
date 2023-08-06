class PrometheusErrorBase(Exception):
    pass


class PrometheusMeticError(PrometheusErrorBase):
    def __init__(self, http_status, data):
        assert data['status'] == 'error'

        self.http_status = http_status
        self.data = data

    def __str__(self):
        return '%d %s: %s' % (
            self.http_status,
            self.data['errorType'], self.data['error']
        )


class PrometheusConnectionError(PrometheusErrorBase):
    pass
