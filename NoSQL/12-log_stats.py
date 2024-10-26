#!/usr/bin/env python3
'''
Script to analyze Nginx logs stored in MongoDB
Displays statistics about HTTP methods and status checks
'''
import os
import argparse
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionError, OperationFailure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def print_nginx_request_logs(nginx_collection):
    '''
    Prints formatted stats about Nginx request logs
    Args:
        nginx_collection: MongoDB collection object containing nginx logs
    '''
    logging.info("Starting Nginx log analysis")

    # 1. Get total number of logs
    total_logs = nginx_collection.count_documents({})
    print(f'{total_logs} logs')

    # 2. Print methods header
    print('Methods:')

    # 3. Count and display each HTTP method
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        count = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {count}')

    # 4. Count status checks (GET requests to /status)
    status_checks = nginx_collection.count_documents({
        'method': 'GET',
        'path': '/status'
    })
    print(f'{status_checks} status check')


def run():
    '''
    Main function to connect to MongoDB and run the analysis
    '''
    # Set up argument parser for command-line options
    parser = argparse.ArgumentParser(description="Analyze Nginx logs stored in MongoDB.")
    parser.add_argument("--db_uri", default="mongodb://127.0.0.1:27017",
                        help="MongoDB URI to connect to. Default is mongodb://127.0.0.1:27017")
    args = parser.parse_args()

    try:
        # Connect to MongoDB with the specified URI
        logging.info(f"Connecting to MongoDB at {args.db_uri}")
        client = MongoClient(args.db_uri)
        nginx_collection = client.logs.nginx

        # Run the log analysis
        print_nginx_request_logs(nginx_collection)

    except ConnectionError:
        logging.error("Failed to connect to MongoDB. Please check the connection.")
    except OperationFailure:
        logging.error("An error occurred while trying to access the MongoDB collection.")
    finally:
        # Clean up client connection
        client.close()
        logging.info("Closed MongoDB connection")


if __name__ == '__main__':
    run()
