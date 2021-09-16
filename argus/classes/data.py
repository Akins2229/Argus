import hikari
from typing import Any

class Topic:
  def __init__(
    self,
    member: hikari.Member,
    message: hikari.Message
  ) -> None:
    self.author=member
    self.message=message.content
    self.voters = [
      self.author
    ]
    self.prioritized=False
    self.create_at=message.created_at
    
  def __repr__(
    self
  ) -> Any:
    if self.prioritized:
      return (
                f'Topic(author="{self.author}", '
                f'votes="{self.votes}", '
                f'prioritized="{self.prioritized}", '
                f'message="{self.message}")'
             )
    else:
      return (
                f'Topic(author="{self.author}", '
                f'votes="{self.votes}", message="{self.message}")'
             )
    
  def __str__(
    self
  ) -> str:
    if self.message.strip() == "":
      return ""
    else:
      return self.message
    
    
  #decoraters
  
  def not_yet_voted(
    func
  ) -> Any:
    def wrapper(*args, **kwargs) -> bool:
      if args[0] in self.voters:
        func(*args, **kwargs)
        return True
      else:
        return False
    return wrapper
    
  def already_voted(
    func
  ) -> Any:
    def wrapper(*args, **Kwargs) -> bool:
      if args[0] in self.voters:
        func(*args, **kwargs)
        return True
      else:
        return False
    return wrapper
    
  @property
  def votes(
    self
  ) -> int:
    if self.prioritized:
      return len(self.voters)+1
    else:
      return len(self.voters)
  
  @not_yet_voted
  def add_voter(
    self,
    member: hikari.Member
  ) -> None:
    self.voters.append(member)
    
  @already_voted
  def remove_voter(
    self,
    member: hikari.Member
  ) -> None:
    self.voters.remove(member)
