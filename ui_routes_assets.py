import os

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse

from pricing import get_defaults


router = APIRouter()


@router.get("/styles.css")
def styles_css():
    # Serve the main stylesheet.
    return FileResponse("assets/CSS/styles.css", media_type="text/css")


@router.get("/three.r134.min.js")
def three_js():
    # Serve the Three.js vendor bundle.
    return FileResponse("assets/JS/three.r134.min.js", media_type="application/javascript")


@router.get("/vanta.waves.min.js")
def vanta_waves_js():
    # Serve the Vanta waves effect script.
    return FileResponse("assets/JS/vanta.waves.min.js", media_type="application/javascript")


@router.get("/download/{filename}")
def download(filename: str):
    # Serve generated quote files from the output directory.
    defaults = get_defaults()
    safe_name = os.path.basename(filename)
    path = os.path.join(defaults["output_dir"], safe_name)
    if not os.path.exists(path):
        return HTMLResponse("File not found", status_code=404)
    return FileResponse(path, filename=safe_name, media_type="text/markdown")
