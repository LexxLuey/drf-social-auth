from ninja import NinjaAPI
from cinema.api import router

api = NinjaAPI()

api.add_router("cinema/", router)    # You can add a router as an object
# api.add_router("cinema/", "cinema.api.router")  #   or by Python path