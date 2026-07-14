import cli


def run_cli(monkeypatch, capsys, inputs):
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))
    monkeypatch.setattr(cli, "delay", lambda ms: None)
    cli.main()
    return capsys.readouterr().out


def test_exit_immediately(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["exit"])
    assert "바이바이" in out


def test_invalid_number_input_shows_error_and_retries(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["abc", "exit"])
    assert "ERROR :: 숫자만 입력 가능" in out


def test_out_of_range_input_shows_error_and_retries(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["9", "exit"])
    assert "ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능" in out


def test_back_navigation_returns_to_previous_step(monkeypatch, capsys):
    # Sedan 선택 -> 뒤로가기(0) -> 다시 차량 타입 메뉴가 표시되어야 함
    out = run_cli(monkeypatch, capsys, ["1", "0", "exit"])
    assert out.count("어떤 차량 타입을 선택할까요?") == 2


def test_full_flow_run_produces_car(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["1", "1", "1", "1", "1", "exit"])
    assert "차량 타입으로 Sedan을 선택하셨습니다." in out
    assert "GM 엔진을 선택하셨습니다." in out
    assert "자동차가 동작됩니다." in out


def test_full_flow_test_produces_pass(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["1", "1", "1", "1", "2", "exit"])
    assert "PASS" in out


def test_final_step_back_returns_to_first_menu(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["1", "1", "1", "1", "0", "exit"])
    assert out.count("어떤 차량 타입을 선택할까요?") == 2
