from pydantic import BaseModel, Field

class GenerateResponseMode(BaseModel):
    apikey :str = Field(..., description="API key for authentication")
    prompt :str = Field(..., description="The prompt to generate a response for")


class GneneratedResponseModel(BaseModel):
    response :str = Field(..., description="The generated response based on the prompt")




