#!/bin/bash

# Display help information when no options are provided
if [ "$1" == "--help" ]; then
    # Help message
    echo "Usage: ./scripts.sh [OPTIONS]"
    echo
    echo "Options:"
    echo "  --help              Display this help message"
    echo "  crawl_listing       Run the crawl listing companies script"
    echo "  crawl_prices        Run the crawl prices script"
    echo "  init_folder         Run the init folder script"
    echo "  train_model         Run the train model script"
    echo "  transform_prices    Run the transform prices script"
    echo "  all                 Run all scripts"
    echo
else
    # Check the provided options using a for loop
    for option in "$@"; do
        # Process the specified option
        # Add additional options handling as needed
        if [ "$option" == "crawl_listing" ]; then
            python ./scripts/run_crawl_listing_companies.py
        elif [ "$option" == "crawl_prices" ]; then
            python ./scripts/run_crawl_prices.py
        elif [ "$option" == "init_folder" ]; then
            python ./scripts/run_init_folder.py
        elif [ "$option" == "train_model" ]; then
            python ./scripts/run_train_model.py
        elif [ "$option" == "transform_prices" ]; then
            python ./scripts/run_transform_prices.py
        elif [ "$option" == "all" ]; then
            python ./scripts/run_crawl_listing_companies.py
            python ./scripts/run_crawl_prices.py
            python ./scripts/run_init_folder.py
            python ./scripts/run_train_model.py
            python ./scripts/run_transform_prices.py
        else
            echo "Invalid argument: $option"
        fi
    done
fi
