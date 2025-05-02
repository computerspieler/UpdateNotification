from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import subprocess

class NotificationLevel(Enum):
    LOW=0
    NORMAL=1
    HIGH=2
  
    def __str__(self):
        cls = NotificationLevel
        if self == cls.LOW: return 'low'
        elif self == cls.NORMAL: return 'normal'
        elif self == cls.HIGH: return 'critical'
        else: raise ValueError()

@dataclass
class Notification:
    title: str
    body: str
    level: NotificationLevel
    cmd_on_click: list[str]

    def __call__(self):
        subprocess.run(["notify-send",
            "-u", str(self.level),
            self.title,
            self.body
        ])

def get_db_path() -> Path:
	db_path: Path = Path.home() / ".cache" / "followed_projects.db"
	parent_dir = db_path.parent
	if not parent_dir.exists():
		parent_dir.mkdir(parents=True)

	return db_path

