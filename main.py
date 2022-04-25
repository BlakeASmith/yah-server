from fastapi import FastAPI
from datetime import datetime
from databases import Database
from sqlalchemy import MetaData, create_engine
import ormar


db_url = "sqlite:///db.sqlite"


db = Database(db_url)
metadata = MetaData()


class Highlight(ormar.Model):
    class Meta(ormar.ModelMeta):
        tablename = "highlights"
        database = db
        metadata = metadata

    id: str = ormar.String(primary_key=True, max_length=1000)
    url: str = ormar.String(max_length=1000)
    title: str = ormar.String(max_length=1000)
    date: datetime = ormar.DateTime()
    contentRawHTML: str = ormar.String(max_length=100000)
    noteRawHTML: str = ormar.String(max_length=100000)


app = FastAPI()

engine = create_engine(db_url)
metadata.create_all(engine)


@app.get('/')
async def root():
    return {"message": "Hllo World"}


@app.post('/highlight/')
async def store_highlight(hl: Highlight):
    return await hl.save()
