# Copyright (c) 2025 GreenTurtle
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""unittest for inference.py"""


import unittest

import munch

from greenturtle import exception
from greenturtle.inference import inference


class TestInference(unittest.TestCase):
    """unittest for Inference module"""

    def test_set_broker(self):
        """test set_broker"""
        conf = munch.Munch()
        # test set back broker by default
        infer = inference.Inference(conf=conf)
        infer.set_broker()
        broker = infer.cerebro.getbroker()
        self.assertEqual("back_broker", broker.name)

    def test_get_auto_margin(self):
        """test get_auto_margin"""
        infer = inference.Inference()
        self.assertEqual(30, infer.get_auto_margin("IF"))

    def test_get_get_multiplier(self):
        """test get_auto_margin"""
        infer = inference.Inference()
        self.assertEqual(300, infer.get_multiplier("IF"))

    def test_set_multiplier_and_auto_margin(self):
        """test set_multiplier_and_auto_margin"""
        infer = inference.Inference()
        infer.set_multiplier_and_auto_margin("IF")

    def test_validate_config(self):
        """test validate_config"""
        infer = inference.Inference()

        # validate empty config
        conf = munch.Munch()
        infer.validate_config(conf)

        # validate config with empty strategy
        conf.strategy = munch.Munch()
        infer.validate_config(conf)

        # validate config with legal risk factor
        conf.strategy.risk_factor = 0.001
        infer.validate_config(conf)

        # validate config with forbidden risk factor
        conf.strategy.risk_factor = 0.006
        self.assertRaises(exception.ValidateRiskFactorError,
                          infer.validate_config,
                          conf)
        conf.strategy.risk_factor = -0.001
        self.assertRaises(exception.ValidateRiskFactorError,
                          infer.validate_config,
                          conf)

        # validate config with legal group risk factor
        conf.strategy.risk_factor = 0.001
        conf.strategy.group_risk_factors = {"indices": 0.02}
        infer.validate_config(conf)

        # validate config with forbidden group risk factor
        conf.strategy.group_risk_factors = {"indices": 0.05}
        self.assertRaises(exception.ValidateGroupRiskFactorError,
                          infer.validate_config,
                          conf)
        conf.strategy.group_risk_factors = {
            "indices": 0.02,
            "agriculture": 0.02,
            "metal": 0.02,
            "energy": 0.02,
        }
        self.assertRaises(exception.ValidateGroupRiskFactorError,
                          infer.validate_config,
                          conf)
