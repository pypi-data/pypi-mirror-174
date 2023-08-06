import time
from urllib.parse import urljoin

import httpx

from . import errors
from .model import parse_data, InstantVector, Scalar

DEFAULT_USER_AGENT = 'Python Aio Prometheus Client'
TIMEOUT = 10 * 60


class PrometheusClient:
    def __init__(self, base_url, user_agent=DEFAULT_USER_AGENT):
        self.base_url = base_url
        self.user_agent = user_agent

    async def query(self, metric):
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(
                    urljoin(self.base_url, 'api/v1/query'),
                    params={
                        'query': metric,
                        'time': str(time.time())
                    },
                    headers={'User-Agent': self.user_agent},
                    timeout=TIMEOUT,
                )
            except Exception as e:
                raise errors.PrometheusConnectionError('request fail') from e

            if r.status_code == 400:
                data = r.json()
                raise errors.PrometheusMeticError(r.status_code, data)

            r.raise_for_status()
            data = r.json()

        if data['status'] != 'success':
            raise ValueError('invalid data: %s' % data)

        return parse_data(data['data'])

    async def query_value(self, metric):
        data = await self.query(metric)
        if isinstance(data, InstantVector):
            series_count = len(data.series)
            if series_count != 1:
                raise ValueError('series count incorrect: %d' % series_count)

            return data.series[0].value.value
        elif isinstance(data, Scalar):
            return data.value
        else:
            raise TypeError('unknown data type: %s' % type(data))
