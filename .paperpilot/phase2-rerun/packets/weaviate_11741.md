=== PACKET: weaviate_11741 ===
[vendor=weaviate version=1.38.0 defect_type=param_validation]

--- RAW ---
  [c1] POST schema TestTenant (multi-tenancy enabled) -> http=200
  [c2] control: create tenant with activityStatus='ACTIVE' -> http=200
  [c3] create tenant with activityStatus='' -> http=200
  [PREP PLACEHOLDER: full HTTP req/resp (REST) captured at experiment stage via probe_common raw logging]

--- CONTRACT SEGMENT ---
contract_file: v1.38.0
- [weaviate_type_tenants_create_001] body[].activityStatus in {ACTIVE, INACTIVE} (/schema/{className}/tenants POST)
    source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json
- [weaviate_type_tenants_update_001] body[].activityStatus in {ACTIVE, INACTIVE, OFFLOADED} (/schema/{className}/tenants PUT)
    source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json
- [weaviate_state_tenants_delete_001] after DELETE tenants, GET tenant returns 404 and its data is gone (/schema/{className}/tenants DELETE)
    source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json
- [weaviate_state_schema_delete_001] after DELETE /schema/{className}, GET /objects?class={className} returns empty (/schema/{className} DELETE)
    source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

--- SOURCE EXCERPT ---
status: found (100 raw hits)
// adapters/handlers/grpc/v1/tenants.go  (line 62, matched: activityStatus)
  47| 		}
  48| 	}
  49| 
  50| 	retTenants := make([]*pb.Tenant, len(tenants))
  51| 	for i, tenant := range tenants {
  52| 		tenantGRPC, err := tenantToGRPC(tenant)
  53| 		if err != nil {
  54| 			return nil, err
  55| 		}
  56| 		retTenants[i] = tenantGRPC
  57| 	}
  58| 	return retTenants, nil
  59| }
  60| 
  61| func tenantToGRPC(tenant *models.Tenant) (*pb.Tenant, error) {
  62| 	status, ok := pb.TenantActivityStatus_value[fmt.Sprintf("TENANT_ACTIVITY_STATUS_%s", tenant.ActivityStatus)]
  63| 	if !ok {
  64| 		return nil, fmt.Errorf("unknown tenant activity status %s", tenant.ActivityStatus)
  65| 	}
  66| 
  67| 	return &pb.Tenant{
  68| 		Name:           tenant.Name,
  69| 		ActivityStatus: pb.TenantActivityStatus(status),
  70| 	}, nil
  71| }
// adapters/handlers/rest/embedded_spec.go  (line 10415, matched: activityStatus)
10400|           "type": "string"
10401|         },
10402|         "removals": {
10403|           "description": "Stopwords to be removed from consideration (default: []). Can be any array of custom strings.",
10404|           "type": "array",
10405|           "items": {
10406|             "type": "string"
10407|           }
10408|         }
10409|       }
10410|     },
10411|     "Tenant": {
10412|       "description": "Attributes representing a single tenant within Weaviate.",
10413|       "type": "object",
10414|       "properties": {
10415|         "activityStatus": {
10416|           "description": "The activity status of the tenant, which determines if it is queryable and where its data is stored.\u003cbr/\u003e\u003cbr/\u003e\u003cb\u003eAvailable Statuses:\u003c/b\u003e\u003cbr/\u003e- ` + "`" + `ACTIVE` + "`" + `: The tenant is fully operational and ready for queries. Data is stored on local, hot storage.\u003cbr/\u003e- ` + "`" + `INACTIVE` + "`" + `: The tenant is not queryable. Data is stored locally.\u003cbr/\u003e- ` + "`" + `OFFLOADED` + "`" + `: The tenant is inactive and its data is stored in a remote cloud backend.\u003cbr/\u003e\u003cbr/\u003e\u003cb\u003eUsage Rules:\u003c/b\u003e\u003cbr/\u003e- \u003cb\u003eOn Create:\u003c/b\u003e This field is optional and defaults to ` + "`" + `ACTIVE` + "`" + `. Allowed values are ` + "`" + `ACTIVE` + "`" + ` and ` + "`" + `INACTIVE` + "`" + `.\u003cbr/\u003e- \u003cb\u003eOn Update:\u003c/b\u003e This field is required. Allowed values are ` + "`" + `ACTIVE` + "`" + `, ` + "`" + `INACTIVE` + "`" + `, and ` + "`" + `OFFLOADED` + "`" + `.\u003cbr/\u003e\u003cbr/\u003e\u003cb\u003eRead-Only Statuses:\u003c/b\u003e\u003cbr/\u003eThe following statuses are set by the server and indicate a tenant is transitioning between states:\u003cbr/\u003e- ` + "`" + `OFFLOADING` + "`" + `\u003cbr/\u003e- ` + "`" + `ONLOADING` + "`" + `\u003cbr/\u003e\u003cbr/\u003e\u003cb\u003eNote on Deprecated Names:\u003c/b\u003e\u003cbr/\u003eFor backward compatibility, deprecated names are still accepted and are mapped to their modern equivalents: ` + "`" + `HOT` + "`" + ` (now ` + "`" + `ACTIVE` + "`" + `), ` + "`" + `COLD` + "`" + ` (now ` + "`" + `INACTIVE` + "`" + `), ` + "`" + `FROZEN` + "`" + ` (now ` + "`" + `OFFLOADED` + "`" + `), ` + "`" + `FREEZING` + "`" + ` (now ` + "`" + `OFFLOADING` + "`" + `), ` + "`" + `UNFREEZING` + "`" + ` (now ` + "`" + `ONLOADING` + "`" + `).",
10417|           "type": "string",
10418|           "enum": [
10419|             "ACTIVE",
10420|             "INACTIVE",
10421|             "OFFLOADED",
10422|             "OFFLOADING",
10423|             "ONLOADING",
10424|             "HOT",
10425|             "COLD",
10426|             "FROZEN",
10427|             "FREEZING",
10428|             "UNFREEZING"
10429|           ]
10430|         },

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
PUT /schema/{className}/tenants -- Update tenants (activityStatus on update: ACTIVE|INACTIVE|OFFLOADED)

=== END PACKET ===