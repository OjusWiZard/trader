# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023-2024 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   you may obtain a copy of the License at
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


import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, FrozenSet, Hashable, List, Mapping, Optional
from unittest import mock
from unittest.mock import MagicMock

import pytest

from packages.valory.skills.abstract_round_abci.base import BaseTxPayload
from packages.valory.skills.abstract_round_abci.test_tools.rounds import BaseCollectSameUntilThresholdRoundTest
from packages.valory.skills.decision_maker_abci.payloads import DecisionReceivePayload
from packages.valory.skills.decision_maker_abci.states.base import (
    Event,
    SynchronizedData,
)
from packages.valory.skills.decision_maker_abci.states.decision_receive import DecisionReceiveRound

DUMMY_DECISION_HASH = "dummy_decision_hash"
DUMMY_PARTICIPANT_TO_DECISION_HASH = json.dumps(
    {
        "agent_0": "decision_1",
        "agent_1": "decision_2",
        "agent_2": "decision_3",
    }
)

def get_participants() -> FrozenSet[str]:
    """Participants."""
    return frozenset([f"agent_{i}" for i in range(4)])

def get_payloads(vote: Optional[str], confidence: Optional[float], bet_amount: Optional[float], next_mock_data_row: Optional[str], is_profitable: bool) -> Mapping[str, BaseTxPayload]:
    """Get payloads."""
    return {
        participant: DecisionReceivePayload(participant, vote, confidence, bet_amount, next_mock_data_row, is_profitable)
        for participant in get_participants()
    }

@dataclass
class RoundTestCase:
    """RoundTestCase for DecisionReceiveRound."""
    name: str
    initial_data: Dict[str, Hashable]
    payloads: Mapping[str, BaseTxPayload]
    final_data: Dict[str, Hashable]
    event: Event
    most_voted_payload: Any
    synchronized_data_attr_checks: List[Callable] = field(default_factory=list)

class TestDecisionReceiveRound(BaseCollectSameUntilThresholdRoundTest):
    """Tests for DecisionReceiveRound."""

    _synchronized_data_class = SynchronizedData  

    @pytest.mark.parametrize(
        "test_case",
        (
            RoundTestCase(
                name="Happy path",
                initial_data={},
                payloads=get_payloads(vote="yes", confidence=0.8, bet_amount=100.0, next_mock_data_row="row_1", is_profitable=True),
                final_data={
                    "decision_hash": DUMMY_DECISION_HASH,
                    "participant_to_decision_hash": DUMMY_PARTICIPANT_TO_DECISION_HASH,
                },
                event=Event.DONE,
                most_voted_payload=DUMMY_DECISION_HASH,
                synchronized_data_attr_checks=[
                    lambda synchronized_data: synchronized_data.decision_hash,
                ],
            ),
            RoundTestCase(
                name="Unprofitable decision",
                initial_data={"is_profitable": False},
                payloads=get_payloads(vote="no", confidence=0.5, bet_amount=50.0, next_mock_data_row="row_2", is_profitable=False),
                final_data={
                    "decision_hash": DUMMY_DECISION_HASH,
                    "participant_to_decision_hash": DUMMY_PARTICIPANT_TO_DECISION_HASH,
                },
                event=Event.UNPROFITABLE,
                most_voted_payload=DUMMY_DECISION_HASH,
                synchronized_data_attr_checks=[
                    lambda synchronized_data: synchronized_data.decision_hash,
                ],
            ),
            RoundTestCase(
                name="No majority",
                initial_data={},
                payloads=get_payloads(vote=None, confidence=None, bet_amount=None, next_mock_data_row=None, is_profitable=True),  # Simulating insufficient votes
                final_data={},
                event=Event.NO_MAJORITY,
                most_voted_payload=None,
                synchronized_data_attr_checks=[],
            ),
            RoundTestCase(
                name="Tie event",
                initial_data={},
                payloads=get_payloads(vote=None, confidence=None, bet_amount=None, next_mock_data_row=None, is_profitable=True),  # Simulating a tie situation
                final_data={},
                event=Event.TIE,
                most_voted_payload=None,
                synchronized_data_attr_checks=[],
            ),
            RoundTestCase(
                name="Mechanism response error",
                initial_data={"mocking_mode": True},
                payloads=get_payloads(vote=None, confidence=None, bet_amount=None, next_mock_data_row=None, is_profitable=True),  # Simulating mocking mode response
                final_data={},
                event=Event.MECH_RESPONSE_ERROR,
                most_voted_payload=None,
                synchronized_data_attr_checks=[],
            ),
        ),
    )
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""
        self.run_test(test_case)

    def run_test(self, test_case: RoundTestCase) -> None:
        """Run the test."""
        self.synchronized_data.update(
            SynchronizedData, **test_case.initial_data
        )

        test_round = DecisionReceiveRound(
            synchronized_data=self.synchronized_data, context=mock.MagicMock()
        )

        self._test_round(
            test_round=test_round,
            round_payloads=test_case.payloads,
            synchronized_data_update_fn=lambda sync_data, _: sync_data.update(
                **test_case.final_data
            ),
            synchronized_data_attr_checks=test_case.synchronized_data_attr_checks,
            most_voted_payload=test_case.most_voted_payload,
            exit_event=test_case.event,
        )
