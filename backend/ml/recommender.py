"""Hybrid recommender: content + collaborative behavior similarity."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Recommendation:
    book_id: str
    title: str
    author: str
    score: float
    reasons: List[str]


def _normalize(series: pd.Series) -> pd.Series:
    if series.empty:
        return series
    max_val = series.max()
    min_val = series.min()
    if max_val == min_val:
        return pd.Series(np.ones(len(series)), index=series.index)
    return (series - min_val) / (max_val - min_val)


def build_hybrid_recommendations(user_id: str, books: list[dict], behaviors: list[dict], top_n: int = 5) -> List[Recommendation]:
    books_df = pd.DataFrame(books)
    if books_df.empty:
        return []

    # Content-based part (TF-IDF over descriptions)
    books_df["description"] = books_df["description"].fillna("")
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(books_df["description"])
    content_sim_matrix = cosine_similarity(tfidf_matrix)

    behaviors_df = pd.DataFrame(behaviors)
    if behaviors_df.empty:
        popular = books_df.head(top_n)
        return [
            Recommendation(
                book_id=row["_id"],
                title=row["title"],
                author=row["author"],
                score=0.1,
                reasons=["Cold start recommendation from catalog"],
            )
            for _, row in popular.iterrows()
        ]

    # Weighted interaction score from richer behavior signals.
    for col in ["time_spent_minutes", "pages_read", "click_frequency", "liked_count", "saved_count"]:
        if col not in behaviors_df.columns:
            behaviors_df[col] = 0

    behaviors_df["interaction_score"] = (
        0.30 * _normalize(behaviors_df["time_spent_minutes"]) +
        0.25 * _normalize(behaviors_df["pages_read"]) +
        0.20 * _normalize(behaviors_df["click_frequency"]) +
        0.15 * _normalize(behaviors_df["liked_count"]) +
        0.10 * _normalize(behaviors_df["saved_count"])
    )

    # Collaborative filtering: user-user similarity on behavior pivot.
    user_item = behaviors_df.pivot_table(
        index="user_id",
        columns="book_id",
        values="interaction_score",
        fill_value=0.0,
        aggfunc="mean",
    )

    if user_id not in user_item.index:
        user_item.loc[user_id] = 0.0

    user_similarity = cosine_similarity(user_item)
    user_sim_df = pd.DataFrame(user_similarity, index=user_item.index, columns=user_item.index)
    similar_users = user_sim_df[user_id].drop(labels=[user_id], errors="ignore").sort_values(ascending=False)

    collaborative_scores = pd.Series(0.0, index=user_item.columns)
    for sim_user_id, sim_score in similar_users.items():
        if sim_score <= 0:
            continue
        collaborative_scores = collaborative_scores.add(user_item.loc[sim_user_id] * sim_score, fill_value=0)

    # Content score based on user's positively engaged books.
    user_behaviors = behaviors_df[behaviors_df["user_id"] == user_id]
    liked_books = user_behaviors.sort_values("interaction_score", ascending=False)["book_id"].tolist()
    content_scores = pd.Series(0.0, index=books_df["_id"])

    for book_id in liked_books[:5]:
        idx_list = books_df.index[books_df["_id"] == book_id].tolist()
        if not idx_list:
            continue
        idx = idx_list[0]
        content_scores = content_scores.add(pd.Series(content_sim_matrix[idx], index=books_df["_id"]), fill_value=0)

    content_scores = _normalize(content_scores)
    collaborative_scores = _normalize(collaborative_scores.reindex(books_df["_id"]).fillna(0.0))

    hybrid_scores = 0.55 * content_scores + 0.45 * collaborative_scores

    seen_books = set(user_behaviors["book_id"].tolist())
    candidates = books_df[~books_df["_id"].isin(seen_books)].copy()
    if candidates.empty:
        candidates = books_df.copy()

    candidates["hybrid_score"] = candidates["_id"].map(hybrid_scores).fillna(0.0)
    candidates = candidates.sort_values("hybrid_score", ascending=False).head(top_n)

    recommendations: List[Recommendation] = []
    for _, row in candidates.iterrows():
        reasons = ["Similar content to books you engaged with"]
        if collaborative_scores.get(row["_id"], 0.0) > 0.05:
            reasons.append("Users with similar behavior also engaged this book")

        recommendations.append(
            Recommendation(
                book_id=row["_id"],
                title=row["title"],
                author=row["author"],
                score=float(round(row["hybrid_score"], 4)),
                reasons=reasons,
            )
        )

    return recommendations
