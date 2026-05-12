from __future__ import annotations

import logging
import sys
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot


class SoundDevice:
    def __init__(
        self, name: str, device_id: int | str, device_type: SoundDeviceType
    ) -> None:
        self.name = name
        self.id = device_id
        self.type = device_type


class SoundDeviceType(Enum):
    Output = 0
    Input = 1


class SoundDeviceManager:
    def __init__(self, bot: Bot) -> None:
        self.config = bot.config
        self.output_device = self.config.sound_devices.output_device
        self.input_device = self.config.sound_devices.input_device
        self.player = bot.player
        self.ttclient = bot.ttclient
        self.output_devices = self.player.get_output_devices()
        self.input_devices = self.ttclient.get_input_devices()

    def _find_device(
        self, key: int | str, devices: list[SoundDevice], label: str
    ) -> SoundDevice:
        if isinstance(key, int):
            try:
                return devices[key]
            except IndexError:
                error = f"Incorrect {label} device index: {key}"
                logging.error(error)
                sys.exit(error)
        for device in devices:
            if key in device.name:
                return device
        error = f"{label.capitalize()} device not found: {key}"
        logging.error(error)
        sys.exit(error)

    def initialize(self) -> None:
        logging.debug("Initializing sound devices")
        output = self._find_device(
            self.output_device, self.output_devices, "output"
        )
        self.player.set_output_device(str(output.id))
        input_ = self._find_device(
            self.input_device, self.input_devices, "input"
        )
        self.ttclient.set_input_device(int(input_.id))
        logging.debug("Sound devices initialized")
