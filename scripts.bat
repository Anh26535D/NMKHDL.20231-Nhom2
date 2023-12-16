@echo off

setlocal enabledelayedexpansion

rem Display help information when no options are provided
if "%~1"=="" (
    :help
    echo Usage: .\scripts.bat [OPTIONS]
    echo.
    echo Options:
    echo   /?, -h, --help    Display this help message
    echo   crawl_listing     Run the crawl listing companies script
    echo   crawl_prices      Run the crawl prices script
    echo   init_folder       Run the init folder script
    echo   train_model       Run the train model script
    echo   transform_prices  Run the transform prices script
    echo   all               Run all scripts
    echo.
) else (
    rem Check the provided options using a for loop
    for %%i in (%*) do (
        set "option=%%i"
        if /I "!option!"=="/?" (
            goto :help
        ) else if /I "!option!"=="-h" (
            goto :help
        ) else if /I "!option!"=="--help" (
            goto :help
        ) else (
            rem Process the specified option
            rem Add additional options handling as needed
            if "!option!"=="crawl_listing" (
                python .\scripts\run_crawl_listing_companies.py
            ) else if "!option!"=="crawl_prices" (
                python .\scripts\run_crawl_prices.py
            ) else if "!option!"=="init_folder" (
                python .\scripts\run_init_folder.py
            ) else if "!option!"=="train_model" (
                python .\scripts\run_train_model.py
            ) else if "!option!"=="transform_prices" (
                python .\scripts\run_transform_prices.py
            ) else if "!option!"=="all" (
                python .\scripts\run_crawl_listing_companies.py
                python .\scripts\run_crawl_prices.py
                python .\scripts\run_init_folder.py
                python .\scripts\run_train_model.py
                python .\scripts\run_transform_prices.py
            ) else (
                echo Invalid argument: !option!
            )
        )
    )
)

endlocal