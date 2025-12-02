from fastapi import APIRouter, Query
import logging

router = APIRouter()
logger = logging.getLogger("backend_logger")

@router.get("/api/reverse")
def reverse_string(text: str = Query(...)):
    logger.info("Reverse endpoint called with text=%s", text)
    return {"reversed": text[::-1]}

@router.get("/api/add")
def add_numbers(a: int = Query(...), b: int = Query(...)):
    logger.info("Add endpoint called with a=%d, b=%d", a, b)
    return {"sum": a + b}

@router.get("/api/echo")
def echo_message(message: str = Query(...)):
    logger.info("Echo endpoint called with message=%s", message)
    return {"echo": message}

@router.get("/api/multiply")
def multiply_numbers(x: int = Query(...), y: int = Query(...)):
    logger.info("Multiply endpoint called with x=%d, y=%d", x, y)
    abc = x * y
    return {"product": abc}