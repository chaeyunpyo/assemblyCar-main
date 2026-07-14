import pytest

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


def test_broken_engine_run_does_not_move(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["1", "4", "1", "1", "1", "exit"])
    assert "엔진이 고장나있습니다." in out
    assert "자동차가 움직이지 않습니다." in out


def test_rule_violation_run_does_not_move(monkeypatch, capsys):
    # Sedan + Continental 제동장치 -> 제한조건2 위반
    out = run_cli(monkeypatch, capsys, ["1", "1", "2", "2", "1", "exit"])
    assert "자동차가 동작되지 않습니다" in out


def test_rule_violation_test_reports_fail(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["1", "1", "2", "2", "2", "exit"])
    assert "FAIL" in out
    assert "Sedan에는 Continental제동장치 사용 불가" in out


@pytest.mark.parametrize("step_inputs,expected_error", [
    (["5"], "ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능"),
    (["1", "9"], "ERROR :: 엔진은 1 ~ 4 범위만 선택 가능"),
    (["1", "1", "9"], "ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능"),
    (["1", "1", "1", "9"], "ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능"),
    (["1", "1", "1", "1", "9"], "ERROR :: Run 또는 Test 중 하나를 선택 필요"),
])
def test_out_of_range_error_per_step(monkeypatch, capsys, step_inputs, expected_error):
    out = run_cli(monkeypatch, capsys, [*step_inputs, "exit"])
    assert expected_error in out
