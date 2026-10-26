from types import SimpleNamespace

from app import ask


def test_ask_displays_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=34,
        ),
    )

    class FakeClient:
        class models:
            @staticmethod
            def generate_content(**kwargs):
                return response

    monkeypatch.setattr(ask.genai, "Client", lambda api_key: FakeClient())
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")

    assert ask.ask("質問") == "回答"
    assert "[トークン数] 入力: 12, 出力: 34" in capsys.readouterr().out


def test_ask_reports_when_token_usage_is_unavailable(monkeypatch, capsys):
    response = SimpleNamespace(text="回答", usage_metadata=None)

    class FakeClient:
        class models:
            @staticmethod
            def generate_content(**kwargs):
                return response

    monkeypatch.setattr(ask.genai, "Client", lambda api_key: FakeClient())
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")

    assert ask.ask("質問") == "回答"
    assert "入力・出力: 取得できませんでした" in capsys.readouterr().out
