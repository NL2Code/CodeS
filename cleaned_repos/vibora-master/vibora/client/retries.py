class RetryStrategy:
    __slots__ = ("network_failures", "responses")

    def __init__(self, network_failures: dict = None, responses: dict = None):
        """

        :param network_failures:
        :param responses:
        """

        self.network_failures = network_failures or {"GET": 1}

        # Retry after an specific status_code is found.
        self.responses = responses or {}

    def clone(self) -> "RetryStrategy":
        return RetryStrategy(
            network_failures=self.network_failures.copy(),
            responses=self.responses.copy(),
        )
