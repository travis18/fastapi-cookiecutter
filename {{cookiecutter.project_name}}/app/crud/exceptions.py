#  Custom CRUD related exceptions

from os import stat
from typing import List


class CRUDBaseException(Exception):
  """ Base CRUD Exception class """
  def __init__(self, name:str, title:str=None, message:str=None, detail:str=None, status_code:int=500):
    self.name = name
    self.title = title
    self.detail = detail
    self.status_code = status_code
    if message is None:
      self.message = f"Something went wrong on {name}"

  def json_response(self)-> dict:
    return {
      "title":self.title,
      "message":self.message,
      "detail":self.detail
    }

class CRUDDataExistError(CRUDBaseException):
  """ Should be raised when data existing checking is True """
  def __init__(self, name: str, repeatedAttrs:List[dict], title:str=None, message:str=None, detail:str=None):
    """ 
    repeatedAttrs is a List of dicts like:{ 
        "name": str,
        "value": Any
      }
    ]
    """
    if title is None:
      title = "Data Already Exists Error"
    super().__init__(name=name, title=title, message=message, detail=detail,status_code=409)
    self.repeatedAttrs = repeatedAttrs
    strAttrs = ""
    for attr in repeatedAttrs:
      strAttrs += f"{attr['name']}:{attr['value']} "
    self.message = f"The data already exists with key attribute(s):{strAttrs}"

class CRUDDataNotExistError(CRUDBaseException):
  """ Should be raised when data existing checking is False """
  def __init__(self, name: str, attrs:List[dict], title:str=None, message:str=None, detail:str=None):
    """ 
    attrs is a List of dicts for checking if the data didn't exist, and it's like:
    
    [
      { 
        "name": str,
        "value": Any
      }
    ]
    """
    if title is None:
      title = "Data Not Exists Error"
    super().__init__(name,title=title, message=message, detail=detail, status_code=404)
    self.attrs = attrs
    strAttrs = ""
    for attr in attrs:
      strAttrs += f"{attr['name']}:{attr['value']} "
    self.message = f"The data not exist with key attribute(s):{strAttrs}"
    
class CRUDDataCheckError(CRUDBaseException):
  """ Will raise when data check error in crud classes """
  def __init__(self, name:str, title:str=None, message:str=None, detail:str=None):
    if title is None:
      title="Data Check Error"
    super().__init__(name=name, title=title, message=message, detail=detail, status_code=400)
    