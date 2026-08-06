#!/usr/bin/env python3
"""headless claude 호출 + JSON 파싱 공용 도구 (task-80)."""

import json
import re
import subprocess
import sys

MODEL = "opus"          # 선별·정리는 Opus 5 고정 (task-80 AC5). fable 을 쓰지 않는다.
TIMEOUT = 900


def ask(prompt, model=MODEL):
    """claude -p 를 돌려 표준출력을 돌려준다. 실패는 예외로 올린다."""
    p = subprocess.run(
        ["claude", "-p", "--model", model, prompt],
        capture_output=True, text=True, timeout=TIMEOUT,
    )
    if p.returncode != 0:
        raise RuntimeError(f"claude 실패 (rc={p.returncode}): {p.stderr.strip()[:400]}")
    out = p.stdout.strip()
    if not out:
        raise RuntimeError("claude 가 빈 응답을 냈다")
    return out


def ask_json(prompt, model=MODEL, retries=2):
    """JSON 을 요구하는 호출. 코드펜스·잡담이 섞여 와도 최대한 건져 낸다."""
    last = None
    for i in range(retries + 1):
        text = ask(prompt if i == 0 else prompt + "\n\n반드시 JSON 만 출력하라. 설명·코드블록 금지.", model)
        try:
            return json.loads(_strip(text))
        except json.JSONDecodeError as e:
            last = e
            print(f"  JSON 파싱 실패({i + 1}/{retries + 1}): {e}", file=sys.stderr)
            print(f"  응답 앞부분: {text[:200]}", file=sys.stderr)
    raise RuntimeError(f"JSON 파싱 최종 실패: {last}")


def _strip(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1)
    text = text.strip()
    # 앞뒤에 문장이 붙어 오는 경우 첫 { 부터 마지막 } 까지만 남긴다.
    if not text.startswith(("{", "[")):
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e > s:
            text = text[s: e + 1]
    return text
