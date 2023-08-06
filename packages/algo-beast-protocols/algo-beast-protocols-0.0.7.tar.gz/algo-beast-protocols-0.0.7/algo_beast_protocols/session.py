from typing import Protocol


class Session(Protocol):
  id: int
  user_id: int
  project_id: int
  broker_config_id: int
  mode: str