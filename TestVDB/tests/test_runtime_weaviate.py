"""tests/test_runtime_weaviate.py — weaviate runtime 单元测试。

mock `req` 验证 path_params 替换 + setup_default + PATHS 模板完整性。
不连真实 weaviate。
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import pytest  # noqa: E402

from runtime import _common, weaviate  # noqa: E402


@pytest.mark.unit
class TestPathsTemplates:
    def test_name_template_keys(self):
        for k in ("describe_schema", "drop_schema", "add_property"):
            assert "{name}" in weaviate.PATHS[k]

    def test_id_template_keys(self):
        for k in ("get_object", "delete_object"):
            assert "{id}" in weaviate.PATHS[k]

    def test_no_param_keys(self):
        for k in ("create_schema", "list_schema", "create_object",
                  "batch_objects", "graphql"):
            assert "{" not in weaviate.PATHS[k]

    def test_distance_map(self):
        assert weaviate.DISTANCE_MAP["cosine"] == "cosine"
        assert weaviate.DISTANCE_MAP["l2"] == "l2-squared"
        assert weaviate.DISTANCE_MAP["dot"] == "dot"


@pytest.mark.unit
class TestRequestPathParams:
    def test_bad_path_key_raises(self):
        with pytest.raises(KeyError, match="path_key"):
            weaviate.request("POST", "nonexistent_key", {})

    def test_path_params_name(self, monkeypatch):
        captured = {}

        def fake_req(base, method, path, body=None, timeout=30):
            captured["path"] = path
            return 200, '{}'

        monkeypatch.setattr("runtime.weaviate.req", fake_req)
        weaviate.request("DELETE", "drop_schema", path_params={"name": "MyClass"})
        assert captured["path"] == "/v1/schema/MyClass"

    def test_path_params_id(self, monkeypatch):
        captured = {}

        def fake_req(base, method, path, body=None, timeout=30):
            captured["path"] = path
            return 200, '{}'

        monkeypatch.setattr("runtime.weaviate.req", fake_req)
        weaviate.request("GET", "get_object", path_params={"id": "abc-123"})
        assert captured["path"] == "/v1/objects/abc-123"

    def test_no_param_request_works(self, monkeypatch):
        captured = {}

        def fake_req(base, method, path, body=None, timeout=30):
            captured["path"] = path
            return 200, '{}'

        monkeypatch.setattr("runtime.weaviate.req", fake_req)
        weaviate.request("GET", "list_schema")
        assert captured["path"] == "/v1/schema"


@pytest.mark.unit
class TestSetupDefault:
    def test_unsupported_metric(self):
        ok, err = weaviate.setup_default("c", 128, metric="INVALID")
        assert ok is False
        assert "unsupported metric" in err

    def test_create_fail(self, monkeypatch):
        def fake_req(base, method, path, body=None, timeout=30):
            return 500, '{"error":"internal"}'

        monkeypatch.setattr("runtime.weaviate.req", fake_req)
        ok, err = weaviate.setup_default("c", 128)
        assert ok is False
        assert "create_schema 500" in err

    def test_create_success(self, monkeypatch):
        captured = {}

        def fake_req(base, method, path, body=None, timeout=30):
            captured["body"] = body
            return 200, '{}'

        monkeypatch.setattr("runtime.weaviate.req", fake_req)
        ok, err = weaviate.setup_default("Article", 128, metric="cosine")
        assert ok is True and err == ""
        assert captured["body"]["class"] == "Article"
        assert captured["body"]["vectorIndexConfig"]["distance"] == "cosine"

    def test_422_idempotent(self, monkeypatch):
        def fake_req(base, method, path, body=None, timeout=30):
            return 422, '{"error":"already exists"}'

        monkeypatch.setattr("runtime.weaviate.req", fake_req)
        ok, _ = weaviate.setup_default("c", 128)
        assert ok is True


@pytest.mark.unit
class TestDropSchema:
    def test_never_raises_on_error(self, monkeypatch):
        def boom(*a, **k):
            raise RuntimeError("network gone")

        monkeypatch.setattr("runtime.weaviate.req", boom)
        weaviate.drop_schema("any")


@pytest.mark.unit
class TestCommonExpectRecordsWeaviateStyle:
    def test_graphql_get_class_list(self):
        assert _common.expect_records(200, '{"data":{"Get":{"Article":[1,2,3]}}}', expected_min=3) == "NO_DEFECT"
        assert _common.expect_records(200, '{"data":{"Get":{"Article":[]}}}', expected_min=1) == "DEFECT_FOUND"

    def test_rest_objects_list(self):
        assert _common.expect_records(200, '{"objects":[1,2]}', expected_min=2) == "NO_DEFECT"
        assert _common.expect_records(200, '{"objects":[],"totalObjects":0}', expected_min=1) == "DEFECT_FOUND"

    def test_4xx_script_error(self):
        assert _common.expect_records(400, '', expected_min=1) == "SCRIPT_ERROR"


@pytest.mark.unit
class TestJudgeSchemaAttack:
    """judge_schema_attack 三态判定 + describe 回读覆盖。
    实战教训（2026-07-05）：weaviate silent-drop schema 字段，旧 expect_rejected 误判 Type1。"""

    def _stub_request(self, monkeypatch, describe_status=200, describe_body=None):
        """造一个 fake request：judge_schema_attack 内部只调 describe 一次，stub 返回它的响应。
        attack 的 status/raw 由测试直接传给 judge_schema_attack 入参（不走 stub）。"""
        import json as _j

        def fake_req(method, path_key, body=None, path_params=None, timeout=30):
            return describe_status, _j.dumps(describe_body) if describe_body else "{}"
        monkeypatch.setattr("runtime.weaviate.request", fake_req)

    def test_type1_persisted_illegal_value(self, monkeypatch):
        # vectorCacheMaxObjects=-1 被持久化为 -1 → Type1
        self._stub_request(monkeypatch, describe_body={"vectorIndexConfig": {"vectorCacheMaxObjects": -1}})
        v = weaviate.judge_schema_attack(200, "", "X",
                                          ["vectorIndexConfig", "vectorCacheMaxObjects"], -1)
        assert v == "DEFECT_FOUND"

    def test_silent_drop_no_defect(self, monkeypatch):
        # cleanupIntervalSeconds 放错位置被 silent-drop → NO_DEFECT（避免 false positive）
        self._stub_request(monkeypatch, describe_body={"vectorIndexConfig": {}})  # 字段不在
        v = weaviate.judge_schema_attack(200, "", "X",
                                          ["vectorIndexConfig", "cleanupIntervalSeconds"], -100)
        assert v == "NO_DEFECT"

    def test_type2_silent_normalization(self, monkeypatch):
        # replicationConfig.factor=0 被持久化为 1（norm）→ Type2 仍算 DEFECT_FOUND
        self._stub_request(monkeypatch, describe_body={"replicationConfig": {"factor": 1}})
        v = weaviate.judge_schema_attack(200, "", "X",
                                          ["replicationConfig", "factor"], 0)
        assert v == "DEFECT_FOUND"

    def test_correct_reject_422(self, monkeypatch):
        # weaviate 正确 422 → NO_DEFECT（不调 describe）
        self._stub_request(monkeypatch, describe_body={})
        v = weaviate.judge_schema_attack(422, "", "X",
                                          ["vectorIndexConfig", "maxConnections"], -1)
        assert v == "NO_DEFECT"

    def test_describe_failure_script_error(self, monkeypatch):
        # status=200 但 describe 失败 → SCRIPT_ERROR
        self._stub_request(monkeypatch, describe_status=500, describe_body={})
        v = weaviate.judge_schema_attack(200, "", "X",
                                          ["vectorIndexConfig", "k"], -1)
        assert v == "SCRIPT_ERROR"

    def test_setup_not_ok_script_error(self):
        v = weaviate.judge_schema_attack(200, "", "X", ["k"], -1, setup_ok=False)
        assert v == "SCRIPT_ERROR"

    def test_5xx_script_error(self):
        v = weaviate.judge_schema_attack(500, "", "X", ["k"], -1)
        assert v == "SCRIPT_ERROR"

    def test_nested_path_missing_returns_script_error(self, monkeypatch):
        # describe 返回的 dict 路径中间断掉 → SCRIPT_ERROR
        self._stub_request(monkeypatch, describe_body={"vectorIndexConfig": "not-a-dict"})
        v = weaviate.judge_schema_attack(200, "", "X",
                                          ["vectorIndexConfig", "subkey"], -1)
        assert v == "SCRIPT_ERROR"


@pytest.mark.unit
class TestGetRuntimeDispatch:
    def test_weaviate_dispatch(self, monkeypatch):
        monkeypatch.setenv("TESTVDB_TARGET", "weaviate")
        from runtime import get_runtime
        rt = get_runtime()
        assert rt.__name__ == "runtime.weaviate"
        for attr in ("PATHS", "request", "setup_default", "drop_schema",
                     "judge_4xx", "judge_200", "expect_records", "expect_rejected"):
            assert hasattr(rt, attr), f"weaviate runtime missing {attr}"

    def test_unsupported_target_lists_weaviate(self, monkeypatch):
        monkeypatch.setenv("TESTVDB_TARGET", "postgres")
        from runtime import get_runtime
        with pytest.raises(RuntimeError, match="implemented: milvus, qdrant, weaviate"):
            get_runtime()
