from curr import Currency
import numpy as np

class Trigger(object):

  def __init__(self, func, prop, threshold, date_start_idx,
                date_end_idx, date_start_str,  date_end_str):

    self.func = func
    self.prop = prop

    self.date_start_str = date_start_str
    self.date_end_str = date_end_str

    self.date_start_idx = date_start_idx
    self.date_end_idx = date_end_idx
    
    self.threshold = threshold

  def calc_value(self, curr):

    # TODO


    return value

  def evaluate(self, value):
    """
    Returns True if an alert should be generated
    for the given news item, or False otherwise.
    """
    # DO NOT CHANGE THIS!
    raise NotImplementedError

  def __repr__(self):

    return f'{self.func}, {self.prop}, {self.threshold}) in between ({self.date_start_str} - {self.date_end_str}'


class HighTrigger(Trigger):
  def __init__(self, func, prop, threshold, date_start_idx,
                date_end_idx, date_start_str,  date_end_str):
    super().__init__(func, prop, threshold, date_start_idx,
              date_end_idx, date_start_str,  date_end_str)

  def evaluate(self, curr):
    
    if self.func == "CHG":
        #CHANGE
        self.funcValue = curr.calc_change(self.date_start_idx, self.date_end_idx, self.prop)
    elif self.func == "MEAN":
        #mean
        self.funcValue = curr.calc_mean(self.date_start_idx, self.date_end_idx, self.prop)
    elif self.func == "VOL":
        #vol
        self.funcValue = curr.calc_volatility(self.date_start_idx, self.date_end_idx, self.prop)
    elif self.func == "MAX":
        #max
        self.funcValue = curr.calc_mean(self.date_start_idx, self.date_end_idx, self.prop)
    elif self.func == "MIN":
        #min
        self.funcValue = curr.calc_min(self.date_start_idx, self.date_end_idx, self.prop)
    
    # TODO

    if self.funcValue > self.threshold:
        return True
    else:
        return False
      
  def __repr__(self):
    """
    :return: Printable representation of the object.
    """

    return f'HighTrigger({super().__repr__()})'

class LowTrigger(Trigger):

  def __init__(self, func, prop, threshold, date_start_idx,
                date_end_idx, date_start_str,  date_end_str):
    super().__init__(func, prop, threshold, date_start_idx,
              date_end_idx, date_start_str,  date_end_str)

  def evaluate(self, curr):
    if self.func == "CHG":
        #CHANGE
        self.funcValue = curr.calc_change(self.date_start_idx, self.date_end_idx, self.prop)
    elif self.func == "MEAN":
        #mean
        self.funcValue = curr.calc_mean(self.date_start_idx, self.date_end_idx, self.prop)
    elif self.func == "VOL":
        #vol
        self.funcValue = curr.calc_volatility(self.date_start_idx, self.date_end_idx, self.prop)
    elif self.func == "MAX":
        #max
        self.funcValue = curr.calc_max(self.date_start_idx, self.date_end_idx, self.prop)
    elif self.func == "MIN":
        #min
        self.funcValue = curr.calc_min(self.date_start_idx, self.date_end_idx, self.prop)
    
    # TODO

    if self.funcValue < self.threshold:
        return True
    else:
        return False

  def __repr__(self):
    """
    :return: Printable representation of the object.
    """

    return f'LowTrigger({super().__repr__()})'

class NotTrigger(Trigger):

  def __init__(self, trigger):
    self.trigger = trigger

  def evaluate(self, curr):
    
    # TODO
    if self.trigger.evaluate(curr):
        return False
    else:
        return True

  def __repr__(self):
    """
    :return: Printable representation of the object.
    """
    return f'NotTrigger({self.trigger})'

class AndTrigger(Trigger):
  def __init__(self, trigger1, trigger2):
    self.trigger1 = trigger1
    self.trigger2 = trigger2

  def evaluate(self, curr):

    if self.trigger1.evaluate(curr) and self.trigger2.evaluate(curr):
        return True
    else:
        return False

  def __repr__(self):
    """
    :return: Printable representation of the object.
    """
    return f'AndTrigger({self.trigger1}, {self.trigger2})'

class OrTrigger(Trigger):
  def __init__(self, trigger1, trigger2):

    self.trigger1 = trigger1
    self.trigger2 = trigger2

  def evaluate(self, curr):

    # TODO
    if self.trigger1.evaluate(curr) or self.trigger2.evaluate(curr):
        return True
    else:
        return False

  def __repr__(self):
    """
    :return: Printable representation of the object.
    """
    return f'OrTrigger({self.trigger1}, {self.trigger2})'

  
if __name__ == "__main__":

  # DON'T MODIFY THIS!
  total_days = 30
  c = Currency("EUR", 30)
  np.random.seed(42)
  c.BUY = 5.0 * np.ones(total_days) + np.random.rand(total_days)
  c.SELL = c.BUY + 0.1

  t1 = LowTrigger('MIN', 'SELL', 5.1, 2, 5, "",  "")
  t2 = HighTrigger('VOL', 'BUY', 0.01, 0, 7, "",  "")
  t3 = HighTrigger('MEAN', 'BUY', 5.0, 2, 5, "",  "")
  t4 = NotTrigger(t1)
  t5 = OrTrigger(t1,t2)
  t6 = AndTrigger(t4,t3)
  t7 = AndTrigger(t1,t3)
  t8 = NotTrigger(t4)
  t9 = LowTrigger('CHG', 'BUY', 1.2, 2, 5, "",  "")
  t10 = HighTrigger('MEAN', 'BUY', 5.0, 2, 5, "",  "")

  print("t1 - ", t1.evaluate(c))
  print("t2 - ", t2.evaluate(c))
  print("t3 - ", t3.evaluate(c))
  print("t4 - ", t4.evaluate(c))
  print("t5 - ", t5.evaluate(c))
  print("t6 - ", t6.evaluate(c))
  print("t7 - ", t7.evaluate(c))
  print("t8 - ", t8.evaluate(c))
  print("t9 - ", t9.evaluate(c))
  print("t10 - ", t10.evaluate(c))
