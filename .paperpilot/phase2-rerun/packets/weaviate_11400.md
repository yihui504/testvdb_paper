=== PACKET: weaviate_11400 ===
[vendor=weaviate version=1.37.4 defect_type=param_validation]

--- RAW ---
  [no cleaned observation available]
  [PREP PLACEHOLDER: full HTTP req/resp (REST) captured at experiment stage via probe_common raw logging]

--- CONTRACT SEGMENT ---
NO_SPECIFIC_CONTRACT: formalized contract(v1.38.0 [derived from v1.38.0]) silent on this param/scenario -> verdict_A=NEUTRAL.

--- SOURCE EXCERPT ---
status: found (14 raw hits)
// adapters/repos/db/vector/hfresh/search.go  (line 28, matched: flatSearchCutoff)
  13| 
  14| import (
  15| 	"context"
  16| 	"iter"
  17| 	"sync/atomic"
  18| 
  19| 	"github.com/pkg/errors"
  20| 	"github.com/weaviate/weaviate/adapters/repos/db/helpers"
  21| 	"github.com/weaviate/weaviate/adapters/repos/db/vector/common"
  22| 	"github.com/weaviate/weaviate/usecases/floatcomp"
  23| )
  24| 
  25| const (
  26| 	// minimum max distance to use when pruning
  27| 	pruningMinMaxDistance = 0.1
  28| 	flatSearchCutoff      = 5_000
  29| )
  30| 
  31| func (h *HFresh) SearchByVector(ctx context.Context, vector []float32, k int, allowList helpers.AllowList) ([]uint64, []float32, error) {
  32| 	vector = h.normalizeVec(vector)
  33| 
  34| 	if allowList != nil && allowList.Len() < flatSearchCutoff {
  35| 		return h.flatSearch(ctx, vector, k, allowList)
  36| 	}
  37| 
  38| 	rescoreLimit := int(h.rescoreLimit)
  39| 	if h.quantizer == nil {
  40| 		if atomic.LoadUint32(&h.dims) == 0 {
  41| 			return nil, nil, nil
  42| 		}
  43| 		return nil, nil, errors.New("quantizer not initialized")
// adapters/repos/db/vector/hnsw/search.go  (line 85, matched: flatSearchCutoff)
  70| 	}
  71| 	if k > ef {
  72| 		ef = k // otherwise results will get cut off early
  73| 	}
  74| 
  75| 	return ef
  76| }
  77| 
  78| func (h *hnsw) SearchByVector(ctx context.Context, vector []float32,
  79| 	k int, allowList helpers.AllowList,
  80| ) ([]uint64, []float32, error) {
  81| 	h.compressActionLock.RLock()
  82| 	defer h.compressActionLock.RUnlock()
  83| 
  84| 	vector = h.normalizeVec(vector)
  85| 	flatSearchCutoff := int(atomic.LoadInt64(&h.flatSearchCutoff))
  86| 	if allowList != nil && !h.forbidFlat && allowList.Len() < flatSearchCutoff {
  87| 		helpers.AnnotateSlowQueryLog(ctx, "hnsw_flat_search", true)
  88| 		return h.flatSearch(ctx, vector, k, h.searchTimeEF(k), allowList)
  89| 	}
  90| 	helpers.AnnotateSlowQueryLog(ctx, "hnsw_flat_search", false)
  91| 	return h.knnSearchByVector(ctx, vector, k, h.searchTimeEF(k), allowList)
  92| }
  93| 
  94| func (h *hnsw) SearchByMultiVector(ctx context.Context, vectors [][]float32, k int, allowList helpers.AllowList) ([]uint64, []float32, error) {
  95| 	if !h.multivector.Load() {
  96| 		return nil, nil, errors.New("multivector search is not enabled")
  97| 	}
  98| 
  99| 	if h.muvera.Load() {
 100| 		// this happens only if hnsw is empty so we need to initialize muvera encoder

--- COGNITION (developer_cognition.json, full vendor) ---
{
 "_meta": {
  "target": "weaviate",
  "analyzed_at": "2026-07-06T20:07:04.320672",
  "total_negative_issues": 0,
  "total_invalid_issues": 80,
  "total_positive_issues": 92,
  "notes": "No explicit negative issues found in this dataset - all closed issues with bug labels were classified as positive"
 },
 "rejection_patterns": [
  {
   "pattern_id": "RP-001",
   "rejection_reason": "expected_behavior",
   "description": "Behaviors that match documented API specifications even if unexpected",
   "example_issues": [],
   "developer_rationale_summary": "If the behavior matches documentation, it is considered correct",
   "attack_guidance": "DO NOT report: Behaviors that are documented or specified. INSTEAD: Verify documentation matches implementation",
   "affected_endpoints_pattern": "All API endpoints",
   "frequency": 0
  }
 ],
 "developer_cognition_signals": {
  "what_developers_consider_bugs": [
   "Parameter validation gaps at API boundaries",
   "Error handling issues that cause crashes or panics",
   "Race conditions in concurrent operations",
   "State consistency problems during operations",
   "Resource management issues (leaks, cleanup)",
   "Vector index calculation errors",
   "Configuration validation problems"
  ],
  "what_developers_prioritize": [
   "System stability and crash prevention",
   "Data consistency and integrity",
   "Storage engine correctness",
   "API contract compliance",
   "Performance and resource efficiency"
  ],
  "blindspot_indicators": [
   "Input validation is often incomplete at API boundaries",
   "Error messages lack context for debugging",
   "Edge cases in concurrent operations are frequently missed",
   "Configuration validation is inconsistent across parameters",
   "Type coercion issues in RAFT communication",
   "Backup/restore state consistency edge cases"
  ]
 },
 "by_design_patterns": []
}

--- BUG SHAPES (bug_shapes.json, full vendor) ---
{
 "_meta": {
  "target": "weaviate",
  "extracted_at": "2026-07-06T20:06:08.594766",
  "total_shapes": 5,
  "total_positive_issues": 92,
  "source_corpus": "weaviate/weaviate issues 2024-07 to 2026-07"
 },
 "bug_shapes": [
  {
   "shape_id": "BS-004",
   "name": "Parameter Validation Issues in Request Parsing",
   "root_cause_category": "parameter_validation",
   "affected_layer": "request_parsing",
   "defect_type_mapping": "Type1_IllegalSuccess",
   "cross_db_applicability": "cross_db_applicable",
   "description": "Systematic parameter_validation defects affecting request_parsing functionality",
   "symptom_pattern": "POST /v1/batch/objects accepts empty vector `[]` and reports per-item SUCCESS (singular POST /v1/obj",
   "historical_instances": [
    {
     "issue_number": 11981,
     "title": "POST /v1/batch/objects accepts empty vector `[]` and reports per-item SUCCESS (singular POST /v1/objects rejects with 422)",
     "confidence": 0.8
    },
    {
     "issue_number": 11917,
     "title": "Dropping a named vector index makes later non-vector object writes fail",
     "confidence": 0.8
    },
    {
     "issue_number": 11894,
     "title": "Broken main: dynamic package fails to compile after PR #9988 merge (stale-base merge collision)",
     "confidence": 0.8
    },
    {
     "issue_number": 11729,
     "title": "shardingConfig.desiredCount accepts negative values but rejects zero",
     "confidence": 0.8
    },
    {
     "issue_number": 11592,
     "title": "property_value boost ranks objects with missing numeric property above objects with negative values",
     "confidence": 0.8
    }
   ],
   "attack_strategy_hints": [
    "Test request_parsing with parameter_validation scenarios",
    "Verify input validation and error handling"
   ],
   "confidence": 0.75,
   "source_issues_count": 42
  },
  {
   "shape_id": "BS-003",
   "name": "Error Handling Issues in Business Logic",
   "root_cause_category": "error_handling",
   "affected_layer": "business_logic",
   "defect_type_mapping": "Type1_IllegalSuccess",
   "cross_db_applicability": "cross_db_applicable",
   "description": "Systematic error_handling defects affecting business_logic functionality",
   "symptom_pattern": "(gemini): embedding MaxObjectsPerBatch is 150; should be 100",
   "historical_instances": [
    {
     "issue_number": 11275,
     "title": "(gemini): embedding MaxObjectsPerBatch is 150; should be 100",
     "confidence": 0.8
    },
    {
     "issue_number": 10322,
     "title": "Updating the schema for a multi-tenant collection will load all shards which were in LAZY_LOADING",
     "confidence": 0.8
    },
    {
     "issue_number": 10258,
     "title": "Incorrect link for C# client library in documentation",
     "confidence": 0.8
    },
    {
     "issue_number": 9340,
     "title": "I set ENABLE_TOKENIZER_GSE_CH=true, but still get the error:  \"the GSE tokenize not enabled: set 'ENABLE TOKENIZFR GSE' enable\"",
     "confidence": 0.8
    },
    {
     "issue_number": 8912,
     "title": "Weaviate fails to start with No private IP address found, and explicit IP not provided error",
     "confidence": 0.8
    }
   ],
   "attack_strategy_hints": [
    "Test business_logic with error_handling scenarios",
    "Verify input validation and error handling"
   ],
   "confidence": 0.75,
   "source_issues_count": 17
  },
  {
   "shape_id": "BS-002",
   "name": "Concurrency Race Issues in Storage Engine",
   "root_cause_category": "concurrency_race",
   "affected_layer": "storage_engine",
   "defect_type_mapping": "Type1_IllegalSuccess",
   "cross_db_applicability": "cross_db_applicable",
   "description": "Systematic concurrency_race defects affecting storage_engine functionality",
   "symptom_pattern": "TTL: auto-activated tenant left permanently HOT when TTL context canceled mid-deletion",
   "historical_instances": [
    {
     "issue_number": 11055,
     "title": "TTL: auto-activated tenant left permanently HOT when TTL context canceled mid-deletion",
     "confidence": 0.8
    },
    {
     "issue_number": 10581,
     "title": "Regression in tenant offloading",
     "confidence": 0.8
    },
    {
     "issue_number": 9918,
     "title": "Out Of Memory when starting from a crash",
     "confidence": 0.8
    },
    {
     "issue_number": 9368,
     "title": "Panic after restart: Multiple named vectors and update of PQ quantization",
     "confidence": 0.8
    },
    {
     "issue_number": 9320,
     "title": "Shutdown while compression of vectors: Cannot query after the reboot",
     "confidence": 0.8
    }
   ],
   "attack_strategy_hints": [
    "Test storage_engine with concurrency_race scenarios",
    "Verify input validation and error handling"
   ],
   "confidence": 0.75,
   "source_issues_count": 15
  },
  {
   "shape_id": "BS-005",
   "name": "State Consistency Issues in Data Access",
   "root_cause_category": "state_consistency",
   "affected_layer": "data_access",
   "defect_type_mapping": "Type1_IllegalSuccess",
   "cross_db_applicability": "db_specific",
   "description": "Systematic state_consistency defects affecting data_access functionality",
   "symptom_pattern": "The CPU usage of weaviate is always high",
   "historical_instances": [
    {
     "issue_number": 10231,
     "title": "The CPU usage of weaviate is always high",
     "confidence": 0.8
    },
    {
     "issue_number": 9801,
     "title": "Hybrid search returns inconsistent results between Python SDK and GraphQL",
     "confidence": 0.8
    },
    {
     "issue_number": 9447,
     "title": "does Property class skip_vectorization REALLY work?",
     "confidence": 0.8
    },
    {
     "issue_number": 8914,
     "title": "Tombstone cleanup: Long time needed after reboot",
     "confidence": 0.8
    },
    {
     "issue_number": 8425,
     "title": "Fix typo: \"apiEndoint\" should be \"apiEndpoint\" in text2vec-google module",
     "confidence": 0.8
    }
   ],
   "attack_strategy_hints": [
    "Test data_access with state_consistency scenarios",
    "Verify input validation and error handling"
   ],
   "confidence": 0.75,
   "source_issues_count": 13
  },
  {
   "shape_id": "BS-001",
   "name": "Boundary Handling Issues in Data Access",
   "root_cause_category": "boundary_handling",
   "affected_layer": "data_access",
   "defect_type_mapping": "Type1_IllegalSuccess",
   "cross_db_applicability": "db_specific",
   "description": "Systematic boundary_handling defects affecting data_access functionality",
   "symptom_pattern": "Flat exact dot search can flip Top-1 after appending a large common inner-product bias dimension",
   "historical_instances": [
    {
     "issue_number": 11668,
     "title": "Flat exact dot search can flip Top-1 after appending a large common inner-product bias dimension",
     "confidence": 0.8
    },
    {
     "issue_number": 11667,
     "title": "Flat exact dot search collapses distinct inner-product scores under large common bias and flips Top-1 by UUID tie-break",
     "confidence": 0.8
    },
    {
     "issue_number": 8621,
     "title": "Property-level skip_vectorization Not Respected After Collection Creation",
     "confidence": 0.8
    },
    {
     "issue_number": 8035,
     "title": "Metadata filtering equal filter operator is not working correctly",
     "confidence": 0.8
    },
    {
     "issue_number": 6491,
     "title": "Creating a collection with `flat/bq` + `cache=true` leads to infinite `prefill_progress` log messages",
     "confidence": 0.8
    }
   ],
   "attack_strategy_hints": [
    "Test data_access with boundary_handling scenarios",
    "Verify input validation and error handling"
   ],
   "confidence": 0.75,
   "source_issues_count": 5
  }
 ]
}

--- API TEMPLATE ---
none matched

=== END PACKET ===