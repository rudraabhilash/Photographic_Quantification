PRODUCTS = [
    {"id": 1, "name": "iPhone 15", "category": "electronics", "price": 800},
    {"id": 2, "name": "MacBook Air", "category": "electronics", "price": 1200},
    {"id": 3, "name": "Running Shoes", "category": "sports", "price": 120},
    {"id": 4, "name": "Noise Cancelling Headphones", "category": "electronics", "price": 300},
    {"id": 5, "name": "Yoga Mat", "category": "sports", "price": 40},
]


user_profile = {
    "interests": ["electronics", "fitness"],
    "budget": 500,
    "previous_purchases": ["iPhone 13"]
}

from openai import OpenAI

client = OpenAI()

def recommend_products(user_profile, products):
    prompt = f"""
You are a recommendation agent.

User profile:
{user_profile}

Available products:
{products}

Rules:
- Recommend max 3 products
- Stay within user's budget
- Prefer user's interests
- Explain briefly why each item is recommended

Return JSON with fields:
id, name, reason
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
if __name__ == "__main__":
    recommendations = recommend_products(user_profile, PRODUCTS)
    print(recommendations)

# output
# [
#   {
#     "id": 4,
#     "name": "Noise Cancelling Headphones",
#     "reason": "Matches electronics interest and fits within budget."
#   },
#   {
#     "id": 3,
#     "name": "Running Shoes",
#     "reason": "Supports fitness interest and reasonably priced."
#   }
# ]
