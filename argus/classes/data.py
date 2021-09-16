import hikari
import datetime

from typing import Any, List, Optional

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

    
    
class Participant:
    def __init__(
        self,
        member: hikari.Member,
        skill: int, # skill is a parameter to represent openskill rank
        session_start: datetime.datetime
    ) -> None:
        self.member=member
        self.id=member.id
        self.debater=False
        self.votes: List[Participant] = []
        self.place = None
        self.against=None
        
        self.skill_pre = skill
        self.skill_post = 0
        self.skill_change = 0
        
        self.session_start: datetime.datetime = session_start
        self.session_end: Optional[datetime.datetime] = None
        self.session_duration: float = 0
            
     def __repr__(
         self
     ) -> Any:
        return (
            f"{self.member.display_name}(elo_post={self.elo_post},"
            f"total_votes={self.total_votes()}, place={self.place}), "
            f"session_duration={self.session_duration}"
        )
    
    def time_spent(
        self
    ) -> Any:
        return self.session_end.totalseconds() - self.session_start.totalseconds()
    
    def update_duration(
        self
    ) -> None:
        self.session_duration+=float(self.time_spent())
        
    def voting_power(
        self
    ) -> float:
        if self.debater:
            return 1 * (1.039582 * (self.session_duration ** 1.579646))
        else:
            return 0.5 * (1.039582 * (self.session_duration ** 1.579646))
        
    def total_votes(
        self
    ) -> float:
        votes: float = 0
        for voter in self.votes:
            if voter.against == self.against:
                votes += voter.voting_power()
            else:
                votes += voter.voting_power() + 1
        return votes
    

    
class DebateMatch:
    def __init__(
        self,
        topic: Any # can be removed (I think), also unsure of type so I didn't type it beyond Any; probably string
    ) -> None:
        self.topic = topic
        self.participants: List[Participant] = []
        
        self.session_start: Optional(datetime.datetime) = None
        self.session_end: Optional(datetime.datetime) = None
            
        self.concluding = False
        self.concluded = False
    
    def add_for(
        self,
        member: Participant
    ) -> None:
        for participant in self.participants:
            if participant.id == member.id:
                member.against = False
                return
        member.against = False
        
        if len(self.participants) == 1:
            self.participants[0].session_start, p.session_start = datetime.datetime.utcnow(), datetime.datetime.utcnow()
    
    def add_against(
        self,
        member: Participant
    ) -> None:
        for participant in self.participants:
            if participant.id == member.id:
                member.against = True
                return
        member.against = True
        
        if len(self.participants) == 1:
            self.participants[0].session_start, p.session_start = datetime.datetime.utcnow(), datetime.datetime.utcnow()
         
    def remove_participant(
        self,
        member: hikari.Member
    ) -> None:
        for m in self.participants:
            if m.id == member.id:
                if not m.debater:
                    self.participants.remove(m)   
    
     def check_participant(
         self,
         member: hikari.Member
     ) -> bool:
        for m in self.participants:
            if m.id == member.id:
                return True
        return False
