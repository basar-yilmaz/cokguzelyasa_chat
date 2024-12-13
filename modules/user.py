from typing import List, Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    """User data model."""

    user_id: Optional[int] = Field(description="User ID.")
    name: str = Field(description="Name of the user.")
    # date_of_birth: Optional[str] = Field(description="Date of birth of the user.")
    chronic_illnesses: str = Field(description="List of chronic illnesses.")
    allergies: str = Field(description="List of allergies.")
    current_medications: str = Field(description="List of current medications.")
    analysis_result: Optional[str] = Field(description="Analysis result.")

    @classmethod
    def mock(cls):
        return cls(
            name="Başar YILMAZ",
            date_of_birth="1990-01-01",
            chronic_illnesses=["Hypertension", "Diabetes"],
            allergies=["Peanuts", "Penicillin"],
            current_medications=["Lisinopril", "Metformin", "Ritalin"],
            analysis_result="""
                The hair thinning on the top and hairline recession suggest an early stage of hair loss. Based on the Norwood scale, this appears to be between Norwood 2 to 3 (mild to moderate thinning/recession). The crown area seems relatively stable, with minor thinning.            
            """,
        )

    def __str__(self):
        return f"User(name={self.name}, chronic_illnesses={self.chronic_illnesses}, allergies={self.allergies}, current_medications={self.current_medications}, analysis_result={self.analysis_result})"