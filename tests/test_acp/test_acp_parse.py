"""Tests for ACPLlm._parse_response() function_call extraction (Doc 25).

Verifies that ACPLlm correctly:
- Returns plain text when no function_call JSON is present
- Extracts function_call JSON into FunctionCall objects
- Handles malformed JSON gracefully (falls back to text)
- Does not mis-extract non-function_call JSON
"""

import pytest

from soulbot.models.acp_llm import ACPLlm


class TestParseResponse:
    """ACPLlm._parse_response() extracts function_call from text."""

    def test_plain_text_passthrough(self):
        """Text without function_call returns Part(text=...)."""
        resp = ACPLlm._parse_response("Hello, how can I help you?")
        assert resp.content is not None
        assert len(resp.content.parts) == 1
        assert resp.content.parts[0].text == "Hello, how can I help you?"
        assert resp.content.parts[0].function_call is None

    def test_function_call_extracted(self):
        """Text with function_call JSON returns Part(function_call=...)."""
        text = '{"function_call": {"name": "get_weather", "arguments": {"city": "Paris"}}}'
        resp = ACPLlm._parse_response(text)
        assert resp.content is not None
        fc = resp.content.parts[0].function_call
        assert fc is not None
        assert fc.name == "get_weather"
        assert resp.content.parts[0].text is None

    def test_function_call_with_args(self):
        """Function call arguments are correctly parsed as dict."""
        text = '{"function_call": {"name": "search", "arguments": {"query": "python", "limit": 10}}}'
        resp = ACPLlm._parse_response(text)
        fc = resp.content.parts[0].function_call
        assert fc.args == {"query": "python", "limit": 10}

    def test_function_call_with_surrounding_text(self):
        """Function call JSON embedded in surrounding text is extracted."""
        text = (
            'I need to check the weather. '
            '{"function_call": {"name": "get_weather", "arguments": {"city": "Tokyo"}}}'
            ' Let me look that up.'
        )
        resp = ACPLlm._parse_response(text)
        fc = resp.content.parts[0].function_call
        assert fc is not None
        assert fc.name == "get_weather"
        assert fc.args == {"city": "Tokyo"}

    def test_malformed_json_fallback(self):
        """Malformed function_call JSON falls back to plain text."""
        text = '{"function_call": {"name": "broken", "arguments": {invalid}}'
        resp = ACPLlm._parse_response(text)
        # Should fall back to text since JSON is invalid
        assert resp.content.parts[0].text is not None
        assert resp.content.parts[0].function_call is None

    def test_empty_text(self):
        """Empty string returns Part(text='')."""
        resp = ACPLlm._parse_response("")
        assert resp.content.parts[0].text == ""
        assert resp.content.parts[0].function_call is None

    def test_non_function_call_json_not_extracted(self):
        """JSON without 'function_call' key is not mis-extracted."""
        text = '{"result": {"name": "test", "value": 42}}'
        resp = ACPLlm._parse_response(text)
        assert resp.content.parts[0].text is not None
        assert resp.content.parts[0].function_call is None

    def test_multiline_function_call(self):
        """Multi-line formatted function_call JSON is extracted."""
        text = """{
  "function_call": {
    "name": "calculate",
    "arguments": {
      "expression": "2 + 2"
    }
  }
}"""
        resp = ACPLlm._parse_response(text)
        fc = resp.content.parts[0].function_call
        assert fc is not None
        assert fc.name == "calculate"
        assert fc.args == {"expression": "2 + 2"}

    def test_no_arguments_defaults_to_empty(self):
        """Function call without 'arguments' key defaults to empty dict."""
        text = '{"function_call": {"name": "no_args"}}'
        resp = ACPLlm._parse_response(text)
        fc = resp.content.parts[0].function_call
        assert fc is not None
        assert fc.name == "no_args"
        assert fc.args == {}
