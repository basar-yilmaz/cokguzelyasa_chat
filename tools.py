# import datetime
from typing import Optional, Literal
from langchain_core.tools import tool

from modules.user import User
from pymongo import MongoClient


def process_user() -> User:
    """Process user data."""
    user = User.mock()
    return user


def fetch_user_data() -> User:
    """Fetch user data."""
    client = MongoClient("mongodb+srv://admin:1234@cokguzelyasadb.1puka.mongodb.net/")
    db = client["cokguzelyasadb"]
    collection = db["users_customuser"]
    user_data = (
        collection.find_one()
    )  # will be replaced with the actual query with user_id (or token)
    analysis_collection = db["recommendations_photoanalysis"]
    # find the analysis result for the user using the user_id
    analysis_result = analysis_collection.find_one({"user_id": user_data["id"]})

    user = User(
        user_id=user_data["id"],
        name=user_data["first_name"],
        # date_of_birth=user_data["date_of_birth"],
        chronic_illnesses=user_data["chronic_illnesses"],
        allergies=user_data["allergies"],
        current_medications=user_data["current_medications"],
        analysis_result=analysis_result["analysis_result"],
    )

    return user


@tool
def get_user(
    field: Optional[
        Literal[
            "user_id",
            "name",
            # "date_of_birth",
            "chronic_illnesses",
            "allergies",
            "current_medications",
            "analysis_result",
        ]
    ] = None,
) -> str:
    """
    Description: Get user data.

    Args:
        field (Optional[Literal["user_id", "name", "chronic_illnesses", "allergies", "current_medications", "analysis_result"]], optional): Field to get. Defaults to None.

    Returns:
        str: User data.

    Example:
        get_user("name") -> "John Doe"
        get_user() -> "{'user_id': 1, 'name': 'John Doe', 'chronic_illnesses': ['Hypertension', 'Diabetes'], 'allergies': ['Peanuts', 'Penicillin'], 'current_medications': ['Lisinopril', 'Metformin', 'Ritalin'], 'analysis_result': 'The hair thinning on the top and hairline recession suggest an early stage of hair loss. Based on the Norwood scale, this appears to be between Norwood 2 to 3 (mild to moderate thinning/recession). The crown area seems relatively stable, with minor thinning.'}"

    """
    user = fetch_user_data()
    if field:
        return getattr(user, field)
    return user.model_dump()


available_functions = {"get_user": get_user}
