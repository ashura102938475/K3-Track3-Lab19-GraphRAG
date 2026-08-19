# Báo cáo thực hành — Lab 19: GraphRAG vs Flat RAG

**Học viên:** Người thực hiện repo · **Ngày:** 19/08/2026
**Chế độ kiểm chứng:** Live smoke run trên HackerNoon subset, NVIDIA LLM, Jina embeddings và local Neo4j.

## 1. Thuyết minh kỹ thuật

1. **Coreference:** Khi một chunk vừa nhắc đến hai công ty, “the company” có thể mơ hồ. Resolver phải giữ nguyên câu và ghi `unresolved_mentions`; resolve sai sẽ tạo false edge.
2. **Entity resolution:** Dùng cosine candidate `0.90` rồi lexical guard. `Apple` và `Apple Music` có thể gần nhau về embedding nhưng khác loại/thực thể, nên bị `REJECT_GUARD`.
3. **Super-node:** Degree >100 bị giới hạn 50 cạnh mới nhất; toàn context tối đa 250 cạnh. Cách này giảm token/latency nhưng có thể bỏ sót sự kiện lịch sử.
4. **Benchmark live:** Golden set chạy đủ 5 câu (`G01–G05`). Trung bình Flat RAG: comprehensiveness 3.8, faithfulness 3.8, multi-hop 3.4, latency 1.488s, 751.2 tokens. GraphRAG: lần lượt 3.6, 3.0, 3.0, 9.033s, 1038.8 tokens. Kết quả cho thấy GraphRAG trong smoke run đắt hơn nhưng chưa thắng về quality; đây là tín hiệu cần cải thiện extraction/seed/context, không phải bằng chứng GraphRAG luôn kém.
5. **Failure Flat RAG:** G03 cần nối Microsoft→OpenAI với Microsoft→Azure. Vector ranking có thể lấy thiếu một chunk; graph traversal nối được hai bằng chứng.
6. **Failure GraphRAG:** G05 có thể mất cạnh cũ vì recency pruning. Cần route theo ngôn ngữ thời gian hoặc truy vấn lịch sử riêng.
7. **Trade-off:** GraphRAG tăng indexing/extraction và retrieval cost, đổi lại cải thiện multi-hop/cross-document reasoning.
8. **Agent control:** Không dùng pairwise entity comparison O(N²); thay bằng ANN candidate blocking, lexical guard và audit.
9. **Scale:** Với 350MB, bottleneck đầu tiên dự kiến là LLM extraction/rate limit, sau đó embedding và graph writes. Giải pháp là queue async, cache, ANN, community partitioning và `UNWIND` batches.
10. **Provenance:** Mọi edge phải có `source_chunk_id`, `published_date`, `evidence`, `confidence`; đây là điều kiện để audit và trích dẫn câu trả lời.

## 2. Mapping bài giảng vào code

| Khái niệm | Module | Bằng chứng |
|---|---|---|
| Conservative coreference | 1 | `resolve_coref_batch()` |
| Schema/allowlist | 2 | `ALLOWED_NODE_TYPES`, `ALLOWED_RELATIONS` |
| Bulk ingestion | 2 | `UNWIND $rows AS row` |
| Entity resolution | 3 | vector candidate + lexical guard + audit |
| Super-node cap | 4 | `SUPER_NODE_EDGE_CAP`, `GLOBAL_EDGE_CAP` |
| LLM judge | 5 | Ba điểm 1–5 và rationale |

## 3. Reflection và action plan

Bài học chính là tách contract deterministic khỏi dịch vụ bên ngoài: live run đo được model/Neo4j, còn contract tests bảo vệ schema, cap, provenance và export.

Đối với đồ án thực tế, bắt đầu bằng Flat RAG cho factoid. Chỉ thêm graph khi golden set chứng minh nhu cầu multi-hop. Dùng typed nodes, provenance-backed edges, ANN blocking, guard rejection và route-level observability.

| Tiêu chí | Tự đánh giá (1–5) |
|---|---:|
| Hiểu GraphRAG | 4 |
| Kiểm soát AI agent | 4 |
| Kỷ luật chất lượng đồ thị | 4 |
| Debug/evaluation | 4 |
