from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import shutil, os, uuid

DATABASE_URL = "postgresql://admin:admin@localhost:5432/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    model_language = Column(String(50), nullable=False)
    model_file_path = Column(String(255), nullable=True)
    error_file_path = Column(String(255), nullable=True)
    llm = Column(String(50), nullable=False)
    language = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
Base.metadata.create_all(bind=engine)

db = SessionLocal()
db.execute(text("ALTER TABLE tasks ALTER COLUMN model_language SET DEFAULT 'UML';"))
db.commit()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/tasks")
async def create_task(
    title: str = Form(...),
    description: str = Form(None),
    model_language: str = Form(...),
    model_file: UploadFile = None,
    error_file: UploadFile = None,
    llm: str = Form(...),
    language: str = Form(...)
):
    db = SessionLocal()
    
    def save_file(file: UploadFile):
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        existing = (
            db.query(Task)
            .filter(
                (Task.model_file_path == file_path) | (Task.error_file_path == file_path)
            ).first()
        )
        
        if existing:
            raise HTTPException(status_code=400, detail="File with the same name already exists.")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return file_path
    
    model_path = save_file(model_file) if model_file else None
    error_path = save_file(error_file) if error_file else None
    
    new_task = Task(
        title = title,
        description = description,
        model_language = model_language,
        model_file_path = model_path,
        error_file_path = error_path,
        llm = llm,
        language = language
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()
    
    return {"id": new_task.id, "title": new_task.title}

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    db.close()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "model_language": task.model_language,
        "model_file_path": task.model_file_path,
        "error_file_path": task.error_file_path,
        "llm": task.llm,
        "language": task.language,
        "created_at": task.created_at
    }
    
@app.get("/tasks")
def get_all_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "model_language": task.model_language,
            "model_file_path": task.model_file_path,
            "error_file_path": task.error_file_path,
            "llm": task.llm,
            "language": task.language,
            "created_at": task.created_at
        }
        for task in tasks
    ]

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    try:
        # Just run a trivial query
        result = db.execute(text("SELECT 1")).scalar()
        return {"db_connection": "ok", "result": result}
    except Exception as e:
        return {"db_connection": "failed", "error": str(e)}