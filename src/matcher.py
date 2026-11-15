"""
matcher.py
==========
Core matching algorithm module - TF-IDF + Cosine Similarity based
cross-border B2B smart inquiry & specification matching engine.

How it works:
  1. Load supplier product CSV (product_name + material + supplier_name as searchable text)
  2. Use scikit-learn TfidfVectorizer to vectorize product text
  3. Vectorize the buyer inquiry text the same way
  4. Compute cosine_similarity, return Top-N best matching products

Usage:
    from src.matcher import InquiryMatcher
    matcher = InquiryMatcher("data/suppliers_products.csv")
    results = matcher.match("Looking for plush squeaky dog toys, 20cm", top_n=3)
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class InquiryMatcher:
    """Smart inquiry matcher.

    Matches buyer inquiry text against the supplier product library
    using semantic similarity, returning Top-N product recommendations.

    Attributes:
        data_path (str): Path to supplier product CSV
        df (pd.DataFrame): Loaded product data
        vectorizer (TfidfVectorizer): TF-IDF vectorizer
        tfidf_matrix: TF-IDF matrix of product text
    """

    def __init__(self, data_path):
        """Initialize the matcher, load product data and build TF-IDF index.

        Args:
            data_path (str): Path to suppliers_products.csv
        """
        self.data_path = data_path
        self.df = pd.read_csv(data_path)

        # Combine product name + material + supplier name into full text for vectorization
        # This allows matching both product type (e.g. "plush toy") and material (e.g. "natural rubber")
        product_texts = (
            self.df["product_name"].fillna("") + " " +
            self.df["material"].fillna("") + " " +
            self.df.get("supplier_name", pd.Series([""] * len(self.df))).fillna("")
        )

        # Initialize TF-IDF vectorizer
        # - ngram_range=(1,2): use unigram + bigram to capture phrases like "dog toy", "rubber ball"
        # - stop_words="english": remove English stop words (a, the, for, etc.) to reduce noise
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            lowercase=True,
        )

        # fit_transform product text to build TF-IDF matrix (index)
        self.tfidf_matrix = self.vectorizer.fit_transform(product_texts)

    def match(self, buyer_text, top_n=3):
        """Match buyer inquiry text against product library, return Top-N results.

        Args:
            buyer_text (str): Buyer inquiry text, e.g.:
                "Looking for plush squeaky dog toys, size around 20cm, MOQ 500 pcs."
            top_n (int): Number of matches to return, default 3

        Returns:
            pd.DataFrame: Match result table with the following columns:
                - product_id: Product ID
                - product_name: Product name
                - material: Material
                - dimensions: Dimensions
                - moq: Minimum order quantity
                - unit_price: Unit price
                - similarity: Similarity score (0~1, higher is better)
                - similarity_pct: Similarity percentage (e.g. "89.5%")
        """
        # Vectorize buyer inquiry text (using fitted vectorizer, transform only)
        inquiry_vec = self.vectorizer.transform([buyer_text])

        # Compute cosine similarity between inquiry vector and all product vectors
        # cosine_similarity returns a matrix of shape=(1, n_products)
        similarities = cosine_similarity(inquiry_vec, self.tfidf_matrix).flatten()

        # Get Top-N indices with highest similarity
        top_indices = similarities.argsort()[-top_n:][::-1]

        # Assemble result DataFrame
        results = self.df.iloc[top_indices].copy()
        results["similarity"] = similarities[top_indices]
        results["similarity_pct"] = (results["similarity"] * 100).round(1).astype(str) + "%"

        # Sort by similarity descending
        results = results.sort_values("similarity", ascending=False).reset_index(drop=True)

        return results

    def match_batch(self, inquiries_df, top_n=3):
        """Batch match multiple inquiries.

        Args:
            inquiries_df (pd.DataFrame): DataFrame with inquiry_id and buyer_text columns
            top_n (int): Number of matches per inquiry

        Returns:
            dict: {inquiry_id: pd.DataFrame} mapping
        """
        results = {}
        for _, row in inquiries_df.iterrows():
            results[row["inquiry_id"]] = self.match(row["buyer_text"], top_n=top_n)
        return results


# ---------------------------------------------------------------------------
# CLI demo when run directly
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    # Locate data files
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "suppliers_products.csv")
    inquiries_path = os.path.join(base_dir, "data", "inquiries.csv")

    # Initialize matcher
    matcher = InquiryMatcher(data_path)

    # Demo: single inquiry match
    print("=" * 80)
    print("B2B Smart Inquiry Matcher - Demo")
    print("=" * 80)

    demo_inquiry = "Looking for plush squeaky dog toys, size around 20cm, durable material, MOQ 500 pcs."
    print(f"\n[Buyer Inquiry] {demo_inquiry}\n")

    results = matcher.match(demo_inquiry, top_n=3)

    print(f"{'Rank':<6}{'Product ID':<12}{'Product Name':<45}{'Similarity':<12}{'Price':<10}{'MOQ':<10}")
    print("-" * 95)
    for i, row in results.iterrows():
        print(f"{i+1:<6}{row['product_id']:<12}{row['product_name']:<45}{row['similarity_pct']:<12}${row['unit_price']:<9.2f}{row['moq']} pcs")

    print("\n" + "=" * 80)

    # Demo: batch matching
    if os.path.exists(inquiries_path):
        inquiries_df = pd.read_csv(inquiries_path)
        print(f"\n[Batch Match] {len(inquiries_df)} inquiries\n")

        batch_results = matcher.match_batch(inquiries_df, top_n=1)
        for inq_id, res in batch_results.items():
            if len(res) > 0:
                top = res.iloc[0]
                original_text = inquiries_df[inquiries_df["inquiry_id"] == inq_id]["buyer_text"].values[0]
                print(f"  {inq_id}: {top['product_name']} (Similarity {top['similarity_pct']})")
                print(f"         Inquiry: {original_text[:60]}...")
                print()
