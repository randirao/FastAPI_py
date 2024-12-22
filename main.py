from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.services.hospital_service import generate_hospital_map

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_map = generate_hospital_map()
    return HTMLResponse(content=html_map)

@app.get("/map", response_class=HTMLResponse)
def get_hospital_map():
    html_map = generate_hospital_map()
    
    return HTMLResponse(content=html_map)