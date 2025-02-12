from pydantic import BaseModel, Field

class VerifyLLMResponseModel(BaseModel):
    isValid: bool = Field(..., description="Whether the response is valid and consistent with the query")
    reason: str = Field(..., description="Explanation for why the response is valid or not")