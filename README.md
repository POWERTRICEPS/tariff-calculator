# Tariff Calculator – AI-Powered Trade Duty Estimator
-----------------------------------------------------
The Tariff Calculator is an AI-powered web application that helps importers and businesses estimate customs duties on products based on their HTS (Harmonized Tariff Schedule) code and country of origin. It combines machine learning, natural language embeddings, and trade rules to provide accurate, real-time duty calculations.


## Features
------------------------------------------
- Matches product descriptions to the closest HTS codes using OpenAI embeddings + FAISS vector search

- Returns Column 1 base duty rates, special trade program exemptions, and additional tariffs (e.g., Section 301, steel, aluminum, auto, fentanyl, reciprocal tariffs)

- Handles country-of-origin logic with trade agreements and exemptions

- FastAPI backend with clear REST endpoints for integration into other systems

- Designed for scalability as a SaaS product

## How It Works
----------------------------------------
- Product Input – User provides a product description and country of origin.

- HTS Code Matching – Description is embedded and compared in a FAISS vector index to find the most relevant HTS codes.

- Tariff Calculation – For the chosen HTS code, the system checks:

- Column 1 base duty rate

- Special trade programs (FTA, GSP, etc.)

- Section 301 tariffs (China)

- Fentanyl/reciprocal tariffs (9903.0124 / 9903.0125)

- Steel, aluminum, and auto tariffs

- Result Output – Returns a detailed duty breakdown including HTS code, description, base duty, exemptions, and applied surcharges.
