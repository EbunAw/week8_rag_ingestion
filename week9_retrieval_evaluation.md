
# Week 9: Hybrid Retrieval and Reranking Evaluation

## Objective

The objective of this evaluation was to assess whether combining keyword and vector retrieval, followed by reranking, improved the relevance of retrieved passages for document-based question answering.

## Method

Three labelled questions were tested against the document collection using:

- **Hybrid retrieval:** combined keyword and vector search using Reciprocal Rank Fusion (RRF).
- **Reranking:** reordered the retrieved candidates using a CrossEncoder.
- **Evaluation metric:** Precision@5 (P@5), calculated as the number of passages in the top five that directly support answering the question, divided by five.

A passage was counted as relevant only if it directly supported the answer—not merely because it mentioned a related topic.

## Results

| Question | Hybrid P@5 | Reranked P@5 |
|---|---:|---:|
| What are the two variants of RAG, and how do they differ? | 0.00 | 0.20 |
| How does RAG use retrieved documents to generate an answer? | 0.20 | 0.20 |
| What does the paper report about RAG-Token and RAG-Sequence on Jeopardy question generation? | 0.20 | 0.40 |
| **Mean P@5** | **0.13** | **0.27** |

## Observations

- For the first question, the hybrid top-five results included a passage comparing the variants’ Jeopardy performance, but it did not directly explain how RAG-Token and RAG-Sequence differ. The reranked results placed a passage that directly explained the distinction in the top five.
- For the second question, both methods retrieved one passage in the top five that directly supported the answer.
- For the third question, reranking increased the number of directly relevant passages in the top five from one to two. It also moved the passage reporting the Jeopardy comparison to the first position.

## Conclusion and Limitations

Across these three test questions, reranking improved mean Precision@5 from approximately **0.13 to 0.27**. The results suggest that reranking helped prioritize relevant passages, although the evaluation set was small.

This evaluation measures retrieval relevance, not the factual accuracy or quality of the generated answers. A larger labelled test set would be needed to draw stronger conclusions.
