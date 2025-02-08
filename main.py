from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from bd.database import engine, Base
from routers.movie import routerMovie
from routers.users import login_user

# Instancia de aplicación
app = FastAPI(
    title = 'Aprendiendo FastApi', # Se le puede cambiar el título
    description='Una api en los primeros pasos', # Cambiar descripción
    version='0.0.1' # cambiar versión    
)

app.include_router(routerMovie)
app.include_router(login_user)


# Vamos a integrar la base de datos
Base.metadata.create_all(bind=engine)


@app.get("/", tags = ['inicio']) # Con / ruta principal, y tags etiquetas
def read_root():
    # return {"Hello": "world"} # Primer tipo de consulta para obtener un objeto fast api http://127.0.0.1:4000/docs
    return HTMLResponse('<h2> Hola mundo! </h2>') # obtenemos solo un texto Hola Mundo

