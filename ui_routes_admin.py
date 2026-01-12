import math
import os

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from pricing import get_defaults, list_materials, update_material_cost
from ui_utils import ADMIN_COOKIE_NAME, admin_cookie_valid, admin_token


router = APIRouter()


@router.post("/admin/login")
async def admin_login(request: Request):
    # Authenticate admin users and set the session cookie.
    secret = os.environ.get("ADMIN_PASSWORD", "").strip()
    if not secret:
        return JSONResponse({"ok": False, "error": "Admin password not configured"}, status_code=400)
    payload = await request.json()
    if payload.get("password", "") != secret:
        return JSONResponse({"ok": False, "error": "Invalid password"}, status_code=401)
    response = JSONResponse({"ok": True})
    response.set_cookie(
        ADMIN_COOKIE_NAME,
        admin_token(secret),
        httponly=True,
        samesite="lax",
    )
    return response


@router.post("/admin/logout")
async def admin_logout():
    # Clear the admin cookie.
    response = JSONResponse({"ok": True})
    response.delete_cookie(ADMIN_COOKIE_NAME)
    return response


@router.get("/admin/materials")
def admin_materials(request: Request):
    # Return the full materials list for the admin panel.
    if not admin_cookie_valid(request):
        return JSONResponse({"ok": False, "error": "Unauthorized"}, status_code=401)
    defaults = get_defaults()
    return JSONResponse({"ok": True, "materials": list_materials(defaults["materials_db_path"])})


@router.post("/admin/materials/update")
async def admin_update_material(request: Request):
    # Update a single material price from the admin panel.
    if not admin_cookie_valid(request):
        return JSONResponse({"ok": False, "error": "Unauthorized"}, status_code=401)
    payload = await request.json()
    name = (payload.get("name") or "").strip()
    unit_cost = payload.get("unit_cost")
    if not name:
        return JSONResponse({"ok": False, "error": "Missing material name"}, status_code=400)
    try:
        unit_cost = float(unit_cost)
    except (TypeError, ValueError):
        return JSONResponse({"ok": False, "error": "Invalid unit_cost"}, status_code=400)
    if not math.isfinite(unit_cost) or unit_cost < 0:
        return JSONResponse({"ok": False, "error": "unit_cost must be a non-negative number"}, status_code=400)
    defaults = get_defaults()
    try:
        update_material_cost(defaults["materials_db_path"], name, unit_cost)
    except ValueError as exc:
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=404)
    return JSONResponse({"ok": True})
