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

## TODO

- [P0] add more test for crypto like strategy
- [P0] Dealing with future data, currently i use the main contract, what's the problem.
- [P0] Portfolio management for single symbol
- [P0] Portfolio management across different sectors
- [P0] Simulate the margin trading.
- [P0] Refactor, abstract the balance for stock and bond with buy one.
- [P1] Risk management
- [P2] Deal with the data limited to the lasted start date.


# Issues

some issue with yahoo data

take GC for example, some data in 2000 looks not good
- sometimes the low/high/open/close are the same
- sometimes the low is higher then close while high is lower than open or close.

take the ZR for example
- the price of ZR look abnormal
