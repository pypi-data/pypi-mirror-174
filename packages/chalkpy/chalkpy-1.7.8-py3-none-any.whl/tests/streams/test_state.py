from pydantic import BaseModel

from chalk.features import features
from chalk.state import State
from chalk.streams import KafkaSource, stream


@features
class StreamFeatures:
    scalar_feature: str


class KafkaMessage(BaseModel):
    val_a: str


s = KafkaSource(message=KafkaMessage)


@stream
def fn(message: s.Message, total: State[int]):
    total.update(4)
    return StreamFeatures(
        scalar_feature=message.val_a,
    )


def test_state_works():
    total = State[int]
    assert total.typ == int
