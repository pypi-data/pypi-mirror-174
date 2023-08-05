import hmac
import os
import sys


class Site:
    def get_signature(self, data: bytes):
        """Return the signature of the given data."""
        return hmac.new(
            os.environb[b"EVENT_ROUTER_CIRCLECI_SECRET"], data, "sha256"
        ).hexdigest()

    def print_signature(self, data: bytes):
        print(self.get_signature(data))


class CircleCI(Site):
    pass
