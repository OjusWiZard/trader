# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
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

"""This module contains the class to connect to the `ServiceStakingTokenMechUsage` contract."""

from aea.common import JSONLike
from aea.configurations.base import PublicId
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi


class ServiceStakingTokenContract(Contract):
    """The Service Staking contract."""

    contract_id = PublicId.from_str("valory/service_staking_token:0.1.0")

    @classmethod
    def is_service_staked(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        service_id: int,
    ) -> JSONLike:
        """Check whether the service is staked."""
        contract_instance = cls.get_instance(ledger_api, contract_address)
        res = contract_instance.functions.isServiceStaked(service_id).call()
        return dict(data=res)

    @classmethod
    def build_stake_tx(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        service_id: int,
    ) -> JSONLike:
        """Build stake tx."""
        contract_instance = cls.get_instance(ledger_api, contract_address)
        data = contract_instance.encodeABI("stake", args=[service_id])
        return dict(data=bytes.fromhex(data[2:]))

    @classmethod
    def build_checkpoint_tx(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Build checkpoint tx."""
        contract_instance = cls.get_instance(ledger_api, contract_address)
        data = contract_instance.encodeABI("checkpoint")
        return dict(data=bytes.fromhex(data[2:]))

    @classmethod
    def build_unstake_tx(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        service_id: int,
    ) -> JSONLike:
        """Build unstake tx."""
        contract_instance = cls.get_instance(ledger_api, contract_address)
        data = contract_instance.encodeABI("unstake", args=[service_id])
        return dict(data=bytes.fromhex(data[2:]))

    @classmethod
    def available_rewards(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Get the available rewards."""
        contract_instance = cls.get_instance(ledger_api, contract_address)
        res = contract_instance.functions.availableRewards().call()
        return dict(data=res)

    @classmethod
    def get_staking_rewards(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        service_id: int,
    ) -> JSONLike:
        """Get the service's staking rewards."""
        contract = cls.get_instance(ledger_api, contract_address)
        reward = contract.functions.calculateServiceStakingReward(service_id).call()
        return dict(data=reward)

    @classmethod
    def get_next_checkpoint_ts(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Get the next checkpoint's timestamp."""
        contract = cls.get_instance(ledger_api, contract_address)
        ts = contract.functions.getNextRewardCheckpointTimestamp().call()
        return dict(data=ts)
