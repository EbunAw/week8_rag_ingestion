# Week 9: RAG Retrieval Evaluation Report

## 1. Objective

The objective of this evaluation was to compare hybrid retrieval with reranked hybrid retrieval in the Week 9 Retrieval-Augmented Generation (RAG) application. The evaluation examined whether retrieved chunks contained information directly relevant to answering a user’s question.

## 2. Evaluation Method

Three labelled questions were tested against the research paper uploaded to the application.

For each question, the top five retrieved chunks were assessed. A chunk was counted as relevant only if it directly supported answering the question.

Precision@5 was calculated as:

**Precision@5 = Number of relevant chunks in the top five ÷ 5**

The two retrieval approaches evaluated were:

- **Hybrid retrieval:** Combines keyword search and vector search using Reciprocal Rank Fusion (RRF).
- **Reranked hybrid retrieval:** Applies a CrossEncoder reranker to reorder the hybrid retrieval candidates.

## 3. Results

| Evaluation question | Hybrid P@5 | Reranked P@5 |
|---|---:|---:|
| 1. What are the two variants of RAG, and how do they differ? | 0.20 | 0.20 |
| 2. How does RAG use retrieved documents to generate an answer? | 0.20 | 0.20 |
| 3. What does the paper report about RAG-Token and RAG-Sequence on Jeopardy question generation? | 0.20 | 0.40 |
| **Mean precision@5** | **0.20** | **0.27** |

## 4. Observations

Reranked hybrid retrieval achieved a higher mean precision@5 than hybrid retrieval alone: approximately 0.27 compared with 0.20 across the three evaluation questions.

For Question 1, both approaches retrieved one directly relevant chunk among the top five. The relevant passage explains the distinction between RAG-Sequence and RAG-Token.

For Question 2, both approaches retrieved one directly relevant chunk among the top five. Reranking improved the position of the relevant chunk in the result list.

For Question 3, hybrid retrieval returned one directly relevant chunk in the top five, while reranked retrieval returned two. This indicates that reranking improved the relevance of the top-five results for this question.

Overall, the results suggest that reranking can improve the ordering of relevant passages and may increase the number of relevant chunks retrieved within the top five.

## 5. Conclusion and Limitations

In this small evaluation, reranked hybrid retrieval performed better on average than hybrid retrieval alone. However, only three labelled questions were evaluated, so the results should be treated as an initial comparison rather than a definitive performance measure.

A larger evaluation set with verified relevance labels would provide a more reliable assessment.

The `/ask` endpoint was also smoke-tested. It answered a question supported by the uploaded research paper with source citations and appropriately declined to answer an unrelated question when the document did not contain enough information.