import btcinflation

test = btcinflation.InflationCalculator(209000)
test.block_stats(verbose=True)
test.inflation(starth = 10000, 
               endh = 480000,
               verbose = True,
               type = "harmonized",
               periodicity = "epochly")
test.inflation(verbose = True,
               type = "fiat",
               periodicity = "daily")
test.inflation(type = "real",
               verbose=True)
test.inflation(starth = 10000,
               verbose = True,
               type = "snap",
               periodicity = "monthly")
test.block_stats(block_height=210000)
test.set_height(210000)
test.get_supply(verbose=True)
