from __future__ import annotations

import json
import logging
import logging.config
from dataclasses import asdict, dataclass
from pathlib import Path

import appdirs

CONFIG_DIR = Path(appdirs.user_config_dir("hue-sunrise"))
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "config.json"

LOG_DIR = Path(appdirs.user_log_dir())
LOG_DIR.mkdir(exist_ok=True, parents=True)
LOG_FILE = LOG_DIR / "hue-sunrise.log"


@dataclass
class Config:
    bridge_ip_address: str | None
    bridge_username: str | None
    lights: list[str]
    total_scene_length_min: int
    afterglow_length_min: int
    config_file: Path
    log_file: Path

    def dump(self) -> None:
        with open(CONFIG_FILE, "w") as fp:
            d = asdict(self)
            d = {
                k: v if not isinstance(v, Path) else str(v)
                for k, v in d.items()
            }
            json.dump(d, fp, indent=2)

    @classmethod
    def reset(cls) -> None:
        CONFIG_FILE.unlink()

    @classmethod
    def default(cls) -> Config:
        return Config(
            bridge_ip_address=None,
            bridge_username=None,
            lights=[],
            total_scene_length_min=15,
            afterglow_length_min=15,
            config_file=CONFIG_FILE,
            log_file=LOG_FILE,
        )

    @classmethod
    def from_file(cls) -> Config:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as fp:
                raw: dict[str, str | list[str] | None] = json.load(fp)

            bridge_ip_address = raw["bridge_ip_address"]
            bridge_username = raw["bridge_username"]
            lights = raw["lights"]
            total_scene_length_min = raw["total_scene_length_min"]
            afterglow_length_min = raw["afterglow_length_min"]

            if bridge_ip_address is not None:
                assert isinstance(bridge_ip_address, str)
            if bridge_username is not None:
                assert isinstance(bridge_username, str)
            assert isinstance(lights, list)
            assert isinstance(total_scene_length_min, int)
            assert isinstance(afterglow_length_min, int)

            return Config(
                bridge_ip_address=bridge_ip_address,
                bridge_username=bridge_username,
                lights=lights,
                total_scene_length_min=total_scene_length_min,
                afterglow_length_min=afterglow_length_min,
                config_file=Path(CONFIG_FILE),
                log_file=Path(LOG_FILE),
            )
        else:
            config = cls.default()
            config.dump()
            return config

    def set_ip(self, ip: str) -> None:
        self.bridge_ip_address = ip
        self.dump()

    def set_username(self, username: str) -> None:
        self.bridge_username = username
        self.dump()

    def set_lights(self, lights: list[str]) -> None:
        self.lights = lights
        self.dump()

    def set_total_scene_length_min(self, total_scene_length_min: int) -> None:
        self.total_scene_length_min = total_scene_length_min
        self.dump()

    def set_afterglow_length_min(self, afterglow_length_min: int) -> None:
        self.afterglow_length_min = afterglow_length_min
        self.dump()


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": str(LOG_FILE),
                "when": "W0",  # Monday
                "backupCount": 1,
            },
            "stream": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "": {
                "handlers": ["file", "stream"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
)
logger = logging.getLogger(__name__)
