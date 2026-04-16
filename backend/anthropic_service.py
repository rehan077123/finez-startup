"""
Anthropic API Service for FineZ
Handles AI-powered features including intent parsing, recommendations, and content generation
"""

import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import anthropic

logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "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")
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"  # Latest Claude model


class AnthropicService:
    """Service to handle Anthropic Claude API requests for AI features."""

    def __init__(self):
        """Initialize Anthropic client."""
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def parse_search_intent(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Parse user search query to extract intent and entities.
        Uses Claude to understand what the user is really looking for.
        
        Args:
            query: User's search query
            context: Optional context like user history, preferences
        
        Returns:
            Dict with intent, entities, category, and recommendations
        """
        try:
            system_prompt = """You are an e-commerce search intent analyzer for FineZ, an Indian product discovery platform.
            
Analyze the user's search query and extract:
1. Primary Intent: What does the user want? (e.g., "price_comparison", "specific_product", "category_browse", "trending", "deals")
2. Product Category: Likely product category (e.g., "Electronics", "Fashion", "Home", "Books", "Sports")
3. Key Entities: Important words/entities (e.g., brand, price range, features)
4. Modifiers: Any modifiers like "budget", "premium", "eco-friendly", "Indian", etc.
5. Confidence: How confident are you in this classification (0-100)

Return a JSON response with these fields."""

            user_message = f"""Search Query: "{query}"
            
Context: {context if context else 'No context provided'}

Analyze this search query and provide the intent analysis in JSON format."""

            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            response_text = message.content[0].text
            logger.info(f"Intent parsed for query: {query}")
            
            return {
                "success": True,
                "query": query,
                "analysis": response_text,
                "model": CLAUDE_MODEL,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error parsing search intent: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    def generate_product_recommendations(
        self,
        user_interests: List[str],
        budget_range: Optional[tuple] = None,
        history: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized product recommendations using Claude.
        
        Args:
            user_interests: List of user interests (e.g., ["tech", "productivity"])
            budget_range: Tuple of (min, max) budget
            history: List of previously viewed/purchased products
        
        Returns:
            Recommendations dict with categories and reasons
        """
        try:
            system_prompt = """You are a product recommendation expert for FineZ, helping users discover amazing Indian products.
            
Based on user interests, budget, and history, recommend:
1. Top 5 product categories they should explore
2. Specific product types within each category
3. Why these recommendations are relevant
4. Budget-friendly alternatives if applicable
5. Emerging trends in their interest areas

Format as actionable, personalized recommendations."""

            budget_text = f"Budget: ₹{budget_range[0]}-₹{budget_range[1]}" if budget_range else "No budget constraints"
            history_text = f"Previous interests: {', '.join(history)}" if history else "New user"

            user_message = f"""User Profile:
Interests: {', '.join(user_interests)}
{budget_text}
{history_text}

Please provide personalized recommendations."""

            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            response_text = message.content[0].text
            logger.info(f"Recommendations generated for interests: {user_interests}")

            return {
                "success": True,
                "interests": user_interests,
                "recommendations": response_text,
                "model": CLAUDE_MODEL,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "interests": user_interests
            }

    def compare_products(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate detailed product comparison analysis.
        
        Args:
            products: List of product dicts with title, price, features, rating, etc.
        
        Returns:
            Comparison analysis with pros/cons and recommendation
        """
        try:
            system_prompt = """You are a product comparison expert for FineZ.
            
Analyze the provided products and create:
1. Detailed comparison table (specifications, price, value)
2. Pros and cons for each product
3. Best fits for different use cases
4. Value for money analysis
5. Final recommendation with reasoning

Be objective and data-driven."""

            products_text = "\n".join([
                f"Product {i+1}: {p.get('title', 'N/A')}\n" +
                f"  Price: ₹{p.get('price', 'N/A')}\n" +
                f"  Rating: {p.get('rating', 'N/A')}\n" +
                f"  Features: {', '.join(p.get('features', []))}\n"
                for i, p in enumerate(products)
            ])

            user_message = f"""Please compare these products:\n\n{products_text}"""

            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1500,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            response_text = message.content[0].text
            logger.info(f"Comparison generated for {len(products)} products")

            return {
                "success": True,
                "product_count": len(products),
                "comparison": response_text,
                "model": CLAUDE_MODEL,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error comparing products: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "product_count": len(products)
            }

    def generate_product_description(
        self,
        title: str,
        category: str,
        features: List[str],
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Generate engaging product description and marketing copy.
        
        Args:
            title: Product title
            category: Product category
            features: List of product features
            price: Optional price for context
        
        Returns:
            Generated descriptions dict with short and long versions
        """
        try:
            system_prompt = """You are a skilled product copywriter for FineZ, an Indian e-commerce platform.
            
Create engaging, SEO-friendly product descriptions:
1. Short description (50 words) - catchy, highlights USP
2. Long description (200 words) - detailed benefits, use cases
3. Key selling points (5-7 bullet points)
4. Who should buy this product
5. Keywords for SEO

Be specific to Indian market and preferences."""

            price_context = f"\nPrice: ₹{price}" if price else ""
            user_message = f"""Product Title: {title}
Category: {category}
Features: {', '.join(features)}{price_context}

Please generate compelling marketing copy."""

            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            response_text = message.content[0].text
            logger.info(f"Description generated for: {title}")

            return {
                "success": True,
                "title": title,
                "description": response_text,
                "model": CLAUDE_MODEL,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating description: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "title": title
            }

    def answer_product_question(
        self,
        question: str,
        product_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Answer user questions about products using AI.
        
        Args:
            question: User's question
            product_context: Optional context about the product being asked about
        
        Returns:
            Answer dict with response and confidence
        """
        try:
            system_prompt = """You are a knowledgeable customer support agent for FineZ, an Indian product discovery platform.
            
Answer product-related questions thoroughly and helpfully:
1. Provide accurate, helpful information
2. Reference product specifications when relevant
3. Suggest alternatives if the current product might not be ideal
4. Be friendly and conversational in Hinglish (mix of English and Hindi)
5. Ask clarifying questions if needed

Focus on Indian market context and preferences."""

            product_info = f"\nProduct Context: {product_context}" if product_context else ""
            user_message = f"""Customer Question: {question}{product_info}

Please provide a helpful answer."""

            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=800,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            response_text = message.content[0].text
            logger.info(f"Question answered: {question[:50]}...")

            return {
                "success": True,
                "question": question,
                "answer": response_text,
                "model": CLAUDE_MODEL,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "question": question
            }

    def analyze_user_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment and emotion from user text (reviews, feedback, messages).
        
        Args:
            text: Text to analyze
        
        Returns:
            Sentiment analysis dict
        """
        try:
            system_prompt = """You are a sentiment analysis expert for FineZ.
            
Analyze the provided text and determine:
1. Overall sentiment: Positive, Negative, Neutral
2. Confidence score (0-100)
3. Key emotions detected (e.g., happy, frustrated, confused)
4. Main topics/concerns mentioned
5. Actionable insights for the business

Return structured analysis."""

            user_message = f"""Please analyze the sentiment of this text:

"{text}" """

            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            response_text = message.content[0].text
            logger.info(f"Sentiment analyzed for text: {text[:30]}...")

            return {
                "success": True,
                "text_preview": text[:100],
                "analysis": response_text,
                "model": CLAUDE_MODEL,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "text_preview": text[:100]
            }
