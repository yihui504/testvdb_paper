"""tests/test_runtime_milvus.py — runtime/{_common,milvus} 单元测试。

mock `req` 验证 setup_default 各阶段失败路径 + judge 全分支 + PATHS 完整性。
不连真实 milvus。
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import pytest  # noqa: E402

from runtime import _common, milvus  # noqa: E402


# ── judge_4xx ──────────────────────────────────────────────

@pytest.mark.unit
class TestJudge4xx:
    def test_200_setup_ok_is_defect(self):
        assert _common.judge_4xx(200, "", setup_ok=True) == "DEFECT_FOUND"

    @pytest.mark.parametrize("status", [400, 422])
    def test_4xx_setup_ok_is_no_defect(self, status):
        assert _common.judge_4xx(status, "", setup_ok=True) == "NO_DEFECT"

    def test_404_is_script_error_not_defect(self):
        # ← milvus v2.6.19 实测根因 ①：404 不应判 contract 违规
        assert _common.judge_4xx(404, "", setup_ok=True) == "SCRIPT_ERROR"

    @pytest.mark.parametrize("status", [500, 502, 503])
    def test_5xx_is_script_error(self, status):
        assert _common.judge_4xx(status, "", setup_ok=True) == "SCRIPT_ERROR"

    def test_connection_failure_is_script_error(self):
        assert _common.judge_4xx(0, "conn refused", setup_ok=True) == "SCRIPT_ERROR"

    def test_setup_fail_blocks_defect(self):
        # ← 实测根因 ③：setup 失败时不应判 contract 违规
        assert _common.judge_4xx(200, "", setup_ok=False) == "SCRIPT_ERROR"


# ── judge_200 ──────────────────────────────────────────────

@pytest.mark.unit
class TestJudge200:
    def test_200_setup_ok_is_no_defect(self):
        assert _common.judge_200(200, "", setup_ok=True) == "NO_DEFECT"

    @pytest.mark.parametrize("status", [400, 404, 422])
    def test_4xx_is_defect(self, status):
        # 合法输入被错误拒绝
        assert _common.judge_200(status, "", setup_ok=True) == "DEFECT_FOUND"

    def test_5xx_is_script_error(self):
        assert _common.judge_200(500, "", setup_ok=True) == "SCRIPT_ERROR"


# ── milvus.request path_key 校验 ───────────────────────────

@pytest.mark.unit
class TestRequestPathKey:
    def test_bad_path_key_raises_keyerror(self):
        with pytest.raises(KeyError, match="path_key"):
            milvus.request("POST", "nonexistent_key", {})


# ── milvus.setup_default 各阶段失败 ───────────────────────

@pytest.mark.unit
class TestSetupDefaultFailure:
    def test_create_fail_returns_false(self, monkeypatch):
        calls = []

        def fake_req(base, method, path, body=None, timeout=30):
            calls.append(path)
            return 500, '{"error":"internal"}'

        monkeypatch.setattr("runtime.milvus.req", fake_req)
        ok, err = milvus.setup_default("c", 128, wait=0)
        assert ok is False
        assert "create 500" in err
        # create 失败不应级联调 index/load
        assert len(calls) == 1

    def test_index_fail_returns_false(self, monkeypatch):
        calls = []

        def fake_req(base, method, path, body=None, timeout=30):
            calls.append(path)
            if path == milvus.PATHS["create_collection"]:
                return 200, "{}"
            if path == milvus.PATHS["create_index"]:
                return 500, '{"error":"index failed"}'
            return 200, "{}"

        monkeypatch.setattr("runtime.milvus.req", fake_req)
        ok, err = milvus.setup_default("c", 128, wait=0)
        assert ok is False
        assert "index 500" in err

    def test_load_fail_returns_false(self, monkeypatch):
        calls = []

        def fake_req(base, method, path, body=None, timeout=30):
            calls.append(path)
            if path == milvus.PATHS["load_collection"]:
                return 500, '{"error":"load failed"}'
            return 200, "{}"

        monkeypatch.setattr("runtime.milvus.req", fake_req)
        ok, err = milvus.setup_default("c", 128, wait=0)
        assert ok is False
        assert "load 500" in err


# ── milvus.setup_default 成功路径 ─────────────────────────

@pytest.mark.unit
class TestSetupDefaultSuccess:
    def test_success_calls_create_index_load_in_order(self, monkeypatch):
        calls = []

        def fake_req(base, method, path, body=None, timeout=30):
            calls.append(path)
            return 200, "{}"

        monkeypatch.setattr("runtime.milvus.req", fake_req)
        ok, err = milvus.setup_default("c", 128, wait=0)
        assert ok is True and err == ""
        assert calls == [
            milvus.PATHS["create_collection"],
            milvus.PATHS["create_index"],
            milvus.PATHS["load_collection"],
        ]

    def test_409_idempotent_releases_first(self, monkeypatch):
        # create 409 → release → index → load 全 200
        calls = []

        def fake_req(base, method, path, body=None, timeout=30):
            calls.append(path)
            if path == milvus.PATHS["create_collection"]:
                return 409, '{"error":"already exists"}'
            return 200, "{}"

        monkeypatch.setattr("runtime.milvus.req", fake_req)
        ok, err = milvus.setup_default("c", 128, wait=0)
        assert ok is True, f"expected ok, got err={err}"
        assert milvus.PATHS["release_collection"] in calls

    def test_create_payload_has_required_fields(self, monkeypatch):
        """milvus v2.6.19 实测根因 ②：payload 缺 dimension → 后续级联失败。"""
        captured = {}

        def fake_req(base, method, path, body=None, timeout=30):
            if path == milvus.PATHS["create_collection"]:
                captured["body"] = body
            return 200, "{}"

        monkeypatch.setattr("runtime.milvus.req", fake_req)
        milvus.setup_default("c", 128, wait=0)
        b = captured["body"]
        for f in ("collectionName", "dimension", "metricType",
                  "idType", "autoID", "vectorFieldType"):
            assert f in b, f"missing required field {f}"
        assert b["dimension"] == 128
        assert b["collectionName"] == "c"


# ── milvus.drop_collection ────────────────────────────────

@pytest.mark.unit
class TestDropCollection:
    def test_never_raises_on_network_error(self, monkeypatch):
        def boom(*a, **k):
            raise RuntimeError("network gone")

        monkeypatch.setattr("runtime.milvus.req", boom)
        # cleanup 永不抛（spec 规定）
        milvus.drop_collection("any")


# ── milvus.PATHS 完整性 ───────────────────────────────────

@pytest.mark.unit
class TestPathsIntegrity:
    def test_all_values_start_with_slash(self):
        for k, v in milvus.PATHS.items():
            assert v.startswith("/"), f"{k}={v!r} should start with /"

    def test_required_keys_present(self):
        must = {"create_collection", "drop_collection", "load_collection",
                "create_index", "insert_points", "search"}
        assert must <= set(milvus.PATHS), f"missing: {must - set(milvus.PATHS)}"

    def test_no_untranslated_plus_in_values(self):
        # path 必须已翻译（contract 的 + → /）；残留 + = 翻译漏了
        for k, v in milvus.PATHS.items():
            assert "+" not in v, f"{k}={v!r} 未翻译（仍含 +）"

    def test_no_entities_create_trap(self):
        # ← milvus v2.6.19 实测根因 ①：建集合路径必须是 /collections/create
        assert milvus.PATHS["create_collection"] == "/collections/create"
        assert milvus.PATHS["create_collection"] != "/entities/create"


# ── dispatch (get_runtime) ─────────────────────────────────

@pytest.mark.unit
class TestGetRuntime:
    def test_milvus_dispatch_returns_module(self, monkeypatch):
        monkeypatch.setenv("TESTVDB_TARGET", "milvus")
        from runtime import get_runtime
        rt = get_runtime()
        assert rt.__name__ == "runtime.milvus"
        # 统一接口齐全
        for attr in ("PATHS", "request", "setup_default",
                     "drop_collection", "judge_4xx", "judge_200"):
            assert hasattr(rt, attr), f"runtime missing {attr}"

    def test_unsupported_target_raises(self, monkeypatch):
        monkeypatch.setenv("TESTVDB_TARGET", "postgres")
        from runtime import get_runtime
        with pytest.raises(RuntimeError, match="unsupported"):
            get_runtime()


@pytest.mark.unit
class TestJudgeSchemaAttackMilvus:
    """judge_schema_attack milvus 版 — describe_collection 回读三态判定。
    跨 target 一致接口；milvus 适配 body code 模式（200+code!=0=拒绝）+ data 嵌套。"""

    def _stub_request(self, monkeypatch, describe_status=200, describe_code=0,
                       describe_data=None):
        import json as _j
        def fake_req(method, path_key, body=None, path_params=None, timeout=30):
            d = {"code": describe_code}
            if describe_data is not None:
                d["data"] = describe_data
            return describe_status, _j.dumps(d)
        monkeypatch.setattr("runtime.milvus.request", fake_req)

    def test_type1_persisted(self, monkeypatch):
        self._stub_request(monkeypatch, describe_data={"opt": -1})
        v = milvus.judge_schema_attack(200, '{"code":0}', "X", ["opt"], -1)
        assert v == "DEFECT_FOUND"

    def test_silent_drop_no_defect(self, monkeypatch):
        # 字段被 silent-drop（None）→ NO_DEFECT
        self._stub_request(monkeypatch, describe_data={})
        v = milvus.judge_schema_attack(200, '{"code":0}', "X", ["opt"], -1)
        assert v == "NO_DEFECT"

    def test_body_code_reject_no_defect(self, monkeypatch):
        # milvus 200+code!=0 = 拒绝 → NO_DEFECT（不调 describe）
        v = milvus.judge_schema_attack(200, '{"code":1100,"msg":"err"}', "X", ["opt"], -1)
        assert v == "NO_DEFECT"

    def test_4xx_reject_no_defect(self, monkeypatch):
        v = milvus.judge_schema_attack(422, '{"code":1100}', "X", ["opt"], -1)
        assert v == "NO_DEFECT"

    def test_describe_body_code_nonzero_script_error(self, monkeypatch):
        # describe 返回 code != 0（如 collection 不存在）→ SCRIPT_ERROR
        self._stub_request(monkeypatch, describe_code=100, describe_data=None)
        v = milvus.judge_schema_attack(200, '{"code":0}', "X", ["opt"], -1)
        assert v == "SCRIPT_ERROR"

    def test_nested_path_persisted(self, monkeypatch):
        self._stub_request(monkeypatch, describe_data={"a": {"b": 0}})
        v = milvus.judge_schema_attack(200, '{"code":0}', "X", ["a", "b"], 0)
        assert v == "DEFECT_FOUND"

    def test_data_missing_script_error(self, monkeypatch):
        # describe 返回 code=0 但无 data 字段 → SCRIPT_ERROR
        self._stub_request(monkeypatch, describe_code=0, describe_data=None)
        v = milvus.judge_schema_attack(200, '{"code":0}', "X", ["opt"], -1)
        assert v == "SCRIPT_ERROR"
