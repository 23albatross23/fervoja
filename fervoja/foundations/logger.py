# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:23:40 2026

@author: Álvaro Pauner Argudo
"""

# Copyright (C) 2026  Álvaro Pauner Argudo <alvaro.pauner@outlook.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from multiprocessing import Process, Queue
from pathlib import Path
from typing import Optional, Final
import sys
from .singleton import SingletonMeta

def logger_worker(queue: Queue, file_path: Path) -> None:
    try:
        with file_path.open(mode='a', encoding='utf-8') as f:
            while True:
                record: Optional[str] = queue.get()
                if record is None:
                    break
                f.write(f"{record}\n")
                f.flush()
    except Exception as e:
        print(f"Critical failure at logging process: {e}", file=sys.stderr)

class Logger(metaclass=SingletonMeta):
    '''
    Process-safe and Thread-safe Logger for Fervoja.
    Uses a separate process to handle I/O operations asynchronously.
    '''
    DEFAULT_LOG_PATH: Final[Path] =\
        Path(__file__).parent.parent / "logs" / "fervoja.log"

    def __init__(self):
        Logger.DEFAULT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        Logger.DEFAULT_LOG_PATH.touch(exist_ok=True)
        self.queue: Queue[Optional[str]] = Queue()
        self.worker_process: Optional[Process] = None
    
    def __assert_process(self) -> None:
        '''Internal method to ensure the worker process is running (Lazy Init).'''
        if self.worker_process is None:
            self.worker_process = Process(
                target=logger_worker,
                args=(self.queue, Logger.DEFAULT_LOG_PATH),
                daemon=True
            )
            self.worker_process.start()

    def log(self, info: str) -> None:
        self.__assert_process()
        self.queue.put(info)

    def error(self, info: str) -> None:
        self.log(f"[ERROR] {info}")

    def info(self, info: str) -> None:
        self.log(f"[INFO] {info}")

    def stop(self) -> None:
        '''Gracefully shuts down the logging process.'''
        if self.worker_process is not None and self.worker_process.is_alive():
            self.queue.put(None)
            self.worker_process.join(timeout=2)
            if self.worker_process.is_alive():
                self.worker_process.terminate()
                
    
    