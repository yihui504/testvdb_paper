=== PACKET: weaviate_11399 ===
[vendor=weaviate version=1.37.4 defect_type=param_validation]

--- RAW ---
  [no cleaned observation available]
  [PREP PLACEHOLDER: full HTTP req/resp (REST) captured at experiment stage via probe_common raw logging]

--- CONTRACT SEGMENT ---
contract_file: v1.38.0 [derived]
- [weaviate_type_schema_create_002] properties.vectorIndexType in {hnsw, flat, dynamic, bwes} (/schema POST)
    source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json
- [weaviate_range_graphql_001] integer values in GraphQL must fit int32 range [-2147483648, 2147483647] (/graphql POST)
    source: https://weaviate.io/developers/weaviate/api/graphql

--- SOURCE EXCERPT ---
status: found (7 raw hits)
// adapters/repos/db/vector/hnsw/index.go  (line 366, matched: dynamicEfMin)
 351| 		id:                    cfg.ID,
 352| 		rootPath:              cfg.RootPath,
 353| 		tombstones:            map[uint64]struct{}{},
 354| 		logger:                cfg.Logger,
 355| 		distancerProvider:     cfg.DistanceProvider,
 356| 		deleteLock:            &sync.Mutex{},
 357| 		tombstoneLock:         &sync.RWMutex{},
 358| 		resetLock:             &sync.RWMutex{},
 359| 		resetCtx:              resetCtx,
 360| 		resetCtxCancel:        resetCtxCancel,
 361| 		shutdownCtx:           shutdownCtx,
 362| 		shutdownCtxCancel:     shutdownCtxCancel,
 363| 		initialInsertOnce:     &sync.Once{},
 364| 
 365| 		ef:       int64(uc.EF),
 366| 		efMin:    int64(uc.DynamicEFMin),
 367| 		efMax:    int64(uc.DynamicEFMax),
 368| 		efFactor: int64(uc.DynamicEFFactor),
 369| 
 370| 		metrics:   newMetrics(cfg.PrometheusMetrics, cfg.ClassName, cfg.ShardName, cfg.HFreshMode),
 371| 		shardName: cfg.ShardName,
 372| 
 373| 		randFunc:                          rand.Float64,
 374| 		compressActionLock:                &sync.RWMutex{},
 375| 		className:                         cfg.ClassName,
 376| 		VectorForIDThunk:                  cfg.VectorForIDThunk,
 377| 		MultiVectorForIDThunk:             cfg.MultiVectorForIDThunk,
 378| 		TempMultiVectorForIDThunk:         cfg.TempMultiVectorForIDThunk,
 379| 		GetViewThunk:                      cfg.GetViewThunk,
 380| 		TempVectorForIDWithViewThunk:      cfg.TempVectorForIDWithViewThunk,
 381| 		TempMultiVectorForIDWithViewThunk: cfg.TempMultiVectorForIDWithViewThunk,
// adapters/repos/db/vector/hnsw/config_update.go  (line 104, matched: dynamicEfMin)
  89| 	}
  90| 
  91| 	return nil
  92| }
  93| 
  94| func (h *hnsw) UpdateUserConfig(updated config.VectorIndexConfig, callback func()) error {
  95| 	parsed, ok := updated.(ent.UserConfig)
  96| 	if !ok {
  97| 		callback()
  98| 		return errors.Errorf("config is not UserConfig, but %T", updated)
  99| 	}
 100| 
 101| 	// Store automatically as a lock here would be very expensive, this value is
 102| 	// read on every single user-facing search, which can be highly concurrent
 103| 	atomic.StoreInt64(&h.ef, int64(parsed.EF))
 104| 	atomic.StoreInt64(&h.efMin, int64(parsed.DynamicEFMin))
 105| 	atomic.StoreInt64(&h.efMax, int64(parsed.DynamicEFMax))
 106| 	atomic.StoreInt64(&h.efFactor, int64(parsed.DynamicEFFactor))
 107| 	atomic.StoreInt64(&h.flatSearchCutoff, int64(parsed.FlatSearchCutoff))
 108| 
 109| 	h.acornSearch.Store(parsed.FilterStrategy == ent.FilterStrategyAcorn)
 110| 
 111| 	if !parsed.PQ.Enabled && !parsed.BQ.Enabled && !parsed.SQ.Enabled && !parsed.RQ.Enabled {
 112| 		callback()
 113| 		return nil
 114| 	}
 115| 
 116| 	// check if rq bits is immutable
 117| 	if h.rqConfig.Enabled && parsed.RQ.Enabled {
 118| 		if parsed.RQ.Bits != h.rqConfig.Bits {
 119| 			callback()

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