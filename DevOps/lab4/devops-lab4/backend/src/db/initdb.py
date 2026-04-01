import models
import models.base
from db.session import engine

def initdb():
    models.base.Base.metadata.create_all(engine)