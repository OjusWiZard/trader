# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the always blue strategy."""

from typing import Dict, Any, List, Union


def get_always_blue() -> Dict[str, Union[int, List[str]]]:
    """ALWAYS BLUE."""
    return {"bet_amount": 0, "info": ["ALWAYS BLUE!"]}


def run(*_args, **kwargs) -> Dict[str, Union[int, List[str]]]:
    """Run the strategy."""
    return get_always_blue()
