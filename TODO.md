# Features & Bugs

## Done

- [P0][Done] Add analysis about the leverage.
- [P0][Done] Add analysis about position profit.
- [P0][Done] Support short size
- [P0][Done] Simulate with true size
- [P0][Done] Refactor, add experiment
- [P0][Done] Refactor, move constant out of util
- [P0][Done] Refactor, move analysis result to summary
- [P0][Done] Refactor, abstract the module for data
- [P0][Done] Refactor, refine the correlation for stock
- [P0][Done] Refactor, provide the correlation capability for future
- [P0][Done] Refactor, add e2e test
- [P2][Done] Refactor, process the data directory
- [P0][Done] add buy and hold strategy
- [P0][Done] add more test for stock like strategy
- [P0][Done] add more test for future like strategy
- [P0][Done] Dealing with future data, currently i use the main contract, what's the problem.
- [P0][Done] Simulate the margin trading.
- [P0][Done] Portfolio management for single symbol
- [P1][Done] Risk management
- [P0][Done] Add stop lost
- [P0][Done] Abstract the progress for generating order. Need take the already hold position into consideration
- [P0][Done] Portfolio management across different sectors
- [P0][Done] Figure out why adjust data fails for BTC/ETH/RB/ZB/ZN/ZT
- [P0][Done] Better high quality data
- [P0][Done] Generate the concat file from quality data
- [P0][Done] Benchmark with the generated concat data file
- [P0][Done] Validate the high quality data
- [P0][Done] Get the CSI concat data
- [P0][Done] Benchmark with the CSI concat date
- [P0][Done] refactor the download module
- [P0][Done] refactor the generate contract module 
- [P0][Done] refactor the const module
- [P0][Done] refactor the continuous and adjusted generation module 
- [P1][Done] Deal with the data limited to the lasted start date.
- [P0][Done] Get the china future data
- [P0][Done] Do some benchmark for china future data
- [P0][Done] fetch the failed china data and test again
- [P0][Done] better understand about the cn commission
- [P1][Done] Add unittest for validation and simulator
- [P0][Done] Fix e2e test
- [P0][Done] [MySQL] Introduce mysql
- [P0][Done] [MySQL] Define the tables for contract, continues contract
- [P0][Done] [MySQL] Syncer the delta data to mysql
- [P0][Done] [Varieties] filter delta data according to variety constant
- [P1][Done] Data exchange plugin for csv, db, datafeed etc
- [P0][Done] [MySQL] Choose the main contract and adaptor
- [P0][Done] [MySQL] Add expire data, and expire should not be non
- [P0][Done] [MySQL] Better validation and padding
- [P0][Done] [MySQL] Delta continuous contract support
- [P0][Done] [Serving] Attention for download the online data, test after close
- [P0][Done] Focus on CTA, remove stock part
- [P0][Done] Refactor, default backtrader to control complexity, including: strategy, indicators, simulator and analyzers
- [P0][Done] Refactor, default future to control complexity, constant and simulator
- [P0][Done] Refactor, better datafeed directory
- [P0][Done] [Serving] datafeed adaptor mysql for continuous contract 
- [P0][Done] [Serving] continuous contract adjust price
- [P0][Done] [Data] DCE download failed before close, just raise exception and block the following progress; 
- [P0][Done] [Data] Check the validation works or not, and it work for the delta contracts
- [P0][Done] [Data] support for trading calender
- [P0][Done] [Serving] contract alignment.
- [P0][Done] [Data] Add logger when padding
- [P0][Done] [Data] Add logger when skip invalid data
- [P0][Done] [Data] Validate the diff price between the days
- [P0][Done] [Backtesting] figure out the bump and spider total values
- [P0][Done] [Refactor] Rename simulator to backtesting
- [P0][Done] [Serving] Trading strategy for backtest and server
- [P0][Done] [Serving] Portfolio management strategy for backtest and server
- [P1][Done] [Data] add insert number for delta data
- [P0][Done] [Serving] Abstract for broker
- [P0][Done] [Serving] Adapter to the trading API with get account/position/orders
- [P0][Done] [Meta] Symbol and varieties mapping in position
- [P0][Done] [Serving] Mapping varieties to symbol during buy and sell
- [P0][Done] [Serving] Support buy and sell
- [P0][Done] [Serving] Care about the limit price
- [P0][Done] [Serving] Notification message for transaction
- [P1][Done] [Config] Refactor the config file
- [P1][Done] [Notifier] Refine order information with more details
- [P0][Done] [Test] make sure the strategy parameters works as expected
- [P1][Done] [Data] check before download to save time
- [P0][Done] [Serving] Contract rolling
- [P0][Done] [Serving] Add warning information like margin ratio and rolling
- [P0][Done] [Serving] Trading validation including margin ratio
- [P1][Done] [Serving] Deployment
- [P1][Done] [Doc] Add more documents, design document and strategy document
- [P1][Done] [Backtesting] Analysis the profit and losing
- [P1][Done] [Portfolio] Need to check the bugs in portfolio
- [P1][Done] [Unittest] Add more unittest(data, strategy, simulator)

## TODO

- [P2] Evaluate the CTA factors
- [P2] [Serving] Add support for multi account, support for both CN and US.
- [P2] [Serving] Persistence logs
- [P2] [Serving] Decoupling the executing order
- [P2] Add pyfolio

# Issues

some issue with yahoo data

take GC for example, some data in 2000 looks not good
- sometimes the low/high/open/close are the same
- sometimes the low is higher then close while high is lower than open or close.

take the ZR for example
- the price of ZR look abnormal

take the PA for example
- some date's data are missing, for example,  2007 Aug
