# Faceblur

## Ambiente desenvolvimento (Linux):
```bash
virtualenv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```

## Build:
```bash
pyinstaller --onefile faceblur.py
```

## Exemplos
### Imagem:
```bash
./dist/faceblur exemplos/exemplo_foto_1.jpg
```

### Video:
```bash
./dist/faceblur exemplos/exemplo_video.mp4
```

### Câmera:
```bash
./dist/faceblur 0
```