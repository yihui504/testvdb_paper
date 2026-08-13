=== PACKET: weaviate_11436 ===
[vendor=weaviate version=1.37.4 defect_type=param_validation]

--- RAW ---
  [no cleaned observation available]
  [PREP PLACEHOLDER: full HTTP req/resp (REST) captured at experiment stage via probe_common raw logging]

--- CONTRACT SEGMENT ---
contract_file: v1.38.0 [derived]
- [weaviate_type_schema_create_002] properties.vectorIndexType in {hnsw, flat, dynamic, bwes} (/schema POST)
    source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json
- [weaviate_state_objects_create_001] POST /objects returns error if id exists; PUT/PATCH required to update (/objects POST)
    source: https://github.com/weaviate/weaviate/blob/v1.38.0/openapi-specs/schema.json

--- SOURCE EXCERPT ---
status: found (13314 raw hits)
// adapters/handlers/grpc/v1/parse_search_request.go  (line 33, matched: ef)
  18| 	"github.com/weaviate/weaviate/entities/modelsext"
  19| 	"github.com/weaviate/weaviate/entities/schema/configvalidation"
  20| 	"github.com/weaviate/weaviate/usecases/config"
  21| 
  22| 	"github.com/go-openapi/strfmt"
  23| 	"github.com/google/uuid"
  24| 	"github.com/pkg/errors"
  25| 	"github.com/weaviate/weaviate/adapters/handlers/graphql/local/common_filters"
  26| 	"github.com/weaviate/weaviate/adapters/handlers/grpc/v1/generative"
  27| 	"github.com/weaviate/weaviate/entities/additional"
  28| 	"github.com/weaviate/weaviate/entities/dto"
  29| 	"github.com/weaviate/weaviate/entities/filters"
  30| 	"github.com/weaviate/weaviate/entities/models"
  31| 	"github.com/weaviate/weaviate/entities/schema"
  32| 	schemaConfig "github.com/weaviate/weaviate/entities/schema/config"
  33| 	"github.com/weaviate/weaviate/entities/schema/crossref"
  34| 	"github.com/weaviate/weaviate/entities/search"
  35| 	"github.com/weaviate/weaviate/entities/searchparams"
  36| 	pb "github.com/weaviate/weaviate/grpc/generated/protocol/v1"
  37| 	"github.com/weaviate/weaviate/usecases/byteops"
  38| 	additional2 "github.com/weaviate/weaviate/usecases/modulecomponents/additional"
  39| 	"github.com/weaviate/weaviate/usecases/modulecomponents/additional/generate"
  40| 	"github.com/weaviate/weaviate/usecases/modulecomponents/additional/rank"
  41| 	"github.com/weaviate/weaviate/usecases/modulecomponents/arguments/nearAudio"
  42| 	"github.com/weaviate/weaviate/usecases/modulecomponents/arguments/nearDepth"
  43| 	"github.com/weaviate/weaviate/usecases/modulecomponents/arguments/nearImage"
  44| 	"github.com/weaviate/weaviate/usecases/modulecomponents/arguments/nearImu"
  45| 	nearText2 "github.com/weaviate/weaviate/usecases/modulecomponents/arguments/nearText"
  46| 	"github.com/weaviate/weaviate/usecases/modulecomponents/arguments/nearThermal"
  47| 	"github.com/weaviate/weaviate/usecases/modulecomponents/arguments/nearVideo"
  48| )
// adapters/handlers/graphql/local/aggregate/sparse_search.go  (line 19, matched: ef)
   4| //  \ V  V /  __/ (_| |\ V /| | (_| | ||  __/
   5| //   \_/\_/ \___|\__,_| \_/ |_|\__,_|\__\___|
   6| //
   7| //  Copyright © 2016 - 2026 Weaviate B.V. All rights reserved.
   8| //
   9| //  CONTACT: hello@weaviate.io
  10| //
  11| 
  12| package aggregate
  13| 
  14| import (
  15| 	"github.com/tailor-platform/graphql"
  16| 	"github.com/weaviate/weaviate/adapters/handlers/graphql/local/common_filters"
  17| )
  18| 
  19| func bm25Fields(prefix string) graphql.InputObjectConfigFieldMap {
  20| 	return graphql.InputObjectConfigFieldMap{
  21| 		"query": &graphql.InputObjectFieldConfig{
  22| 			Description: "The query to search for",
  23| 			Type:        graphql.String,
  24| 		},
  25| 		"properties": &graphql.InputObjectFieldConfig{
  26| 			Description: "The properties to search in",
  27| 			Type:        graphql.NewList(graphql.String),
  28| 		},
  29| 		"searchOperator": common_filters.GenerateBM25SearchOperatorFields(prefix),
  30| 	}
  31| }

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
GET /.well-known/openid-configuration -- 200 OIDC config; 404 not configured; 500 internal error

=== END PACKET ===