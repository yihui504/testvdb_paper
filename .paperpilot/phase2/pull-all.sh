#!/bin/bash
# 批量拉取 Phase 2 所需镜像(已有则跳过)
imgs=(
  milvusdb/milvus:v2.3.22
  milvusdb/milvus:v2.6.10
  milvusdb/milvus:v2.6.12
  milvusdb/milvus:v2.6.16
  milvusdb/milvus:v2.6.17
  milvusdb/milvus:v2.6.19
  milvusdb/milvus:v3.0.0
  qdrant/qdrant:v1.12.1
  qdrant/qdrant:v1.17.1
  qdrant/qdrant:v1.18.0
  qdrant/qdrant:v1.18.1
  qdrant/qdrant:v1.18.2
  qdrant/qdrant:v1.18.3
  semitechnologies/weaviate:1.37.4
  semitechnologies/weaviate:1.38.0
  semitechnologies/weaviate:1.38.2
)
for img in "${imgs[@]}"; do
  if docker images --format '{{.Repository}}:{{.Tag}}' | grep -qx "$img"; then
    echo "SKIP (exists): $img"
    continue
  fi
  echo "PULL: $img"
  if ! docker pull "$img" > /dev/null 2>&1; then
    echo "FAIL: $img"
  else
    echo "OK: $img"
  fi
done
echo "ALL DONE"
