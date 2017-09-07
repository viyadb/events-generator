from lib.random import WeightedRandomGenerator

class Device(object):
  def __init__(self, name, vendor_gen):
    self.name = name
    self.vendor_gen = vendor_gen

  def vendor(self):
    return self.vendor_gen()

class Android(Device):
  def __init__(self):
    super(Android, self).__init__("Android", WeightedRandomGenerator(
      ["Samsung",	"Huawei", "OPPO", "vivo", "LG", "HP", "Acer"],
      [23.3, 10, 7.5, 5.5, 3, 1.5, 1.4]
    ))

class Apple(Device):
  def __init__(self):
    super(Apple, self).__init__("iOS", lambda: "Apple")

class Windows(Device):
  def __init__(self):
    super(Windows, self).__init__("Windows Phone", WeightedRandomGenerator(
      ["Microsoft", "Nokia", "HP", "Acer", "Vaio"],
      [50, 30, 5, 4, 1]
    ))

class Blackberry(Device):
  def __init__(self):
    super(Blackberry, self).__init__("Blackberry", lambda: "Blackberry")

random_device = WeightedRandomGenerator(
  [Android(), Apple(), Windows(), Blackberry()],
  [85, 14.7, 0.1, 0.1]
)

