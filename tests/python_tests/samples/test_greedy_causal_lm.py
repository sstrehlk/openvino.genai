# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import os
import pytest
import sys

from conftest import SAMPLES_PY_DIR, SAMPLES_CPP_DIR, SAMPLES_C_DIR
from test_utils import run_sample

class TestGreedyCausalLM:
    @pytest.mark.llm
    @pytest.mark.samples
    @pytest.mark.parametrize(
        "convert_model, sample_args",
        [
            pytest.param("TinyLlama-1.1B-Chat-v1.0", "test"),
            pytest.param("SmolLM-135M", "return 0"),
            pytest.param("Qwen2.5-0.5B-Instruct", "69"),
        ],
        indirect=["convert_model"],
    )
    def test_sample_greedy_causal_lm(self, convert_model, sample_args):
        # Test Python sample
        py_script = os.path.join(SAMPLES_PY_DIR, "text_generation/greedy_causal_lm.py")
        py_command = [sys.executable, py_script, convert_model, sample_args]
        py_result = run_sample(py_command)

        # Test CPP sample
        cpp_sample = os.path.join(SAMPLES_CPP_DIR, 'greedy_causal_lm')
        cpp_command =[cpp_sample, convert_model, sample_args]
        cpp_result = run_sample(cpp_command)

        # Test C sample
        c_sample = os.path.join(SAMPLES_C_DIR, "greedy_causal_lm_c")
        c_command =[c_sample, convert_model, sample_args]
        c_result = run_sample(c_command)

        # Compare results
        assert py_result.stdout == cpp_result.stdout, f"Results should match"
        assert cpp_result.stdout == c_result.stdout, f"Results should match"
