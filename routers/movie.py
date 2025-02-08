# Solamente rutas que tengan que ver con movie
from fastapi import FastAPI, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from bd.database import Session, engine, Base
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerMovie = APIRouter()

# Clase que valida la ruta. Sirve para cubrir una ruta que queramos. 
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'briandevita16@gmail.com':
            raise HTTPException(statuscode=403, detail='Credenciales incorrectas')
        # Podemos darle una dependencia a la ruta

# Vamos a crear una clase de películas a partir de BaseModel
class Movie(BaseModel):
    id: Optional[int] = None 
    title: str = Field(default='Titulo de la película', min_lenght=5, max_length=200)
    overview: str = Field(default='Descripcion de la película', min_lenght=15, max_length=200)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=100, default='Aqui va la categoria')  


# vamos a crear un nuevo endpoint para ver todas las películas en http://127.0.0.1:4000/movies
# Con depends marcamos que el usuario debe estar autenticado para ver esa ruta
# Este es el metodo tradicional
# @routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
# def get_movies():
#     return JSONResponse(content=movies)


# vamos a crear un nuevo endpoint para ver todas las películas en http://127.0.0.1:4000/movies
# Con depends marcamos que el usuario debe estar autenticado para ver esa ruta
# Este es el metodo aprovechando la base de datos que hemos creado

@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(ModelMovie).all() # con .all() nos estamos trayendo todas las features
    return JSONResponse(content=jsonable_encoder(data))

# Vamos a crear una nueva ruta para buscar una peli en función de un id
# Esta es la forma tradicional de hacerlo
# @routerMovie.get('/movies/{id}', tags=['Movies'], status_code=200)
# def get_movie(id: int = Path(ge=1, le=100)):
#     for item in movies:
#         if item["id"] == id:
#             return item
#     return []

# Vamos a crear una nueva ruta para buscar una peli en función de un id
# Aquí vamos a utilizar la base de datos creada
@routerMovie.get('/movies/{id}', tags=['Movies'], status_code=200)
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

# Parámetros de búsqueda. http://127.0.0.1:4000/movies/?category=crimen
@routerMovie.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

# # Crear un nuevo recurso con método tradicional
# @routerMovie.post('/movies', tags=['Movies'], status_code=201)
# def create_movie(movie: Movie):
#     movies.routerMovieend(movie)
#     print(movies)
#     return JSONResponse(status_code=201, content={'message': 'Se ha cargado una nueva pelicula', 'movie':[movie.dict() for m in movies]})

# # Crear un nuevo recurso con método de base de datos
@routerMovie.post('/movies', tags=['Movies'], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.dict()) # pasamos todos los parámetros y los convertimos a diccionario
    db.add(newMovie)
    db.commit()
    return JSONResponse(status_code=201, content={'message': 'Se ha cargado una nueva pelicula', 'movie':[movie.dict() for m in movies]})


# metodo putt
# Vamos a validar los parámetros
@routerMovie.put('/movies/{id}', tags=['Movies'], status_code=200)
def update_movie(id: int, movie:Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'No se encontrón el recurso'})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(content={'message': 'Se ha modificado la pelicula'})

            
# Ahora vamos a borrar una peli
@routerMovie.delete('/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id:int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'No se encontrón el recurso'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Se ha eliminado una pelicula', 'data': jsonable_encoder(data)})

