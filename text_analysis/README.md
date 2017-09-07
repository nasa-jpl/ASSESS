Hybrid System 1

This system is a hybrid based on

-  Tf-idf ranking of n-grams.
- Keyword extraction. And scoring of keywords based on tf-idf.

We create vectors for each standard documents (only the scope and/or the abstract) using the above two scorings. This consists of our model.
To recommend standards to a piece of text or SOW in his case, we first vectorize the SOW in the same manner as the standards. Then we perform cosine similarity between each standard vector and the SOW vector. We return a ranked list of standards (most to least similar)

Since for each document we have two vectors (one from n-grams and one from keywords). We can give relative importance of each over the other. This we do by using a hyper-parameter ‘Lamba’. Lambda can be toggled between 0 (most importance to n-grams and none to keywords) to 1 (most importance to keywords and none to n-grams). Being a hyper-parameter, the best value depends on the data, and can be determined by testing the algorithm over real data.

Hybrid System 2

This system is a hybrid based on

- TRS (refer to Technique-4) of 1-grams.
- Keyword extraction. And ranking of keywords based on TRS.

This system is also a hybrid just like system 1, but used a different technique to score the terms to create a vector. Lambda can be toggled between 0 (most importance to 1-grams and none to keywords) to 1 (most importance to keywords and none to 1-grams).
