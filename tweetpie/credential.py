import dataclasses

@dataclasses.dataclass
class Credential:

    consumer_key: str
    consumer_secret: str
    access_token: str
    access_secret: str