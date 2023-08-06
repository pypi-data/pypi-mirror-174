from __future__ import annotations

import logging
import os
import time
import types
from typing import Dict, List, Tuple

import ulid

from ..serialize import get_callsite_data


formatter = logging.Formatter()


class LoggingFilter:
    co_names: Tuple[str, ...] = ("_log",)
    logging_filename = os.path.normpath("/logging/")

    def __init__(self, config) -> None:
        self.config = config

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        return (
            event == "return"
            and self.logging_filename in frame.f_code.co_filename
            and frame.f_code.co_name in self.co_names
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        timestamp = time.time()
        frame_locals = frame.f_locals
        exc_info = frame_locals["exc_info"]
        traceback = None if exc_info is None else formatter.formatException(exc_info)
        extra = frame_locals["extra"]
        if call_frame_ids:
            user_code_call_site = get_callsite_data(frame, call_frame_ids[-1])
        else:
            user_code_call_site = None
        return {
            "args": frame_locals["args"],
            "extra": extra,
            "frame_id": f"frm_{ulid.new()}",
            "level": logging.getLevelName(frame_locals["level"]),
            "msg": frame_locals["msg"],
            "stack": formatter.formatStack(frame_locals["sinfo"]),
            "timestamp": timestamp,
            "traceback": traceback,
            "type": "log_message",
            "user_code_call_site": user_code_call_site,
        }
