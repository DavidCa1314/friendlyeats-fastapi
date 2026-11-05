from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.restaurants import router as restaurants_router
from app.services.restaurant_service import RestaurantService

app = FastAPI(title="FriendlyEats")

# Instancia del servicio de restaurantes
service = RestaurantService()

# Montar archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Incluir rutas de la API v1 (/api/v1/restaurants)
app.include_router(restaurants_router, prefix="/api/v1")


# app/main.py

@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    category: str | None = None,
    city: str | None = None,
    price: str | None = None  # Cambiado a str para aceptar "" sin lanzar error 422
):
    # Limpiar cadenas vacías que envía el formulario HTML cuando no se selecciona una opción
    clean_category = category if category and category.strip() != "" else None
    clean_city = city if city and city.strip() != "" else None
    
    # Convertir el precio a entero solo si viene con un valor como "1", "2" o "3"
    clean_price = int(price) if price and price.strip().isdigit() else None

    # Consultar los restaurantes usando los valores limpios
    restaurants = service.list(category=clean_category, city=clean_city, price=clean_price)
    
    # Obtener el catálogo completo para los desplegables
    all_restaurants = service.list()
    categories = sorted(list({r.get("category") for r in all_restaurants if r.get("category")}))
    cities = sorted(list({r.get("city") for r in all_restaurants if r.get("city")}))

    return templates.TemplateResponse(
        request=request,
        name="restaurants.html",
        context={
            "restaurants": restaurants,
            "categories": categories,
            "cities": cities,
            "selected_category": clean_category,
            "selected_city": clean_city,
            "selected_price": clean_price
        }
    )


@app.get("/restaurants/new", response_class=HTMLResponse)
async def new_restaurant_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="restaurant_form.html",
        context={"restaurant": None}
    )


@app.get("/restaurants/{restaurant_id}", response_class=HTMLResponse)
async def restaurant_detail_page(request: Request, restaurant_id: str):
    # Obtiene el restaurante desde el servicio (si no existe, lanza el 404 formateado)
    restaurant = service.get(restaurant_id)
    return templates.TemplateResponse(
        request=request,
        name="restaurant_detail.html",
        context={"restaurant": restaurant}
    )


@app.get("/restaurants/{restaurant_id}/edit", response_class=HTMLResponse)
async def edit_restaurant_page(request: Request, restaurant_id: str):
    restaurant = service.get(restaurant_id)
    return templates.TemplateResponse(
        request=request,
        name="restaurant_form.html",
        context={"restaurant": restaurant}
    )