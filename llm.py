#!/usr/bin/env python3
"""headless LLM 호출 + JSON 파싱 공용 도구 (task-80).

기본 백엔드는 Claude Opus 5(`claude -p`)다. task-121 의 A/B 실측을 위해
`BRIEFING_LLM=codex` 로 OpenAI 쪽(codex CLI, gpt-5.6-sol)으로 갈아끼울 수 있다.
기본값을 건드리지 않으므로 매일 09:00 발행 경로는 그대로다.

BRIEFING_LLM_USAGE=<경로> 를 주면 호출마다 토큰·비용을 JSONL 로 덧붙인다.
비교 실험이 아니면 비워 둔다.
"""

import json
import os
import re
import subprocess
import sys
import time

MODEL = "opus"          # 선별·정리는 Opus 5 고정 (task-80 AC5). fable 을 쓰지 않는다.
TIMEOUT = 900

BACKEND = os.environ.get("BRIEFING_LLM", "claude")
# codex CLI 의 기본 모델은 ~/.codex/config.toml 에 있다. 실험에서 모델을 고정하고
# 싶으면 이 값을 준다(빈 값이면 codex 의 설정을 그대로 쓴다).
CODEX_MODEL = os.environ.get("BRIEFING_CODEX_MODEL", "")
USAGE_LOG = os.environ.get("BRIEFING_LLM_USAGE", "")


def _log_usage(record):
    if not USAGE_LOG:
        return
    record["backend"] = BACKEND
    with open(USAGE_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _ask_claude(prompt, model, tag):
    """claude -p 를 돌려 표준출력을 돌려준다. 실패는 예외로 올린다."""
    args = ["claude", "-p", "--model", model]
    if USAGE_LOG:
        args += ["--output-format", "json"]
    t0 = time.monotonic()
    p = subprocess.run(args + [prompt], capture_output=True, text=True, timeout=TIMEOUT)
    elapsed = time.monotonic() - t0
    if p.returncode != 0:
        # claude 는 인증 만료 같은 치명적 실패를 stdout 으로 뱉는다. stderr 만 보면
        # 로그에 빈 문자열이 남아 원인을 못 찾는다(2026-08-26 발행 사고).
        why = (p.stderr.strip() or p.stdout.strip() or "(출력 없음)")[:400]
        raise RuntimeError(f"claude 실패 (rc={p.returncode}): {why}")
    out = p.stdout.strip()
    if not out:
        raise RuntimeError("claude 가 빈 응답을 냈다")
    if USAGE_LOG:
        # --output-format json 은 결과와 usage 를 한 봉투에 담아 준다.
        env = json.loads(out)
        u = env.get("usage") or {}
        _log_usage({"tag": tag, "seconds": round(elapsed, 1),
                    "input": u.get("input_tokens", 0),
                    "cache_read": u.get("cache_read_input_tokens", 0),
                    "cache_write": u.get("cache_creation_input_tokens", 0),
                    "output": u.get("output_tokens", 0),
                    "cost_usd": env.get("total_cost_usd")})
        out = (env.get("result") or "").strip()
        if not out:
            raise RuntimeError("claude 가 빈 result 를 냈다")
    return out


def _ask_codex(prompt, tag):
    """codex exec 를 돌려 마지막 메시지를 돌려준다 (task-121 A/B 용).

    codex 는 에이전트 하니스라 도구를 들고 돈다. 이 잡은 순수 생성만 필요하므로
    샌드박스를 read-only 로 묶고 세션 파일도 남기지 않는다. 그래도 시스템 프롬프트와
    도구 정의가 매 호출 앞에 붙는데(실측 17K 안팎), 그 오버헤드까지 포함한 값이
    이 잡에서 실제로 드는 비용이라 그대로 잰다.
    """
    out_file = f"/tmp/codex-last-{os.getpid()}-{tag}.txt"
    args = ["codex", "exec", "--json", "--ephemeral", "--skip-git-repo-check",
            "-s", "read-only", "-o", out_file]
    if CODEX_MODEL:
        args += ["-m", CODEX_MODEL]
    t0 = time.monotonic()
    p = subprocess.run(args + [prompt], capture_output=True, text=True, timeout=TIMEOUT)
    elapsed = time.monotonic() - t0
    if p.returncode != 0:
        raise RuntimeError(f"codex 실패 (rc={p.returncode}): {p.stderr.strip()[:400]}")
    usage = {}
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "turn.completed":
            usage = ev.get("usage") or {}
    try:
        with open(out_file, encoding="utf-8") as f:
            out = f.read().strip()
    except FileNotFoundError:
        raise RuntimeError("codex 가 마지막 메시지를 남기지 않았다")
    finally:
        try:
            os.remove(out_file)
        except OSError:
            pass
    if not out:
        raise RuntimeError("codex 가 빈 응답을 냈다")
    _log_usage({"tag": tag, "seconds": round(elapsed, 1),
                "input": usage.get("input_tokens", 0),
                "cache_read": usage.get("cached_input_tokens", 0),
                "cache_write": usage.get("cache_write_input_tokens", 0),
                "output": usage.get("output_tokens", 0),
                "reasoning": usage.get("reasoning_output_tokens", 0)})
    return out


def ask(prompt, model=MODEL, tag="ask"):
    if BACKEND == "codex":
        return _ask_codex(prompt, tag)
    return _ask_claude(prompt, model, tag)


def ask_json(prompt, model=MODEL, retries=2, tag="ask"):
    """JSON 을 요구하는 호출. 코드펜스·잡담이 섞여 와도 최대한 건져 낸다."""
    last = None
    for i in range(retries + 1):
        text = ask(prompt if i == 0 else prompt + "\n\n반드시 JSON 만 출력하라. 설명·코드블록 금지.",
                   model, tag=f"{tag}{'' if i == 0 else f'-retry{i}'}")
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
