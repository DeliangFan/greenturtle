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

## TODO

- [P0] Validate the high quality data
- [P1] Deal with the data limited to the lasted start date.
- [P0] Get the CSI concat data
- [P0] Benchmark with the CSI concat date
- [P0] Fix e2e test
- [P1] Add pyfolio
- [P1] Refactor, abstract the balance for stock and bond with buy one.


# Issues

some issue with yahoo data

take GC for example, some data in 2000 looks not good
- sometimes the low/high/open/close are the same
- sometimes the low is higher then close while high is lower than open or close.

take the ZR for example
- the price of ZR look abnormal

take the PA for example
- some date's data are missing, for example,  2007 Aug
