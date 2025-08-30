# This program contain functions that will help do miscallenous things such as file checking and etc.


# Checks if the given filename is a valid .gml filename.
def is_gml(filename: str) -> bool:
  if (not filename):
    return False
  if (filename[-4:] != ".gml"):
    return False
  return True
