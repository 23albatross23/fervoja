# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:17:11 2026

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

import pytest
import time
from pathlib import Path
from typing import Any
from fervoja.foundations.logger import Logger

@pytest.fixture(autouse=True)
def reset_singleton():
    """
    Cleans up the Singleton instance before each test to ensure
    isolation between test cases.
    """
    # We access the private attribute of the metaclass to reset state
    Logger._instances = {}
    yield

class TestLogger:
    def test_logger_creates_directory_and_file(self, tmp_path: Path, monkeypatch: Any):
        """Verify that the logger creates the directory and file if they don't exist."""
        test_log = tmp_path / "logs" / "fervoja.log"
        monkeypatch.setattr(Logger, "DEFAULT_LOG_PATH", test_log)
        
        # Inits the logger (creates path)
        logger = Logger()
        
        assert test_log.parent.exists()
        assert test_log.exists()

    def test_logger_writes_info_stop_message(self, tmp_path: Path, monkeypatch: Any):
        """Verify that an info message is correctly written to the file."""
        test_log = tmp_path / "info.log"
        monkeypatch.setattr(Logger, "DEFAULT_LOG_PATH", test_log)
        
        logger = Logger()
        message = "Testing the railway system logs"
        logger.info(message)
        content = ""
        for _ in range(20):  # 20 attempts * 0.1s = 2s total timeout
            if test_log.exists():
                content = test_log.read_text(encoding='utf-8')
                if f"[INFO] {message}" in content:
                    break
            time.sleep(0.1)
        
        assert f"[INFO] {message}" in content
        
        logger.error(message)
        content = ""
        for _ in range(20):  # 20 attempts * 0.1s = 2s total timeout
            if test_log.exists():
                content = test_log.read_text(encoding='utf-8')
                if f"[ERROR] {message}" in content:
                    break
            time.sleep(0.1)
        
        assert f"[INFO] {message}" in content
        logger.stop()

    def test_logger_singleton_behavior(self):
        """Verify that multiple Logger calls return the same instance."""
        logger1 = Logger()
        logger2 = Logger()
        
        assert logger1 is logger2
        logger1.stop()

    def test_logger_stop_process_cleanly(self, tmp_path: Path, monkeypatch: Any):
        """Verify that the worker process stops after calling stop()."""
        test_log = tmp_path / "stop.log"
        monkeypatch.setattr(Logger, "DEFAULT_LOG_PATH", test_log)
        
        logger = Logger()
        logger.log("Termination test")
        
        # Ensure process started
        assert logger.worker_process is not None
        assert logger.worker_process.is_alive()
        
        logger.stop()
        assert not logger.worker_process.is_alive()
        
        
        