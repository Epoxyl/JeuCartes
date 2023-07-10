class InvalidCardException(Exception):
  code = -1

  def __init__(self, description, code):
    self.code = code
    super().__init__(description)
