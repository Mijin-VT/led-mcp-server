#!/usr/bin/env python3
"""
LED MCP Server - Control LEDs through Model Context Protocol
Permite controlar LEDs a través de Xiaozhi y otras aplicaciones de IA
"""

import asyncio
import json
import logging
from typing import Any

import mcp.server.stdio
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Estado simulado del LED
led_state = {
    "is_on": False,
    "brightness": 0,
    "color": "white",
    "blink_count": 0,
}

# Crear servidor MCP
server = Server("led-mcp-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Lista todas las herramientas disponibles para controlar LEDs"""
    return [
        Tool(
            name="turn_on_led",
            description="Enciende el LED con el brillo especificado (0-100%)",
            inputSchema={
                "type": "object",
                "properties": {
                    "brightness": {
                        "type": "integer",
                        "description": "Nivel de brillo del LED (0-100). Por defecto: 100",
                        "minimum": 0,
                        "maximum": 100,
                    }
                },
                "required": [],
            },
        ),
        Tool(
            name="turn_off_led",
            description="Apaga el LED completamente",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="get_led_status",
            description="Obtiene el estado actual del LED (encendido/apagado, brillo, color)",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="set_brightness",
            description="Ajusta el brillo del LED a un nivel específico (0-100%)",
            inputSchema={
                "type": "object",
                "properties": {
                    "brightness": {
                        "type": "integer",
                        "description": "Nuevo nivel de brillo (0-100)",
                        "minimum": 0,
                        "maximum": 100,
                    }
                },
                "required": ["brightness"],
            },
        ),
        Tool(
            name="blink_led",
            description="Hace parpadear el LED un número específico de veces",
            inputSchema={
                "type": "object",
                "properties": {
                    "times": {
                        "type": "integer",
                        "description": "Número de parpadeos (1-20). Por defecto: 3",
                        "minimum": 1,
                        "maximum": 20,
                    },
                    "duration": {
                        "type": "integer",
                        "description": "Duración de cada parpadeo en milisegundos (100-5000). Por defecto: 500",
                        "minimum": 100,
                        "maximum": 5000,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="set_led_color",
            description="Cambia el color del LED (solo para LEDs RGB)",
            inputSchema={
                "type": "object",
                "properties": {
                    "color": {
                        "type": "string",
                        "description": "Color del LED: red, green, blue, yellow, cyan, magenta, white",
                        "enum": ["red", "green", "blue", "yellow", "cyan", "magenta", "white"],
                    }
                },
                "required": ["color"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Ejecuta las herramientas disponibles"""

    if name == "turn_on_led":
        brightness = arguments.get("brightness", 100)
        led_state["is_on"] = True
        led_state["brightness"] = brightness
        logger.info(f"LED encendido al {brightness}%")
        return [
            TextContent(
                type="text",
                text=f"✓ LED encendido correctamente con brillo al {brightness}%",
            )
        ]

    elif name == "turn_off_led":
        led_state["is_on"] = False
        led_state["brightness"] = 0
        logger.info("LED apagado")
        return [TextContent(type="text", text="✓ LED apagado correctamente")]

    elif name == "get_led_status":
        status = {
            "encendido": led_state["is_on"],
            "brillo": led_state["brightness"],
            "color": led_state["color"],
        }
        status_text = f"""
Estado del LED:
- Encendido: {'Sí' if led_state['is_on'] else 'No'}
- Brillo: {led_state['brightness']}%
- Color: {led_state['color']}
"""
        logger.info(f"Estado consultado: {status}")
        return [TextContent(type="text", text=status_text.strip())]

    elif name == "set_brightness":
        brightness = arguments.get("brightness", 50)
        if not 0 <= brightness <= 100:
            return [
                TextContent(
                    type="text",
                    text=f"✗ Error: El brillo debe estar entre 0 y 100. Recibido: {brightness}",
                )
            ]
        led_state["brightness"] = brightness
        if brightness > 0:
            led_state["is_on"] = True
        logger.info(f"Brillo ajustado a {brightness}%")
        return [
            TextContent(
                type="text",
                text=f"✓ Brillo ajustado correctamente a {brightness}%",
            )
        ]

    elif name == "blink_led":
        times = arguments.get("times", 3)
        duration = arguments.get("duration", 500)
        logger.info(f"LED parpadeando {times} veces con duración {duration}ms")
        return [
            TextContent(
                type="text",
                text=f"✓ LED parpadeando {times} veces con duración de {duration}ms cada parpadeo",
            )
        ]

    elif name == "set_led_color":
        color = arguments.get("color", "white")
        valid_colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white"]
        if color not in valid_colors:
            return [
                TextContent(
                    type="text",
                    text=f"✗ Error: Color no válido. Colores disponibles: {', '.join(valid_colors)}",
                )
            ]
        led_state["color"] = color
        logger.info(f"Color del LED cambiado a {color}")
        return [
            TextContent(
                type="text",
                text=f"✓ Color del LED cambiado correctamente a {color}",
            )
        ]

    else:
        return [TextContent(type="text", text=f"✗ Herramienta desconocida: {name}")]


async def main():
    """Inicia el servidor MCP"""
    logger.info("Iniciando LED MCP Server...")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, asyncio.Event())


if __name__ == "__main__":
    asyncio.run(main())
