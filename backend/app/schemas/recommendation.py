from datetime import datetime
from pydantic import BaseModel
class RecommendationResponse(BaseModel):
    id:int; patient_id:int; category:str; title:str; description:str; priority:str; created_at:datetime
    model_config={"from_attributes":True}
