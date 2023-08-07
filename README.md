    # Bitcoin Monetary Inflation Calculator
## A small Python module to calculate Bitcoin's monetary inflation using several metrics
This is the fist piece of a bigger project that I’m writing. This module can calculate several metrics of Bitcoin’s monetary inflation using different methods. The calculator can be initiated at any Block Height using InflationCalculator(block_height).

### Functions description:

**set_height(block_height)**: changes the current default block_height value.

**block_stats(block_height, verbose)**: Calculates several stats about the block (defaults to current set Block Height). Calculates the current epoch (halvings since Genesis Block), current Block subsidy, supply at the end of the last epoch, circulating supply and percentage of supply over the total supply. If *verbose=True*, it prints a small human-readable report of the Block stats.

**get_supply(block_height, verbose)**: Returns the circulating supply at the given Block Height (defaults to current set Block Height). If *verbose=True*, it prints a small human-readable report instead.

**inflation(start_height, end_height, inflation_type, periodicity\*, verbose)**: This is the main function of the calculator. If *verbose=False* (default), it returns the calculated inflation. Otherwhise, it prints a small human-readable report. It can calculate four different metrics for monetary inflation, defined by *type*:

1. *type=”real”* (default). Calculates the cumulative Block over Block inflation from Block Height 1 to a given block height.
     
2. *type=”fiat”*. This is the classic methodology for calculating inflation and the one commonly used by central banks and economists. Calculates the inflation over a set of blocks defined by periodicity ("block", "daily", "weekly", "monthly", "yearly" or "epochly").

3. *type="harmonized"*. Calculates the cumulative inflation over a set of blocks. Blocks are aggregated over a period of time defined by periodicity. This method is usefull to compare Bitcoin's monetary inflation to fiat currencies monetary inflation, M1 and/or M2 (e.g. one can easily download US$ money supply on a weekly, calculate the cummulative change and compare it to Bitcoin's harmonized monetary inflation with *periodicity = weekly*). Harmonized inflation calculation can be calculated for a specific length of time by providing a start Block Height (defaults to *starth = 1*).

    Note: Similarly to M1 and M2 calculations, the ending Block Height is set to the nearest integer of the formula *(endh - starth)/periodicity*. In other words, you cannot know the exact monetary supply of a given Friday if data is relased every Wednesday. Instead you'd need to use last Wednesday's monetary supply.

5. *type="snap"*. Calculate the cumulative Block over Block inflation for a set of blocks. If a starting Block Height is provided, inflation is calculated from starth to endh, otherwhise starting Block Height is defined by periodicity.

\*Human defined times are converted to blocks under the assumption that block generation moves at a speed of 1\*10<sup>-1</sup> blocks\*minute<sup>-1</sup>.

    - daily = 144 blocks
    - weekly = 1008 blocks
    - monthly = 4320 blocks
    - yearly =  52560 blocks
    - epochly = 210000 blocks**
\*\* When calculating epochly inflation, starth is set to the beggining of the current epoch and endh is set to the end of the current epoch
