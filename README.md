# Minimal Analog Clock

Este proyecto es un reloj analógico minimalista desarrollado en Python con Tkinter. Incorpora diversas funcionalidades adicionales para mejorar la experiencia visual y funcional:

## Funcionalidades

- **Reloj Analógico Dinámico:**  
  - Se adapta al tamaño de la ventana.  
  - Las manecillas (hora, minuto y segundo) se actualizan en tiempo real.

- **Zona Horaria Personalizable:**  
  - Permite seleccionar la zona horaria deseada mediante un menú desplegable (por ejemplo: UTC, America/Bogota, Europe/London, Asia/Tokyo, etc.).

- **Modo Claro/Oscuro:**  
  - Botón para alternar entre modo claro y oscuro.

- **Reloj Digital y Fecha:**  
  - Se muestra la hora digital en la esquina inferior derecha.  
  - Se muestra la fecha (día, mes y año) en la esquina inferior izquierda.

- **Opciones de Estilo del Reloj:**  
  - **Mostrar/Ocultar Números:** Opción para alternar la visualización de los números en el dial del reloj.  
  - **Cambio de Estilo de Manecillas:** Permite cambiar entre un estilo "Clásico" y "Moderno" (se ajustan las longitudes y grosores de las manecillas).

- **Sonido de Tic-Tac:**  
  - Se reproduce un sonido (tic) cada segundo para simular el sonido de un reloj real.

## Requisitos

- Python 3.x
- Tkinter (incluido en la mayoría de las instalaciones de Python)
- pygame (para la reproducción del sonido)
- pytz (para el manejo de zonas horarias)

### Instalación de dependencias

```bash
pip install pygame pytz
```

