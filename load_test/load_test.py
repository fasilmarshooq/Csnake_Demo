#!/usr/bin/env python3
"""
Load test script for CsnakeDemo API using Locust.
Tests the /chromadb/add and /chromadb/search endpoints with focus on search performance.
"""

import random
import time
from locust import HttpUser, task, between, events
from locust.exception import StopUser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaDBUser(HttpUser):
    """Locust user class for testing ChromaDB API endpoints.
    
    Note: The 'self.client' is automatically created by Locust's HttpUser class.
    It's a requests.Session object that handles HTTP requests to the specified host.
    The host is specified when running locust with --host=http://localhost:5115
    """
    
    # Wait between 1-3 seconds between tasks
    wait_time = between(1, 3)
    
    # Test data - 10 strings to add to the database
    test_strings = [
        "Machine learning is a subset of artificial intelligence",
        "Python is a popular programming language for data science",
        "ChromaDB is a vector database for embeddings",
        "Natural language processing uses machine learning techniques",
        "Vector embeddings represent text as numerical arrays",
        "Semantic search finds documents by meaning not keywords",
        "Large language models can generate human-like text",
        "Deep learning uses neural networks with multiple layers",
        "Text preprocessing is important for NLP applications",
        "Information retrieval systems help find relevant documents"
    ]
    
    # Search queries related to the test strings
    search_queries = [
        "artificial intelligence machine learning",
        "programming language data science",
        "vector database embeddings",
        "natural language processing",
        "numerical arrays text representation",
        "semantic search meaning",
        "language models text generation",
        "neural networks deep learning",
        "text preprocessing NLP",
        "information retrieval documents"
    ]
    
    def on_start(self):
        """Called when a user starts. Add test data to the database."""
        logger.info(f"User starting - adding test data")
        self.add_test_data()
    
    def add_test_data(self):
        """Add the 10 test strings to the database."""
        for i, text in enumerate(self.test_strings):
            try:
                response = self.client.post(
                    "/chromadb/add",
                    params={"text": text},
                    name="add_text"
                )
                if response.status_code == 200:
                    logger.info(f"Successfully added string {i+1}/10")
                else:
                    logger.error(f"Failed to add string {i+1}: {response.status_code}")
            except Exception as e:
                logger.error(f"Exception adding string {i+1}: {str(e)}")
    
    @task(10)  # Weight: 10 (high priority for search operations)
    def search_text(self):
        """Search for text in the database - primary test operation."""
        query = random.choice(self.search_queries)
        
        start_time = time.time()
        try:
            response = self.client.post(
                "/chromadb/search",
                params={"query": query},
                name="search_text"
            )
            
            # Calculate latency
            latency = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                # Log successful search
                logger.info(f"Search successful for query: '{query}' (latency: {latency:.2f}ms)")
                
                # Record custom metrics
                self.environment.events.request.fire(
                    request_type="POST",
                    name="search_text_success",
                    response_time=latency,
                    response_length=len(response.content),
                    context={"query": query}
                )
            else:
                logger.error(f"Search failed for query: '{query}' - Status: {response.status_code}")
                
                # Record failure metrics
                self.environment.events.request.fire(
                    request_type="POST",
                    name="search_text_failure",
                    response_time=latency,
                    response_length=0,
                    exception=f"HTTP {response.status_code}",
                    context={"query": query}
                )
                
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            logger.error(f"Exception during search for query '{query}': {str(e)}")
            
            # Record exception metrics
            self.environment.events.request.fire(
                request_type="POST",
                name="search_text_exception",
                response_time=latency,
                response_length=0,
                exception=str(e),
                context={"query": query}
            )
    
    @task(1)  # Weight: 1 (lower priority - occasional add operations)
    def add_additional_text(self):
        """Occasionally add additional text to the database."""
        additional_texts = [
            "API testing with Locust load testing framework",
            "Performance metrics include latency and throughput",
            "Load testing helps identify system bottlenecks",
            "Scalability testing ensures system can handle growth"
        ]
        
        text = random.choice(additional_texts)
        try:
            response = self.client.post(
                "/chromadb/add",
                params={"text": text},
                name="add_additional_text"
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully added additional text: '{text[:50]}...'")
            else:
                logger.error(f"Failed to add additional text: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Exception adding additional text: {str(e)}")

# Custom event handlers for detailed metrics
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception=None, context=None, **kwargs):
    """Custom request handler for detailed logging and metrics."""
    if exception:
        logger.error(f"Request failed: {name} - {exception}")
    else:
        logger.debug(f"Request successful: {name} - {response_time:.2f}ms")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when the test starts."""
    logger.info("Starting ChromaDB load test...")
    logger.info(f"Target host: {environment.host}")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when the test stops."""
    logger.info("ChromaDB load test completed")

# Configuration for different test scenarios
class QuickTest(ChromaDBUser):
    """Quick test with fewer users and shorter duration."""
    wait_time = between(0.5, 1.5)

class StressTest(ChromaDBUser):
    """Stress test with more aggressive timing."""
    wait_time = between(0.1, 0.5)

class EnduranceTest(ChromaDBUser):
    """Endurance test with longer waits between requests."""
    wait_time = between(5, 10)
