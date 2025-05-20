from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def events_test():
    return {"message": "Events working"}
