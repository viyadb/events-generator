from lib.random import WeightedRandomGenerator

class Device(object):
  def __init__(self, name, vendor_gen):
    self.name = name
    self.vendor_gen = vendor_gen

  def vendor(self):
    return self.vendor_gen()

class Android(Device):
  def __init__(self):
    super(Android, self).__init__(u"Android", WeightedRandomGenerator(
      [u"Samsung",	u"Huawei", u"OPPO", u"vivo", u"LG", u"HP", u"Acer"],
      [23.3, 10, 7.5, 5.5, 3, 1.5, 1.4]
    ))

class Apple(Device):
  def __init__(self):
    super(Apple, self).__init__(u"iOS", lambda: u"Apple")

class Windows(Device):
  def __init__(self):
    super(Windows, self).__init__(u"Windows Phone", WeightedRandomGenerator(
      [u"Microsoft", u"Nokia", u"HP", u"Acer", u"Vaio"],
      [50, 30, 5, 4, 1]
    ))

class Blackberry(Device):
  def __init__(self):
    super(Blackberry, self).__init__(u"Blackberry", lambda: u"Blackberry")

random_device = WeightedRandomGenerator(
  [Android(), Apple(), Windows(), Blackberry()],
  [85, 14.7, 0.1, 0.1]
)

