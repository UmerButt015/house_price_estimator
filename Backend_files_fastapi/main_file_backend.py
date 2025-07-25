# -*- coding: utf-8 -*-

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from House_system import router as house_router

app = FastAPI()

# ✅ Add CORS Middleware here (global for all routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chatbot_router)
app.include_router(calculator_router)
app.include_router(car_details_router)
app.include_router(house_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
