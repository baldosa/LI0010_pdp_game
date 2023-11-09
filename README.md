# Asteroids + NAVE

Intendo de mezclar el clásico Asteroids con [NAVE](https://videogamo.com/navearcade/), donde cada enemigo que mates hace crecer tu nave hasta que se vuelve incontrolablemente grande.

### Run

Requisito Python >= 3.10

1. Crear y activar virtual env

```bash
python -m venv venv
source venv/bin/activate
```

2. Instalar requisitos

```bash
pip install -r requirements.txt
```

3. Ejecutar

```bash
python run.py
```

4. Se mueve con WASD y se dispara con left click

### TODO

- [x] Movimiento de la nave
- [x] Disparo de proyectiles
- [x] Ángulo correcto de proyectiles 🫠
- [x] Spawn enemigos/asteroides
- [ ] Coallition dectection
- [ ] Crecimiento de la nave
- [ ] Powerups?
- [ ] Ship HP?
- [ ] Score
- [ ] Highscore
