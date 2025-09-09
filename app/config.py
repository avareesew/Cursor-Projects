import os


MIN_PICKS = int(os.getenv("DWTS_MIN_PICKS", "3"))
DATA_CONTESTANTS_PATH = os.getenv("DWTS_CONTESTANTS_PATH", "/workspace/data/contestants.json")
