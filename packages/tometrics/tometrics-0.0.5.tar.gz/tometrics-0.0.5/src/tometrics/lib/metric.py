class Metric:
    def __init__(self, name: str,
        timestamp_ns: int,
        data: map = {},
        metadata: map = {},):
        self.name = name
        self.timestamp_ns = timestamp_ns
        self.data = data
        self.metadata = metadata
