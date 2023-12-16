#!/bin/bash

# Display help information when no options are provided
if [ "$1" == "--help" ]; then
    # Help message
    echo "Usage: bash.sh [OPTIONS]"
    echo
    echo "Options:"
    echo "   --help              Display this help message"
    echo "   crawl_listing       Run the crawl listing companies script"
    echo "   crawl_prices        Run the crawl prices script"
    echo "   init_folder         Run the init folder script"
    echo "   train_model         Run the train model script"
    echo "   transform_prices    Run the transform prices script"
    echo "   all                 Run all scripts"
    echo
else
    # Check the provided options using a for loop
    for option in "$@"; do
        # Process the specified option
        # Add additional options handling as needed
        case "$option" in
            crawl_listing)
                python3 ./scripts/run_crawl_listing_companies.py
                ;;
            crawl_prices)
                python3 ./scripts/run_crawl_prices.py
                ;;
            init_folder)
                python3 ./scripts/run_init_folder.py
                ;;
            train_model)
                python3 ./scripts/run_train_model.py
                ;;
            transform_prices)
                python3 ./scripts/run_transform_prices.py
                ;;
            all)
                python3 ./scripts/run_init_folder.py
                python3 ./scripts/run_crawl_listing_companies.py
                python3 ./scripts/run_crawl_prices.py
                python3 ./scripts/run_transform_prices.py
                python3 ./scripts/run_train_model.py
                ;;
            *)
                echo "Invalid argument: $option"
                ;;
        esac
    done
fi
