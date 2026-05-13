# main.py

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
import uvicorn
import logging

from app.operations import add, subtract, multiply, divide
from app.database import Base, engine, get_db
from app.models.calculation import Calculation
from app.models.user import User
from app.schemas.calculation import CalculationCreate, CalculationResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Module 11 Calculation API")

templates = Jinja2Templates(directory="templates")

# Create database tables
Base.metadata.create_all(bind=engine)


class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator("a", "b")
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Both a and b must be numbers.")
        return value


class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join(
        [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    )
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/add", response_model=OperationResponse)
async def add_route(operation: OperationRequest):
    result = add(operation.a, operation.b)
    return OperationResponse(result=result)


@app.post("/subtract", response_model=OperationResponse)
async def subtract_route(operation: OperationRequest):
    result = subtract(operation.a, operation.b)
    return OperationResponse(result=result)


@app.post("/multiply", response_model=OperationResponse)
async def multiply_route(operation: OperationRequest):
    result = multiply(operation.a, operation.b)
    return OperationResponse(result=result)


@app.post("/divide", response_model=OperationResponse)
async def divide_route(operation: OperationRequest):
    try:
        result = divide(operation.a, operation.b)
        return OperationResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/calculations", response_model=CalculationResponse)
async def create_calculation(
    calculation: CalculationCreate,
    db: Session = Depends(get_db),
):
    try:
        db_calculation = Calculation.create(
            calculation_type=calculation.type.value,
            user_id=calculation.user_id,
            inputs=calculation.inputs,
        )

        db_calculation.result = db_calculation.get_result()

        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation)

        return db_calculation

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/calculations", response_model=list[CalculationResponse])
async def get_calculations(db: Session = Depends(get_db)):
    return db.query(Calculation).all()


@app.get("/calculations/{calculation_id}", response_model=CalculationResponse)
async def get_calculation(calculation_id: str, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()

    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")

    return calculation


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)