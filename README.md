# trabajo-ia
Trabajo Metro de México

### Instalación de dependencias
Para instalar las dependencias necesarias, se usa:
```
pip install -r requirements.txt
```
### Generación del ejecutable
Si necesitas un ejecutable con el intérprete embebido, puedes usar el fichero `main.spec` con `pyinstaller`:
```
pip install pyinstaller
pyinstaller main.spec
```
Los assets usados (la carpeta de `Imagenes/`) se copiaran automáticamente con el ejecutable al usar el archivo de spec.
