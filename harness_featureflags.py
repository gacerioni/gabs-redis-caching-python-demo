import time
from featureflags.evaluations.auth_target import Target
from featureflags.client import CfClient
from featureflags.util import log
from featureflags.config import with_base_url, with_events_url
import logging

# Set the logging level
log.setLevel(logging.INFO)


class FeatureFlagClient:
    def __init__(self, api_key="ebe7582a-88fc-4aac-980c-9dd20f1ba87b"):
        self.client = CfClient(api_key,
                               with_base_url("https://config.ff.harness.io/api/1.0"),
                               with_events_url("https://events.ff.harness.io/api/1.0"))
        self.target = Target(identifier='GABS_AWS_K3S', name="Gabs_AWS_k3s", attributes={"location": "brazil"})

    def get_demo_variation(self, flag_key='demo_mode', default_value={'min': '0.3', 'max': '0.5'}):
        result = self.client.json_variation(flag_key, self.target, default_value)
        log.debug("Result %s", result)
        return result


def main():
    log.debug("Starting example")
    api_key = "ebe7582a-88fc-4aac-980c-9dd20f1ba87b"
    ff_client = FeatureFlagClient(api_key)

    while True:
        demo_variation = ff_client.get_demo_variation()
        print("Demo variation:", demo_variation)
        time.sleep(3)


if __name__ == "__main__":
    main()
