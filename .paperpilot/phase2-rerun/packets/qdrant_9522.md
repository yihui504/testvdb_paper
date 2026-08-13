=== PACKET: qdrant_9522 ===
[vendor=qdrant version=1.18.2 defect_type=behavior]

--- RAW ---
  [c1] lookup referencing non-existent collection -> status=200, 3 results
  [c2] control: lookup referencing valid collection -> status=200
  [PREP PLACEHOLDER: full HTTP req/resp (REST) captured at experiment stage via probe_common raw logging]

--- CONTRACT SEGMENT ---
contract_file: v1.18.2
- [qdrant_range_search_points_006] hnsw_ef parameter is applicable only when exact=false. (collections+{collection_name}+points+search)
    source: https://api.qdrant.tech/v-1-18-x/api-reference/search/points
- [qdrant_state_remove_peer_013] force=true should only be used when peer is unreachable. (cluster+peer+{peer_id})
    source: https://api.qdrant.tech/v-1-18-x/api-reference
- [qdrant_state_search_points_009] When exact=true, search uses brute-force; when exact=false, search uses HNSW. (collections+{collection_name}+points+search)
    source: https://api.qdrant.tech/v-1-18-x/api-reference/search/points

--- SOURCE EXCERPT ---
status: found (2416 raw hits)
// src/actix/api/search_api.rs  (line 3, matched: API)
   1| use actix_web::{HttpResponse, Responder, post, web};
   2| use actix_web_validator::{Json, Path, Query};
   3| use api::rest::{SearchMatrixOffsetsResponse, SearchMatrixPairsResponse, SearchMatrixRequest};
   4| use collection::collection::distance_matrix::CollectionSearchMatrixRequest;
   5| use collection::operations::shard_selector_internal::ShardSelectorInternal;
   6| use collection::operations::types::{
   7|     CoreSearchRequest, SearchGroupsRequest, SearchRequest, SearchRequestBatch,
   8| };
   9| use itertools::Itertools;
  10| use storage::content_manager::collection_verification::check_strict_mode;
  11| use storage::dispatcher::Dispatcher;
  12| use tokio::time::Instant;
  13| 
  14| use super::CollectionPath;
  15| use super::read_params::ReadParams;
  16| use crate::actix::auth::ActixAuth;
  17| use crate::actix::helpers::{
  18|     get_request_hardware_counter, process_response, process_response_error,
// src/common/inference/query_requests_grpc.rs  (line 1, matched: API)
   1| use api::conversions::json::json_path_from_proto;
   2| use api::grpc::qdrant::RecommendInput;
   3| use api::grpc::qdrant::query::Variant;
   4| use api::grpc::{InferenceUsage, qdrant as grpc};
   5| use api::rest::{self, LookupLocation, RecommendStrategy};
   6| use collection::operations::universal_query::collection_query::{
   7|     CollectionPrefetch, CollectionQueryGroupsRequest, CollectionQueryRequest, FeedbackInternal,
   8|     FeedbackStrategy, Mmr, NearestWithMmr, Query, VectorInputInternal, VectorQuery,
   9| };
  10| use collection::operations::universal_query::formula::FormulaInternal;
  11| use collection::operations::universal_query::shard_query::{FusionInternal, SampleInternal};
  12| use ordered_float::OrderedFloat;
  13| use segment::data_types::order_by::OrderBy;
  14| use segment::data_types::vectors::{DEFAULT_VECTOR_NAME, MultiDenseVectorInternal, VectorInternal};
  15| use segment::types::{Filter, PointIdType, SearchParams};
  16| use segment::vector_storage::query::{

--- COGNITION (developer_cognition.json, full vendor) ---
{
 "blindspot_indicators": [
  "Parameter validation on filter/condition APIs (min_should, value_count)",
  "HNSW approximation edge cases in offset-based pagination",
  "WAL replay state consistency (point resurrection)",
  "Concurrent shard worker restart safety (try_join_all cancellation)",
  "TLS/auth edge cases in cluster p2p communication",
  "Snapshot compatibility across different platforms (Windows Docker)",
  "Silent failure in recommend API with missing point IDs",
  "Replica consistency reporting discrepancies",
  "Optimizer worker restart partial progress states",
  "Memory allocator compatibility (jemalloc on large page sizes)"
 ],
 "what_developers_prioritize": [
  "Data consistency and persistence over API strictness",
  "Production stability over edge case handling",
  "Performance optimization over diagnostic completeness",
  "API backward compatibility over strict validation",
  "Cluster communication over single-node correctness"
 ],
 "recurring_patterns": [
  {
   "pattern": "Pagination API contract violations",
   "count": 88
  },
  {
   "pattern": "Filter condition validation gaps",
   "count": 51
  },
  {
   "pattern": "WAL replay state inconsistency",
   "count": 67
  },
  {
   "pattern": "Concurrent worker safety",
   "count": 55
  },
  {
   "pattern": "Memory/platform compatibility",
   "count": 15
  }
 ],
 "high_frequency_shapes": [
  {
   "pattern": "error_handling",
   "count": 95
  },
  {
   "pattern": "api_contract_violation",
   "count": 88
  },
  {
   "pattern": "state_consistency",
   "count": 67
  },
  {
   "pattern": "concurrency_race",
   "count": 55
  },
  {
   "pattern": "parameter_validation",
   "count": 51
  },
  {
   "pattern": "resource_management",
   "count": 42
  },
  {
   "pattern": "authentication_authorization",
   "count": 18
  },
  {
   "pattern": "memory_management",
   "count": 15
  }
 ],
 "by_design_patterns": [
  {
   "pattern": "HNSW approximation duplicates in pagination",
   "developer_stance": "Accepted limitation of approximate search",
   "source_issues": [
    9523
   ],
   "should_report": false
  },
  {
   "pattern": "Large page sizes on aarch64 with jemalloc",
   "developer_stance": "External dependency limitation",
   "source_issues": [
    3831,
    4298,
    6512,
    7246
   ],
   "should_report": false
  }
 ],
 "low_priority_patterns": [
  {
   "pattern": "Documentation typos",
   "count": 25
  },
  {
   "pattern": "User questions/how-to",
   "count": 43
  }
 ]
}

--- BUG SHAPES (bug_shapes.json, full vendor) ---
{
 "_meta": {
  "target": "qdrant",
  "extracted_at": "2026-08-11T06:27:00.132946Z",
  "total_shapes": 5,
  "d2_shape_injected_at": "2026-08-11T06:51:03.532456Z",
  "d2_shape_injected_note": "cardinality_oracle hand-injected for D2 (extractor produced empty shells); isolates attack-vein consumption of shape guidance from extractor production bug",
  "d3_hints_rollback_at": "2026-08-11T08:28:15.536410Z",
  "d3_hints_rollback_reason": "D3 验证 hints 改动无效且部分误导：hint2 same-field split 让 agent 误读成 must+must 重复条件（D3 vein_compound_and_test.py 实证，引出 70% under 非 TP#2）；hint7 GROUND-TRUTH SANITY 在 geo 正向（避免 FP）但在 type_mismatch 反向理解（agent 用 scroll=0 当应返回 0 证据，FP 更精致）。净效果接近 0 或负面，按 surgical 原则回退。cardinality_oracle shape 本身保留（D2 论文论据）。"
 },
 "bug_shapes": [
  {
   "shape_id": "qdrant-parameter-validation-numeric-boundary",
   "name": "Parameter Validation issues where Numeric Boundary validation is missing",
   "root_cause_category": "parameter_validation",
   "shape_type": "numeric_boundary",
   "affected_layer": "request_parsing",
   "defect_type_mapping": "Type1_IllegalSuccess",
   "cross_db_applicability": "cross_db_applicable",
   "abstract_pattern": "Parameter Validation issues where Numeric Boundary validation is missing",
   "description": "Parameter Validation issues where Numeric Boundary validation is missing",
   "symptom_pattern": "API accepts invalid Numeric Boundary values without returning 4xx",
   "known_instances": [
    {
     "issue_number": 9613,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 7246,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 9438,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 9017,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 9039,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 2557,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 5138,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 9027,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 8724,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 6416,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    }
   ],
   "attack_strategy_hints": [
    "Enumerate Numeric Boundary parameters in contract",
    "Test boundary values"
   ],
   "confidence": 0.75,
   "source_issues_count": 36,
   "source_prs_count": 0
  },
  {
   "shape_id": "qdrant-type-coercion-type-confusion",
   "name": "Type Coercion issues where Type Confusion validation is missing",
   "root_cause_category": "type_coercion",
   "shape_type": "type_confusion",
   "affected_layer": "request_parsing",
   "defect_type_mapping": "Type1_IllegalSuccess",
   "cross_db_applicability": "cross_db_applicable",
   "abstract_pattern": "Type Coercion issues where Type Confusion validation is missing",
   "description": "Type Coercion issues where Type Confusion validation is missing",
   "symptom_pattern": "API accepts invalid Type Confusion values without returning 4xx",
   "known_instances": [
    {
     "issue_number": 9373,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 8126,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 6825,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 5807,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 4015,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    }
   ],
   "attack_strategy_hints": [
    "Enumerate Type Confusion parameters in contract",
    "Test boundary values"
   ],
   "confidence": 0.75,
   "source_issues_count": 5,
   "source_prs_count": 0
  },
  {
   "shape_id": "qdrant-resource-management-resource-limit",
   "name": "Resource Management issues where Resource Limit validation is missing",
   "root_cause_category": "resource_management",
   "shape_type": "resource_limit",
   "affected_layer": "request_parsing",
   "defect_type_mapping": "Type1_IllegalSuccess",
   "cross_db_applicability": "cross_db_applicable",
   "abstract_pattern": "Resource Management issues where Resource Limit validation is missing",
   "description": "Resource Management issues where Resource Limit validation is missing",
   "symptom_pattern": "API accepts invalid Resource Limit values without returning 4xx",
   "known_instances": [
    {
     "issue_number": 9045,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 7967,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 6826,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 6334,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 5388,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 3802,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 3818,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 3820,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 3737,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 1737,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    }
   ],
   "attack_strategy_hints": [
    "Enumerate Resource Limit parameters in contract",
    "Test boundary values"
   ],
   "confidence": 0.75,
   "source_issues_count": 10,
   "source_prs_count": 0
  },
  {
   "shape_id": "qdrant-concurrency-race-concurrency-race",
   "name": "Concurrency Race issues where Concurrency Race validation is missing",
   "root_cause_category": "concurrency_race",
   "shape_type": "concurrency_race",
   "affected_layer": "request_parsing",
   "defect_type_mapping": "Type1_IllegalSuccess",
   "cross_db_applicability": "cross_db_applicable",
   "abstract_pattern": "Concurrency Race issues where Concurrency Race validation is missing",
   "description": "Concurrency Race issues where Concurrency Race validation is missing",
   "symptom_pattern": "API accepts invalid Concurrency Race values without returning 4xx",
   "known_instances": [
    {
     "issue_number": 4808,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 1662,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    },
    {
     "issue_number": 1515,
     "endpoint": "N/A",
     "param": "N/A",
     "value": "N/A"
    }
   ],
   "attack_strategy_hints": [
    "Enumerate Concurrency Race parameters in contract",
    "Test boundary values"
   ],
   "confidence": 0.75,
   "source_issues_count": 3,
   "source_prs_count": 0
  },
  {
   "shape_id": "qdrant-cardinality-oracle-count-exact-false",
   "name": "Cardinality Oracle mismatch on count API exact:false (indexed approximate path)",
   "root_cause_category": "cardinality_estimation",
   "shape_type": "cardinality_oracle",
   "affected_layer": "query_planning",
   "defect_type_mapping": "Type2_PoorDiagnostics",
   "cross_db_applicability": "cross_db_applicable",
   "abstract_pattern": "count API's approximate cardinality path (exact:false, uses index histograms / estimators) diverges from the exact path (exact:true, scan) and from scroll/search ground truth, for certain filter condition classes. The estimator math (numeric_index histogram, geo_index, keyword_index estimate, query_estimator combine_*) is imprecise or wrong for specific condition shapes, so the returned count is systematically off.",
   "description": "When POST /collections/{c}/points/count is called with exact:false, the server uses index-based cardinality estimation rather than a scan. Different condition classes route to different estimators (numeric_index.range_cardinality / histogram.estimate, geo_index, keyword_index.estimate_cardinality, query_estimator.combine_must_estimations / combine_should_estimations, IsEmptyCondition cardinality, condition_checker for type-mismatch match values). Each estimator is an independent bug surface: math imprecision or formula error causes count(exact:false) to diverge from count(exact:true) and from the scroll/search ground truth. Symptom is a returned count that is systematically over or under the true cardinality for one condition class while other classes remain correct.",
   "symptom_pattern": "count(exact:false)=N but count(exact:true)=M and scroll with same filter returns M points; |N-M| exceeds tolerated estimation error (>20% OR systematic one-directional drift across collection sizes). Other condition classes on the same collection return correct counts, isolating the bug to one estimator.",
   "known_instances": [
    {
     "issue_number": 10096,
     "endpoint": "POST /collections/{collection_name}/points/count",
     "param": "exact:false + is_null condition on indexed field",
     "value": "indexed vs unindexed (exact:true) path return different counts for is_null"
    },
    {
     "issue_number": 9373,
     "endpoint": "POST /collections/{collection_name}/points/count",
     "param": "exact:false",
     "value": "adjacent: under-count report (different root cause, listed for context only)"
    }
   ],
   "attack_strategy_hints": [
    "PRIMARY ENDPOINT: POST /collections/{collection_name}/points/count. Always probe BOTH exact:true and exact:false for the same filter; divergence beyond tolerated estimation error is the signal.",
    "GENERALIZATION from #10096: is_null indexed-vs-scan divergence is one instance of a wider pattern. Treat each filter condition class in the contract as an independent estimator surface — matrix-test every condition class (range, compound must+must_not AND, geo_radius, match_any OR, is_empty, match-value-type vs schema-type) on count(exact:false) vs count(exact:true) vs scroll ground truth.",
    "INDEXING PRECONDITION: the approximate path only triggers when the payload index is built. After PUT /index, sleep 3-5s; also set optimizer_config.indexing_threshold=1 on the collection to force payload cardinality estimate. Without this the indexed path is not exercised and the bug is invisible.",
    "CONTROL GROUP (mandatory for every DEFECT_FOUND): (a) same filter via scroll/search returns ground-truth point set — count it client-side and compare; (b) vary collection size (e.g. 50 / 200 / 500 points with the same proportional distribution) — if the count ratio scales linearly with size (e.g. always 1/2), it is a fallback heuristic (by-design), NOT a bug; a real estimator bug has direction-consistent but size-independent absolute or proportional error.",
    "BEWARE BY-DESIGN FALLBACK: qdrant falls back to a coarse estimate (often 1/2 scaling) when the index has insufficient data. Rule this out with the size-variation control above before claiming a defect. Consult threat_model.json by_design / wontfix entries.",
    "NOVELTY CHECK before claiming: confirm the divergence is not already tracked in an OPEN issue; #9373 is an under-count report (different root cause), #8723/#8734 are about rebuild visibility not cardinality under-count, #9201 is gRPC NaN. A genuine new finding must be a different condition-class / different estimator."
   ],
   "confidence": 0.9,
   "source_issues_count": 2,
   "source_prs_count": 0
  }
 ]
}

--- API TEMPLATE ---
POST collections+{collection_name}+points+query -- Universal Query API with multi-stage pipeline support

=== END PACKET ===