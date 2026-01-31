#!/usr/bin/env python3
"""
Web server wrapper for LED MCP Server
Proporciona un endpoint HTTP para que Render pueda monitorear el servidor
"""

import asyncio
import logging
import os
import subprocess
import sys
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(title="LED MCP Server", version="1.0.0")

# Variable global para el proceso MCP
mcp_process = None


@app.on_event("startup")
async def startup_event():
    """Inicia el servidor MCP al iniciar la aplicación"""
    global mcp_process
    logger.info("Iniciando servidor MCP...")
    try:
        # Iniciar el servidor MCP como un subproceso
        mcp_process = subprocess.Popen(
            [sys.executable, "-m", "led_mcp_server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logger.info(f"Servidor MCP iniciado con PID: {mcp_process.pid}")
    except Exception as e:
        logger.error(f"Error al iniciar servidor MCP: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Detiene el servidor MCP al cerrar la aplicación"""
    global mcp_process
    if mcp_process:
        logger.info("Deteniendo servidor MCP...")
        mcp_process.terminate()
        try:
            mcp_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            mcp_process.kill()
        logger.info("Servidor MCP detenido")


@app.get("/")
async def root():
    """Endpoint raíz para verificar que el servidor está activo"""
    return {
        "status": "ok",
        "service": "LED MCP Server",
        "version": "1.0.0",
        "mcp_status": "running" if mcp_process and mcp_process.poll() is None else "stopped",
    }


@app.get("/health")
async def health():
    """Endpoint de salud para Render"""
    if mcp_process and mcp_process.poll() is None:
        return JSONResponse({"status": "healthy"}, status_code=200)
    else:
        return JSONResponse({"status": "unhealthy"}, status_code=503)


@app.get("/api/led/status")
async def get_led_status():
    """Obtiene el estado del LED (simulado)"""
    return {
        "is_on": False,
        "brightness": 0,
        "color": "white",
        "message": "Este es un endpoint de demostración. El servidor MCP se comunica a través de stdio.",
    }


@app.post("/api/led/on")
async def turn_on_led(brightness: int = 100):
    """Enciende el LED (simulado)"""
    if not 0 <= brightness <= 100:
        raise HTTPException(status_code=400, detail="Brightness must be between 0 and 100")
    return {
        "status": "ok",
        "message": f"LED encendido al {brightness}%",
        "note": "Este es un endpoint de demostración. El servidor MCP se comunica a través de stdio.",
    }


@app.post("/api/led/off")
async def turn_off_led():
    """Apaga el LED (simulado)"""
    return {
        "status": "ok",
        "message": "LED apagado",
        "note": "Este es un endpoint de demostración. El servidor MCP se comunica a través de stdio.",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Iniciando servidor web en puerto {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
