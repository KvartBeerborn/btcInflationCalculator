#Bitcoin monetary inflation calculator

import numpy as np


class InflationCalculator:

  def __init__(self, block_height):

    self.block_height = np.int64(block_height)
    self.current_epoch = np.int8(0)
    self.current_subsidy = np.int8(0)
    self.past_epoch_supply = np.int8(0)
    self.circulating_supply = np.int8(0)
    initial_message = print("Calculator initiated at Block Height: " +
                            str(self.block_height))

    return initial_message

  def set_height(self, block_height):

    self.block_height = np.int64(block_height)
    set_message = print("Block Height set to: " + str(self.block_height))
    return set_message

  def block_stats(self, **kwargs):
    block_height = kwargs.get("block_height", None) 
    verbose = kwargs.get("verbose", False)
    
    if block_height is None:
      block_height = self.block_height
    self.current_epoch = np.int8(block_height / 210000)
    self.current_subsidy = np.int64(
      (50 * (50 / (50 * (2**self.current_epoch)))) * 100000000)
    self.past_epoch_supply = sum(
      210000 * np.uint64(5000000000 * (5000000000 / (5000000000 * (2**i))))
      for i in range(0, self.current_epoch))
    self.circulating_supply = np.int64(self.past_epoch_supply + (
      (block_height - (210000 * self.current_epoch)) * self.current_subsidy))
    self.supply_percentage = np.int16(
      (self.circulating_supply * 100) / 2100000000000000)
    if verbose:
      return print("Block Height: " + str(block_height) +
                       "\nCirculating supply: " +
                       str(self.circulating_supply) +
                       " Satoshis\nPercentage of the total supply: " +
                       str(self.supply_percentage) + "%\nCurrent Subsidy: " +
                       str(self.current_subsidy) +
                       " Satoshis\nHalvings since Genesis Block: " +
                       str(self.current_epoch))
    return

  def get_supply(self, **kwargs):
    block_height = kwargs.get("block_height", None) 
    verbose = kwargs.get("verbose", False)

    if block_height is None:
      block_height = self.block_height
    self.block_stats(block_height=block_height)
    if verbose:
      return print("Block height: " + str(block_height) +
                           "\nCirculating supply: " +
                           str(self.circulating_supply) + 
                           " Satoshis\nPercentage of the total supply: " +
                           str(self.supply_percentage) + "%")
    return self.circulating_supply

  def inflation(self, **kwargs):
    start_height = kwargs.get("starth", None)
    end_height = kwargs.get("endh", None)
    inflation_type = kwargs.get("type", "real")
    periodicity = kwargs.get("periodicity", "block")
    verbose = kwargs.get("verbose", False)

    self.supply = np.int8(0)
    self.inflat = np.int8(0)
    if end_height is None:
      self.end_height = self.block_height
    else:
      self.end_height = end_height

    if start_height is None:
      self.start_height = 1
    else:
      self.start_height = start_height

    if periodicity == "block" and self.end_height <= 1:
      raise ValueError(
        "No Bitcoin was mined on Genesis Block, " +
        "therefore Block over Block inflation cannot " +
        "be calculated for Genesis Block or Block 1."
      )
    if periodicity == "block" and self.end_height - self.start_height < 1:
      raise ValueError(
        "Imposible to calculate inflation on a " +
        "block basis. Start and end Blocks " +
        "must be at least 1 Block appart."
      )
    elif periodicity == "daily" and self.end_height <= 144:
      raise ValueError(
        "Insuficient data points. "+
        "The minimum Block Height to calculate inflation " +
        "on a daily basis is Block Height 145."
      )
    elif periodicity == "daily" and self.end_height - self.start_height < 144:
      raise ValueError(
        "Imposible to calculate inflation on a " +
        "daily basis. Start and end Blocks must be " +
        "at least 144 Blocks appart."
      )
    elif periodicity == "weekly" and self.end_height <= 1008:
      raise ValueError(
        "Insuficient data points. " +
        "The minimum Block Height to calculate inflation on a " +
        "weekly basis is Block Height 1009."
      )
    elif periodicity == "weekly" and self.end_height - self.start_height < 1008:
      raise ValueError(
        "Imposible to calculate inflation on a " +
        "weekly basis. Start and end Blocks must be " +
        "at least 1008 Blocks appart."
      )
    elif periodicity == "monthly" and self.end_height <= 4320:
      raise ValueError(
        "Insuficient data points. " +
        "The minimum Block Height to calculate inflation on a " + 
        "monthly basis is Block Height 4321."
      )
    elif periodicity == "monthly" and self.end_height - self.start_height < 4320:
      raise ValueError(
        "Imposible to calculate inflation on a " +
        "monthly basis. Start and end Blocks must be " +
        "at least 4320 Blocks appart."
      )
    elif periodicity == "yearly" and self.end_height <= 52560:
      raise ValueError(
        "Insuficient data points. " +
        "The minimum Block Height to calculate inflation on a " +
        "yearly basis is Block Height 52561."
      )
    elif periodicity == "yearly" and self.end_height - self.start_height < 52560:
      raise ValueError(
        "Imposible to calculate inflation on a " +
        "yearly basis. Start and end Blocks must be " +
        "at least 52560 Blocks appart."
      )
    elif periodicity == "epochly" and self.end_height <= 210000:
      raise ValueError(
        "Insuficient data points. " +
        "The minimum Block Height to calculate inflation on " + 
        "an epochly basis is Block Height 210001."
      )
    elif periodicity == "epochly" and self.end_height - self.start_height < 210000:
      raise ValueError(
        "Imposible to calculate inflation on a " +
        "epochly basis. Start and end Blocks must be " + 
        "at least 210000 Blocks appart."
      )

    steps = {
      "block": 1,
      "daily": 144,
      "weekly": 1008,
      "monthly": 4320,
      "yearly": 52560,
      "epochly": 210000
    }

    def real_inflation():
      self.start_height = 1
      for i in range(self.start_height, self.end_height + 1,
                     steps[periodicity]):
        height = i
        self.block_stats(block_height = height)
        if self.supply == 0:
          self.supply = self.circulating_supply
        else:
          self.inflat += np.float64((self.current_subsidy * 100) / self.supply)
          self.supply = self.circulating_supply
      return self.inflat

    def fiat_inflation():
      self.start_height = self.end_height - steps[periodicity]
      if periodicity == "epochly":
        current_epoch_supply = np.int64(self.past_epoch_supply +
                                        (210000 * self.current_subsidy))
        self.inflat = np.float64(
          ((current_epoch_supply - self.past_epoch_supply) * 100) /
          self.past_epoch_supply)
      else:
        for i in range(self.start_height, self.end_height + 1,
                       steps[periodicity]):
          height = i
          self.block_stats(block_height = height)
          if self.supply == 0:
            self.supply = self.circulating_supply
          else:
            self.inflat += np.float64(
              ((self.circulating_supply - self.supply) * 100) / self.supply)
      return self.inflat

    def harmonized_inflation():
      if periodicity == "epochly":
        self.block_stats(block_height = self.end_height)
        self.end_height = (self.current_epoch + 1) * 210000
        self.supply = self.past_epoch_supply
        for i in range(self.start_height, self.end_height + 1,
                       steps[periodicity]):
          height = i
          self.block_stats(block_height = height)
          self.inflat += np.float64(
            ((self.circulating_supply - self.supply) * 100) / self.supply)
          self.supply = self.circulating_supply
      else:
        for i in range(self.start_height, self.end_height + 1,
                       steps[periodicity]):
          height = i
          self.block_stats(block_height = height)
          if self.supply == 0:
            self.supply = self.circulating_supply
          else:
            self.inflat += np.float64(
              ((self.circulating_supply - self.supply) * 100) / self.supply)
            self.supply = self.circulating_supply
      return self.inflat

    def snap_inflation():
      if periodicity == "epochly":
        self.block_stats(block_height = self.end_height)
        self.start_height = self.current_epoch * 210000
        self.end_height = (self.current_epoch + 1) * 210000
      else:
        if start_height is None:
          self.start_height = self.end_height - steps[periodicity]
      for i in range(self.start_height, self.end_height + 1, 1):
        height = i
        self.block_stats(block_height = height)
        if self.supply == 0:
          if periodicity == "epochly":
            self.supply = self.past_epoch_supply
            self.inflat += np.float64(
              (self.current_subsidy * 100) / self.supply)
          else:
            self.supply = self.circulating_supply
        else:
          self.inflat += np.float64((self.current_subsidy * 100) / self.supply)
          self.supply = self.circulating_supply
      return self.inflat

    if inflation_type == "real":
      real_inflation()
    elif inflation_type == "fiat":
      fiat_inflation()
    elif inflation_type == "harmonized":
      harmonized_inflation()
    elif inflation_type == "snap":
      snap_inflation()

    if verbose:
      return print(
        str(inflation_type).capitalize() + " inflation from Block height " +
        str(self.start_height) + " to Block height " + str(self.end_height) +
        " measured on a " + str(periodicity) + " basis: " + str(self.inflat) +
        "%")
    else:
      return self.inflat
