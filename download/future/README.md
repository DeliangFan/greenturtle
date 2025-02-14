Download the future data by akshare.

You may refer [futures](https://akshare.akfamily.xyz/data/futures/futures.html#id1) for more details.

I meet some problems when dealing the different future data sources with different format.

To solve this, we need to clear define the data struct for different type of future.

- Download Process
  - Get the original data and save to a local file with original format
  - The directory should be future/source/{cn|us}/...

- Generate single contract files
  - Read the data from source directory and generate the single contract data
  - The directory should be future/contract/{cn|us}/...
  - The data format should be the same in every csv file

- Generate data for backtesting
  - Read the data from single contracts and generate the continuous and adjust contract
  - The directory should be future/backtesting/{cn|us}/...
  - The data format should be the same in every csv file
