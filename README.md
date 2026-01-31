# LED MCP Server

Un servidor MCP (Model Context Protocol) para controlar LEDs a través de Xiaozhi y otras aplicaciones de IA.

## 🌟 Características

- ✅ Encender/apagar LED
- ✅ Ajustar brillo (0-100%)
- ✅ Cambiar color (RGB)
- ✅ Hacer parpadear con control de duración
- ✅ Consultar estado en tiempo real
- ✅ Soporte para GPIO (Raspberry Pi)
- ✅ Soporte para comunicación serial (Arduino)
- ✅ Soporte para HTTP (ESP32)

## 📋 Requisitos

- Python 3.10 o superior
- MCP SDK 1.2.0 o superior

## 🚀 Instalación Rápida

```bash
pip install led-mcp-server
```

## 💻 Uso

```bash
led-mcp
```

## 🔧 Herramientas Disponibles

### `turn_on_led`
Enciende el LED con el brillo especificado.

**Parámetros:**
- `brightness` (int, 0-100): Nivel de brillo. Por defecto: 100

### `turn_off_led`
Apaga el LED.

### `get_led_status`
Obtiene el estado actual del LED.

### `set_brightness`
Ajusta el brillo del LED.

**Parámetros:**
- `brightness` (int, 0-100): Nuevo nivel de brillo

### `blink_led`
Hace parpadear el LED.

**Parámetros:**
- `times` (int, 1-20): Número de parpadeos. Por defecto: 3
- `duration` (int, 100-5000): Duración en ms. Por defecto: 500

### `set_led_color`
Cambia el color del LED (RGB).

**Parámetros:**
- `color` (str): Color del LED. Opciones: 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white'

## 🔌 Integración con Xiaozhi

1. Registra este servidor en imcp.pro
2. Vincula el servicio a tu agente de Xiaozhi
3. Comienza a usar comandos de voz:
   - "Enciende el LED"
   - "Apaga el LED"
   - "Aumenta el brillo"
   - "Cambia a color azul"
   - "Haz parpadear"

## 📄 Licencia

MIT License

## 🤝 Contribuciones

Las contribuciones son bienvenidas.

## 💬 Soporte

Para soporte, consulta la documentación de imcp.pro: https://imcp.pro/docs
