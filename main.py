from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form 

from fastapi import FastAPI, Request, Form
from data.database import database
from typing import Annotated
from data.dao.dao_coches import DaoCoches
from data.modelo.coche import Coche
from fastapi.responses import RedirectResponse
from pydantic import BaseModel


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

marcas = [
    {"id": "bmw", "nombre": "BMW", "logo": "bmw.jpg"},
    {"id": "mitsubishi", "nombre": "Mitsubishi", "logo": "mitsubishi.jpg"},
    {"id": "subaru", "nombre": "Subaru", "logo": "logosubaru.jpg"},
    {"id": "honda", "nombre": "Honda", "logo": "honda2.jpg"},
    {"id": "audi", "nombre": "Audi", "logo": "audi.jpg"},
    {"id": "mercedes", "nombre": "Mercedes", "logo": "mercedes.jpg"},
    {"id": "citroen", "nombre": "Citroën", "logo": "citroen.jpg"},
    {"id": "renault", "nombre": "Renault", "logo": "renaultlogo.jpg"}
]

marcas_info = {
    "bmw": {
        "nombre": "BMW",
        "descripcion": "BMW es una marca alemana conocida por su lujo y rendimiento.",
        "modelos": [
            {"nombre": "E46", "imagen": "e46.jpg", "piezas": ["Alerón", "Suspensión", "Neumáticos"]},
            {"nombre": "E92", "imagen": "e92.jpg", "piezas": ["Spoilers", "Ruedas", "Sistema de escape"]},
            {"nombre": "F30", "imagen": "f30.jpg", "piezas": ["Alerón trasero", "Suspensión deportiva", "Frenos"]},
        ]
    },
    "mitsubishi": {
        "nombre": "Mitsubishi",
        "descripcion": "Mitsubishi es conocida por sus coches confiables y deportivos.",
        "modelos": [
            {"nombre": "Lancer Evolution", "imagen": "evo.jpg", "piezas": ["Alerón", "Suspensión", "Neumáticos"]},
            {"nombre": "Eclipse", "imagen": "eclipse.jpg", "piezas": ["Frenos de alto rendimiento", "Suspensión baja", "Escape"]},
            {"nombre": "Outlander", "imagen": "outlander.jpg", "piezas": ["Llantas", "Suspensión de off-road", "Neumáticos"]},
        ]
    },
    "subaru": {
        "nombre": "Subaru",
        "descripcion": "Subaru se destaca por sus coches con tracción integral y rendimiento deportivo.",
        "modelos": [
            {"nombre": "Impreza WRX", "imagen": "subaru.jpg", "piezas": ["Suspensión", "Neumáticos de alto rendimiento", "Turbocompresor"]},
            {"nombre": "Forester", "imagen": "forester.jpg", "piezas": ["Alerón", "Llantas", "Suspensión"]},
            {"nombre": "BRZ", "imagen": "brz.jpg", "piezas": ["Sistema de escape", "Suspensión", "Frenos"]},
        ]
    },
    "honda": {
        "nombre": "Honda",
        "descripcion": "Honda es conocida por sus coches económicos y fiables, con una gama deportiva destacada.",
        "modelos": [
            {"nombre": "Civic", "imagen": "civic.jpg", "piezas": ["Frenos deportivos", "Alerón", "Suspensión"]},
            {"nombre": "Accord", "imagen": "accord.jpg", "piezas": ["Ruedas", "Suspensión", "Escape"]},
            {"nombre": "NSX", "imagen": "nsx.jpg", "piezas": ["Suspensión de competición", "Frenos de carbono", "Escape"]},
        ]
    },
    "audi": {
        "nombre": "Audi",
        "descripcion": "Audi es una marca premium alemana, reconocida por sus coches de lujo y tecnología avanzada.",
        "modelos": [
            {"nombre": "A3", "imagen": "a3.jpg", "piezas": ["Suspensión", "Alerón", "Ruedas"]},
            {"nombre": "A4", "imagen": "a4.jpg", "piezas": ["Escape deportivo", "Suspensión", "Turbocompresor"]},
            {"nombre": "Q5", "imagen": "q5.jpg", "piezas": ["Ruedas", "Llantas personalizadas", "Suspensión"]},
        ]
    },
    "mercedes": {
        "nombre": "Mercedes",
        "descripcion": "Mercedes-Benz es una marca alemana de coches de lujo, conocida por su elegancia y rendimiento.",
        "modelos": [
            {"nombre": "Clase C", "imagen": "clase_c.jpg", "piezas": ["Suspensión", "Ruedas deportivas", "Escape"]},
            {"nombre": "Clase E", "imagen": "clase_e.jpg", "piezas": ["Alerón", "Suspensión neumática", "Frenos"]},
            {"nombre": "GLE", "imagen": "gle.jpg", "piezas": ["Neumáticos de alto rendimiento", "Suspensión", "Escape"]},
        ]
    },
    "citroen": {
        "nombre": "Citroën",
        "descripcion": "Citroën es una marca francesa famosa por su confort y diseño innovador.",
        "modelos": [
            {"nombre": "C3", "imagen": "c3.jpg", "piezas": ["Alerón", "Suspensión", "Ruedas"]},
            {"nombre": "C4", "imagen": "c4.jpg", "piezas": ["Suspensión deportiva", "Escape", "Ruedas"]},
            {"nombre": "Berlingo", "imagen": "berlingo.jpg", "piezas": ["Llantas", "Suspensión", "Turbocompresor"]},
        ]
    },
    "renault": {
        "nombre": "Renault",
        "descripcion": "Renault es una marca francesa conocida por su fiabilidad y vehículos económicos.",
        "modelos": [
            {"nombre": "Clio", "imagen": "clio.jpg", "piezas": ["Suspensión", "Frenos deportivos", "Ruedas"]},
            {"nombre": "Megane", "imagen": "megane.jpg", "piezas": ["Alerón", "Ruedas", "Escape"]},
            {"nombre": "Kangoo", "imagen": "kangoo.jpg", "piezas": ["Suspensión", "Neumáticos de alto rendimiento", "Escape"]},
        ]
    }
}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/gallery", response_class=HTMLResponse)
def gallery(request: Request, search: str = ""):
    if search:
        marcas_filtradas = [marca for marca in marcas if search.lower() in marca["nombre"].lower()]
    else:
        marcas_filtradas = marcas
    
    return templates.TemplateResponse("gallery.html", {
        "request": request,
        "marcas": marcas_filtradas,
        "search_term": search
    })

@app.get("/contact", response_class=HTMLResponse)
def contact_get(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/services", response_class=HTMLResponse)
def services(request: Request):
    return templates.TemplateResponse("servicios.html", {"request": request})

@app.get("/servicios", response_class=HTMLResponse)
def servicios(request: Request):
    return templates.TemplateResponse("servicios.html", {"request": request})

@app.get("/sobrenosotros", response_class=HTMLResponse)
def sobrenosotros(request: Request):
    return templates.TemplateResponse("sobrenosotros.html", {"request": request})

@app.get("/marca/{nombre_marca}", response_class=HTMLResponse)
def marca(request: Request, nombre_marca: str):
    if nombre_marca in marcas_info:
        info = marcas_info[nombre_marca]
        return templates.TemplateResponse("marca.html", {
            "request": request,
            "nombre": info["nombre"],
            "descripcion": info["descripcion"],
            "modelos": info["modelos"]
        })
    else:
        return templates.TemplateResponse("404.html", {"request": request})

@app.post("/contact", response_class=HTMLResponse)
def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    confirmation_message = "Gracias, {}. Hemos recibido tu mensaje y te responderemos pronto.".format(name)
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "confirmation_message": confirmation_message
    })

@app.get("/")
def read_root():
    return DaoCoches().get_all(database)

@app.get("/coches")
def get_coches(request: Request, marca: str = "marca", modelo: str = "modelo"):
    coches = DaoCoches().get_all(database)
    return templates.TemplateResponse(
        "coches.html", 
        {"request": request, "coches": coches}
    )

@app.post("/coches/add")
async def add_coches(request: Request, modelo: str = Form(...)):
    dao = DaoCoches()
    coche = Coche(id=None, modelo=modelo)  
    dao.add(database, coche)
    
    return RedirectResponse(url="/coches", status_code=303)


class CocheDelete(BaseModel):
    modelo: str

@app.post("/coches/delete")
def delete_coches(request: Request, modelo: str = Form(...)):  
    dao = DaoCoches()
    
    dao.delete(database, modelo)
    
    coches = dao.get_all(database)

    return templates.TemplateResponse(
        "coches.html", 
        {"request": request, "coches": coches, "message": f"Coche '{modelo}' eliminado correctamente"}
    )

@app.get("/coches/buscar")
def buscar_coche(request: Request, modelo: str):
    coches = DaoCoches().get_all(database)
    
    coche_encontrado = None
    for coche in coches:
        if coche.modelo.lower() == modelo.lower():
            coche_encontrado = coche
            break
    
    if coche_encontrado:
        return templates.TemplateResponse("coche_encontrado.html", {"request": request, "coche": coche_encontrado})
    else:
        return templates.TemplateResponse("coches.html", {"request": request, "coches": coches, "message": f"No se encontró el coche '{modelo}'."})

