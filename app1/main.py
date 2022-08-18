from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.responses import StreamingResponse
import io
import pandas as pd

csv_file_path_docker = "app/data/sample_data.csv"
csv_file_path_local = "data/sample_data.csv"

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


sqlite_file_name = "database1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/app1/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/app1/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

@app.get("/app1/get_csv")
async def get_csv():
    try:
        df = pd.read_csv(csv_file_path_docker)
    except:
        df = pd.read_csv(csv_file_path_local)

    stream = io.StringIO()
    df.to_csv(stream, index = False)
    response = StreamingResponse(iter([stream.getvalue()]),
                        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response