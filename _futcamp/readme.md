# Futcamp

## Instruções:

<br/>

### Crie o ambiente virtual

```
python -m venv venv
```

### Ative o venv

```bash
# linux:

source venv/bin/activate

# windows:

source ./venv/Scripts/activate

```

### Instale as dependências

```
pip install -r requirements.txt
```

### Instale o pip 22.3

```
python.exe -m pip install --upgrade pip
```

### Execute as migrações

```
python manage.py migrate
```

## Rodar os testes:

<br/>

### Para rodar os testes utilize um dos comandos abaixo:

```python
./manage.py test
```

ou para mais detalhes

```
./manage.py test -v2
```

### Rodar os testes com coverage

```
coverage run ./manage.py test
```

### Exibir o relatório

```
coverage report
```

