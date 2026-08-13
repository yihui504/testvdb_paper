=== PACKET: milvus_47755 ===
[vendor=milvus version=2.6.10 defect_type=param_validation]

--- RAW ---
  [c1] search with descending IN range -> http=200, code=0, 1 result
  [c2] search with empty IN range -> http=200, code=0, 0 results
  [PREP PLACEHOLDER: full HTTP req/resp (REST) captured at experiment stage via probe_common raw logging]

--- CONTRACT SEGMENT ---
contract_file: v2.6.17 [derived]
- [milvus_type_collections_drop_001] collectionName is non-empty string (collections+drop)
    source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md
- [milvus_type_collections_load_001] collectionName is non-empty string (collections+load)
    source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md
- [milvus_type_collections_rename_001] collectionName is non-empty string AND newCollectionName is non-empty string (collections+rename)
    source: https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md
- [milvus_type_partitions_create_001] partitionName is non-empty string (partitions+create)
    source: https://github.com/milvus-io/milvus/blob/v2.6.17/internal/distributed/proxy/httpserver/constant.go

--- SOURCE EXCERPT ---
status: found (1778 raw hits)
// internal/distributed/proxy/httpserver/handler_v1.go  (line 510, matched: Filter)
 495| 
 496| func (h *HandlersV1) query(c *gin.Context) {
 497| 	httpReq := QueryReq{
 498| 		DbName:       DefaultDbName,
 499| 		Limit:        100,
 500| 		OutputFields: []string{DefaultOutputFields},
 501| 	}
 502| 	if err := c.ShouldBindWith(&httpReq, binding.JSON); err != nil {
 503| 		log.Warn("high level restful api, the parameter of query is incorrect", zap.Any("request", httpReq), zap.Error(err))
 504| 		HTTPAbortReturn(c, http.StatusOK, gin.H{
 505| 			HTTPReturnCode:    merr.Code(merr.ErrIncorrectParameterFormat),
 506| 			HTTPReturnMessage: merr.ErrIncorrectParameterFormat.Error() + ", error: " + err.Error(),
 507| 		})
 508| 		return
 509| 	}
 510| 	if httpReq.CollectionName == "" || httpReq.Filter == "" {
 511| 		log.Warn("high level restful api, query require parameter: [collectionName, filter], but miss")
 512| 		HTTPAbortReturn(c, http.StatusOK, gin.H{
 513| 			HTTPReturnCode:    merr.Code(merr.ErrMissingRequiredParameters),
 514| 			HTTPReturnMessage: merr.ErrMissingRequiredParameters.Error() + ", required parameters: [collectionName, filter]",
 515| 		})
 516| 		return
 517| 	}
 518| 	req := &milvuspb.QueryRequest{
 519| 		DbName:             httpReq.DbName,
 520| 		CollectionName:     httpReq.CollectionName,
 521| 		Expr:               httpReq.Filter,
 522| 		OutputFields:       httpReq.OutputFields,
 523| 		GuaranteeTimestamp: BoundedTimestamp,
 524| 		QueryParams:        []*commonpb.KeyValuePair{},
 525| 	}
// internal/distributed/proxy/httpserver/handler_v2.go  (line 225, matched: Filter)
 210| 	// Query
 211| 	router.POST(EntityCategory+QueryAction, restfulSizeMiddleware(timeoutMiddleware(wrapperPost(func() any {
 212| 		return &QueryReqV2{
 213| 			Limit:        100,
 214| 			OutputFields: []string{DefaultOutputFields},
 215| 		}
 216| 	}, wrapperTraceLog(h.query))), true))
 217| 	// Get
 218| 	router.POST(EntityCategory+GetAction, restfulSizeMiddleware(timeoutMiddleware(wrapperPost(func() any {
 219| 		return &CollectionIDReq{
 220| 			OutputFields: []string{DefaultOutputFields},
 221| 		}
 222| 	}, wrapperTraceLog(h.get))), true))
 223| 	// Delete
 224| 	router.POST(EntityCategory+DeleteAction, restfulSizeMiddleware(timeoutMiddleware(wrapperPost(func() any {
 225| 		return &CollectionFilterReq{}
 226| 	}, wrapperTraceLog(h.delete))), false))
 227| 	// Insert
 228| 	router.POST(EntityCategory+InsertAction, restfulSizeMiddleware(timeoutMiddleware(wrapperPost(func() any {
 229| 		return &CollectionDataReq{}
 230| 	}, wrapperTraceLog(h.insert))), false))
 231| 	// Upsert
 232| 	router.POST(EntityCategory+UpsertAction, restfulSizeMiddleware(timeoutMiddleware(wrapperPost(func() any {
 233| 		return &CollectionDataReq{}
 234| 	}, wrapperTraceLog(h.upsert))), false))
 235| 	// Search
 236| 	router.POST(EntityCategory+SearchAction, restfulSizeMiddleware(timeoutMiddleware(wrapperPost(func() any {
 237| 		return &SearchReqV2{
 238| 			Limit: 100,
 239| 		}
 240| 	}, wrapperTraceLog(h.search))), true))

--- COGNITION (developer_cognition.json, full vendor) ---
{
 "_meta": {
  "generated_at": "2026-08-06T10:00:00Z",
  "total_issues_analyzed": 161
 },
 "developer_cognition_signals": {
  "what_developers_prioritize": [
   "Performance optimization over data validation (REST v2 issues persist)",
   "Feature development over edge case handling (segment lifecycle)",
   "Index functionality over data safety (compaction errors)"
  ],
  "blindspot_indicators": [
   "REST v2 API data type serialization - 8 issues in corpus",
   "Segment state machine violations - 15+ issues",
   "Snapshot isolation broken during concurrent operations - 7 issues",
   "Memory admission control bypassed - 6 OOM issues",
   "RBAC privilege annotations incomplete - 5 security issues",
   "Concurrent operation edge cases - 12 deadlock/hang issues"
  ],
  "areas_with_repeated_issues": [
   {
    "area": "REST v2 API",
    "issue_count": 25,
    "pattern": "Data type serialization not validated",
    "example_issues": [
     52232,
     52230,
     52229
    ]
   },
   {
    "area": "Segment Management",
    "issue_count": 25,
    "pattern": "State machine violations during lifecycle transitions",
    "example_issues": [
     52201,
     52199,
     52195
    ]
   },
   {
    "area": "Concurrency Control",
    "issue_count": 15,
    "pattern": "Deadlocks and hangs in concurrent DML/DQL",
    "example_issues": [
     52233,
     52178,
     52154
    ]
   }
  ]
 },
 "rejection_patterns": [
  {
   "pattern_id": "RP-001",
   "rejection_reason": "expected_behavior",
   "description": "Issue rejected as expected system behavior",
   "examples": [
    "load partition stuck at 50%",
    "channel checkpoint lag increasing"
   ],
   "attack_guidance": "Verify against documentation, check if behavior matches documented contract"
  },
  {
   "pattern_id": "RP-002",
   "rejection_reason": "by_design",
   "description": "Issue rejected as intentional design choice",
   "examples": [
    "uneven vchannel distribution",
    "memory imbalance"
   ],
   "attack_guidance": "Design may prioritize scalability over perfect balance"
  }
 ],
 "by_design_patterns": [
  {
   "pattern_id": "BDP-001",
   "pattern": "Storage V3 excludes uncommitted segments from snapshots",
   "endpoint": "Storage V3 snapshot/restore",
   "developer_quote": "uncommitted V3 growing segments intentionally excluded",
   "source_issue_numbers": [
    52043
   ],
   "should_report": false,
   "classification": "Type4_StateViolation — FALSE POSITIVE",
   "attack_guidance": "DO NOT report missing uncommitted segments as defect. Team explicitly excludes them from snapshots for correctness."
  },
  {
   "pattern_id": "BDP-002",
   "pattern": "Rollback from 3.0 to 2.6 not supported",
   "endpoint": "Version downgrade",
   "developer_quote": "index store path version incompatibility - rollback not supported",
   "source_issue_numbers": [
    51788
   ],
   "should_report": false,
   "classification": "deployment_mismatch — FALSE POSITIVE",
   "attack_guidance": "DO NOT report rollback failures. Downgrade not supported by design."
  }
 ],
 "statistics": {
  "total_blindspot_areas": 6,
  "high_frequency_blindspots": [
   "REST_v2_data_types",
   "Segment_state_management",
   "Concurrency_control"
  ],
  "rejection_patterns_count": 2,
  "by_design_patterns_count": 2
 }
}

--- BUG SHAPES (bug_shapes.json, full vendor) ---
{
 "_meta": {
  "generated_at": "2026-08-06T10:00:00Z",
  "total_issues_analyzed": 161,
  "total_prs_analyzed": 100
 },
 "bug_shapes": [
  {
   "shape_id": "rest-v2-data-type-handling",
   "name": "REST_v2_data_type_handling",
   "affected_layer": "api_gateway",
   "defect_type": "Type1_IllegalSuccess",
   "description": "REST v2 API fails to properly serialize/deserialize complex data types",
   "symptoms": [
    "Returns wrong values for large integers",
    "Array fields in raw protobuf format",
    "AutoId not working for Int64 PK"
   ],
   "historical_instances": [
    {
     "number": 52232,
     "title": "[Bug]: avoid index build task fails for 0 element in nested array index",
     "state": "open",
     "labels": [
      "kind/bug",
      "needs-triage"
     ]
    },
    {
     "number": 52230,
     "title": "[Bug]: Incorrect Content-Type for JSON responses on port 9091",
     "state": "open",
     "labels": [
      "kind/bug",
      "needs-triage"
     ]
    },
    {
     "number": 52229,
     "title": "Incorrect Content-Type for JSON responses on port 9091",
     "state": "closed",
     "labels": []
    },
    {
     "number": 52212,
     "title": "[Bug]: REST insert stores invalid JSON for a JSON field holding a string or an out-of-range number",
     "state": "open",
     "labels": []
    },
    {
     "number": 52188,
     "title": "[Bug]: REST v2 large search responses are fully buffered, causing high latency and memory amplification",
     "state": "open",
     "labels": [
      "kind/bug",
      "area/performance",
      "priority/critical-urgent",
      "area/api",
      "triage/accepted"
     ]
    }
   ],
   "instance_count": 26,
   "confidence": 0.95
  },
  {
   "shape_id": "segment-lifecycle-corruption",
   "name": "Segment_lifecycle_corruption",
   "affected_layer": "storage_engine",
   "defect_type": "Type4_StateViolation",
   "description": "Segment state machine violations leading to data corruption or loss",
   "symptoms": [
    "Silent data loss during compaction",
    "Incorrect segment handoff",
    "Flush errors"
   ],
   "historical_instances": [
    {
     "number": 52201,
     "title": "[Bug]: Clustering compaction ignores record-boundary cluster-buffer Flush errors, allowing partial-write replay and per-field file divergence",
     "state": "open",
     "labels": []
    },
    {
     "number": 52199,
     "title": "[Bug]: Flushed segment remains on the growing query path after snapshot protection rejects sort compaction",
     "state": "open",
     "labels": [
      "kind/bug",
      "needs-triage"
     ]
    },
    {
     "number": 52195,
     "title": "Track vector index size in segment statistics",
     "state": "open",
     "labels": []
    },
    {
     "number": 52191,
     "title": "[Bug]: geometry cache uses a reader-preferring shared_mutex, allowing per-row writer starvation on the growing insert path",
     "state": "open",
     "labels": [
      "kind/bug",
      "severity/minor",
      "component/querynode"
     ]
    },
    {
     "number": 52178,
     "title": "[Bug]: Compaction workers swallow writer errors and crash/hang on abnormal inputs, allowing silent row loss",
     "state": "open",
     "labels": []
    }
   ],
   "instance_count": 27,
   "confidence": 0.95
  },
  {
   "shape_id": "snapshot-consistency-violations",
   "name": "Snapshot_consistency_violations",
   "affected_layer": "storage_engine",
   "defect_type": "Type4_StateViolation",
   "description": "Snapshot isolation broken by including uncommitted data or missing committed data",
   "symptoms": [
    "Uncommitted V3 manifests in snapshots",
    "Missing committed rows after restore"
   ],
   "historical_instances": [
    {
     "number": 52202,
     "title": "[Bug]: Snapshot restore resets consistency level and drops collection properties",
     "state": "open",
     "labels": [
      "kind/bug",
      "priority/critical-urgent",
      "severity/critical",
      "triage/accepted",
      "feature/snapshot"
     ]
    },
    {
     "number": 52199,
     "title": "[Bug]: Flushed segment remains on the growing query path after snapshot protection rejects sort compaction",
     "state": "open",
     "labels": [
      "kind/bug",
      "needs-triage"
     ]
    },
    {
     "number": 52149,
     "title": "[Bug]: Clustering compaction drops commit_timestamp and silently deletes committed import rows",
     "state": "open",
     "labels": [
      "kind/bug",
      "triage/accepted"
     ]
    },
    {
     "number": 52125,
     "title": "[Bug]: Azure CopyObject uses async StartCopyFromURL without polling copy status — snapshot restore can report success before data is copied",
     "state": "open",
     "labels": []
    },
    {
     "number": 52112,
     "title": "[Bug]: Search parses naive TIMESTAMPTZ filters before resolving timezone",
     "state": "open",
     "labels": [
      "kind/bug"
     ]
    }
   ],
   "instance_count": 9,
   "confidence": 0.95
  },
  {
   "shape_id": "concurrency-deadlocks",
   "name": "Concurrency_deadlocks",
   "affected_layer": "business_logic",
   "defect_type": "Type3_RuntimeFailure",
   "description": "Concurrent operations cause deadlocks or hangs",
   "symptoms": [
    "StreamingNode deadlock with HWM sealing",
    "QueryNode hangs during recovery"
   ],
   "historical_instances": [
    {
     "number": 52233,
     "title": "[Bug]: [Benchmark][Standalone] Milvus crashes during concurrent insert/search/upsert with custom scalar and vector fields",
     "state": "open",
     "labels": [
      "kind/bug",
      "triage/accepted",
      "test/benchmark"
     ]
    },
    {
     "number": 52178,
     "title": "[Bug]: Compaction workers swallow writer errors and crash/hang on abnormal inputs, allowing silent row loss",
     "state": "open",
     "labels": []
    },
    {
     "number": 52154,
     "title": "[Bug]: Import job deadlocks with concurrent add_function_field: IndexBuilding waits for a bound index that cannot build before commit",
     "state": "open",
     "labels": []
    },
    {
     "number": 52139,
     "title": "[Bug]: Streaming QueryNodes can block sealed segment balancing in channel-exclusive mode",
     "state": "open",
     "labels": [
      "kind/bug",
      "needs-triage"
     ]
    },
    {
     "number": 52092,
     "title": "[Bug]: ScoreBasedBalancer's scoreUnbalanceTolerationFactor check never blocks moves once target priority goes negative",
     "state": "open",
     "labels": []
    }
   ],
   "instance_count": 15,
   "confidence": 0.95
  },
  {
   "shape_id": "memory-management-failures",
   "name": "Memory_management_failures",
   "affected_layer": "resource_management",
   "defect_type": "Type3_RuntimeFailure",
   "description": "Memory not properly managed leading to OOM or leaks",
   "symptoms": [
    "DataNode OOM from oversized tasks",
    "Unbounded memory growth"
   ],
   "historical_instances": [
    {
     "number": 52188,
     "title": "[Bug]: REST v2 large search responses are fully buffered, causing high latency and memory amplification",
     "state": "open",
     "labels": [
      "kind/bug",
      "area/performance",
      "priority/critical-urgent",
      "area/api",
      "triage/accepted"
     ]
    },
    {
     "number": 52180,
     "title": "[Bug]: DataNode OOM because oversized index and multi-GiB MixCompaction tasks bypass slot admission",
     "state": "open",
     "labels": [
      "kind/bug",
      "area/performance",
      "triage/accepted"
     ]
    },
    {
     "number": 52178,
     "title": "[Bug]: Compaction workers swallow writer errors and crash/hang on abnormal inputs, allowing silent row loss",
     "state": "open",
     "labels": []
    },
    {
     "number": 51902,
     "title": "[Bug]: disk write worker pool swallows write failures and drops queued writes on reconfig",
     "state": "open",
     "labels": [
      "kind/bug",
      "needs-triage"
     ]
    },
    {
     "number": 51799,
     "title": "[Bug]: C++ unit tests mutate process-global SegcoreConfig (inline static); chunk_rows=2 leak causes deterministic UT shard timeouts",
     "state": "closed",
     "labels": []
    }
   ],
   "instance_count": 6,
   "confidence": 0.95
  },
  {
   "shape_id": "rbac-authorization-gaps",
   "name": "RBAC_authorization_gaps",
   "affected_layer": "authentication_authorization",
   "defect_type": "Type1_IllegalSuccess",
   "description": "Authorization checks missing or incomplete",
   "symptoms": [
    "Missing RBAC on diagnostic endpoints",
    "Privilege annotation missing on RPCs"
   ],
   "historical_instances": [
    {
     "number": 52238,
     "title": "[Bug]: DumpMessages WAL salvage stream lacks RBAC authorization",
     "state": "open",
     "labels": [
      "kind/bug"
     ]
    },
    {
     "number": 52237,
     "title": "[Bug]: RunAnalyzer collection-scoped path lacks RBAC privilege annotation",
     "state": "open",
     "labels": [
      "kind/bug"
     ]
    },
    {
     "number": 52236,
     "title": "[Bug]: MilvusService RPCs can miss RBAC privilege annotations without CI failure",
     "state": "open",
     "labels": [
      "kind/bug"
     ]
    },
    {
     "number": 52197,
     "title": "[Bug]: RBAC backup repeats tenant-wide grantee scans",
     "state": "open",
     "labels": [
      "kind/bug",
      "needs-triage"
     ]
    },
    {
     "number": 52038,
     "title": "[Bug]: Credential material can be written to Milvus logs",
     "state": "open",
     "labels": [
      "kind/bug",
      "needs-triage"
     ]
    }
   ],
   "instance_count": 6,
   "confidence": 0.95
  }
 ],
 "statistics": {
  "total_shapes_identified": 6,
  "high_confidence_shapes": 6,
  "most_frequent_layers": {
   "api_gateway": 1,
   "storage_engine": 2,
   "business_logic": 1,
   "resource_management": 1,
   "authentication_authorization": 1
  },
  "defect_type_distribution": {
   "Type1_IllegalSuccess": 2,
   "Type4_StateViolation": 2,
   "Type3_RuntimeFailure": 2
  }
 }
}

--- API TEMPLATE ---
POST entities+delete -- 200 on success; 400 on invalid filter expression

=== END PACKET ===