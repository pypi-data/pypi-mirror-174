from dataclasses import dataclass
from typing import List


@dataclass
class Scalar:
    timestamp: float
    value: float

    @classmethod
    def from_data(cls, data):
        return cls(
            timestamp=data[0],
            value=float(data[1])
        )


@dataclass
class InstantSeries:
    metric: dict
    value: Scalar

    @classmethod
    def from_data(cls, data):
        return cls(
            metric=data['metric'],
            value=Scalar.from_data(data['value'])
        )


@dataclass
class InstantVector:
    series: List[InstantSeries]

    @classmethod
    def from_data(cls, data):
        return cls(
            series=[
                InstantSeries.from_data(i)
                for i in data
            ]
        )


def parse_data(data):
    result_type = data['resultType']
    result = data['result']

    if result_type == 'scalar':
        return Scalar.from_data(result)
    elif result_type == 'vector':
        return InstantVector.from_data(result)
