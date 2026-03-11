# Rosca y Votos

Mini deckbuilder web con temática de política argentina.

## ¿Cómo lo pruebo si no sé nada de código?

Tenés 2 formas. La más fácil es la **Opción A**.

### Opción A (la más simple, sin terminal)

1. Abrí la carpeta del proyecto.
2. Hacé doble click en `index.html`.
3. Se abre en el navegador y ya podés jugar.

Si se abre una pantalla en blanco, usá la Opción B.

### Opción B (con un solo comando)

1. Abrí una terminal en esta carpeta.
2. Ejecutá este comando:

```bash
python3 -m http.server 4173
```

3. Abrí tu navegador en: `http://localhost:4173`
4. Para cerrar, volvés a la terminal y presionás `Ctrl + C`.

## ¿Cómo se juega? (rápido)

1. En **Tu mano**, hacé click en **Jugar carta**.
2. Juntá **influencia** para comprar cartas del **Mercado**.
3. Hacé click en **Terminar turno** para robar 5 cartas nuevas.
4. Repetí hasta llegar al turno 12.

## Objetivo

- **Ganás** si al final del turno 12 tenés **20 o más de popularidad**.
- **Perdés** si la **tensión social** llega a **15** en cualquier momento.
