from contextlib import asynccontextmanager
from typing import Literal

from fastapi import (
    FastAPI,
    HTTPException,
    Request
)

from pydantic import (
    BaseModel,
    Field
)

from .assistant import MoodleGuideAssistant


class QuestionRequest(BaseModel):
    text: str = Field(
        min_length=3,
        max_length=1000,
        description=(
            "Student or instructor question"
        )
    )

    language: Literal[
        "ar",
        "en"
    ]

    user_role: Literal[
        "student",
        "instructor"
    ]


class ExtractedEntity(BaseModel):
    type: str
    value: str


class SimilarQuestion(BaseModel):
    question: str
    topic: str
    score: float


class QuestionResponse(BaseModel):
    question: str
    language: str
    user_role: str

    predicted_topic: str
    topic_source: str
    classification_confidence: float

    sentiment: str
    sentiment_confidence: float
    sentiment_source: str
    sentiment_scores: dict[str, float]

    entities: list[ExtractedEntity]

    support_priority: str

    answer: str
    route_to: str
    search_score: float

    similar_questions: list[
        SimilarQuestion
    ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting MoodleGuide API...")

    app.state.assistant = (
        MoodleGuideAssistant()
    )

    print("MoodleGuide API is ready")

    yield

    print("Stopping MoodleGuide API...")


app = FastAPI(
    title="MoodleGuide API",
    description=(
        "Bilingual intelligent academic "
        "assistant for Moodle LMS"
    ),
    version="1.3.0",
    lifespan=lifespan
)


@app.get("/")
def root():
    return {
        "name": "MoodleGuide",
        "version": "1.3.0",
        "message": (
            "Bilingual academic assistant "
            "for Moodle LMS"
        ),
        "documentation": "/docs"
    }


@app.get("/health")
def health(request: Request):
    assistant_ready = hasattr(
        request.app.state,
        "assistant"
    )

    return {
        "status": (
            "healthy"
            if assistant_ready
            else "starting"
        ),
        "assistant_ready": assistant_ready
    }


@app.get("/topics")
def topics():
    return {
        "topics": [
            "login_access",
            "course_enrollment",
            "assignment",
            "quiz_exam",
            "grades",
            "course_content",
            "attendance",
            "notifications",
            "virtual_class",
            "technical_problem"
        ],
        "roles": [
            "student",
            "instructor"
        ],
        "languages": [
            "ar",
            "en"
        ],
        "sentiments": [
            "positive",
            "neutral",
            "negative"
        ],
        "priorities": [
            "normal",
            "medium",
            "high"
        ],
        "entity_types": [
            "PERSONAL_DATA",
            "FILE_TYPE",
            "DATE",
            "ERROR_CODE",
            "COURSE",
            "ASSIGNMENT",
            "QUIZ",
            "MOODLE_FEATURE"
        ]
    }


@app.post(
    "/v1/ask",
    response_model=QuestionResponse
)
def ask_question(
    payload: QuestionRequest,
    request: Request
):
    try:
        assistant = (
            request.app.state.assistant
        )

        result = assistant.answer(
            text=payload.text,
            language=payload.language,
            user_role=payload.user_role
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except Exception as error:
        print(
            "Request processing error:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "The assistant could not "
                "process the request."
            )
        ) from error