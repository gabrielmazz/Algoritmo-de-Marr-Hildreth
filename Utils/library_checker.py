import importlib
import subprocess
import sys

def check_library():
    
    # Lista de bibliotecas necessárias
    bibliotecas = [
        'rich',
        'matplotlib',
        'numpy',
        'requests',
        'PIL',
        'io',
    ]
    
    print('Verificando bibliotecas...')
    
    # Verifica se todas as bibliotecas estão instaladas
    for lib in bibliotecas:
        
        try:
            # Tenta importar a biblioteca
            importlib.import_module(lib)
            print(f'[OK] Biblioteca {lib} está instalada')
        
        except ImportError:
            
            # Se a biblioteca não estiver instalada, tenta instalar
            print(f'[ERRO] Biblioteca {lib} não está instalada. Instalando...')
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f'[OK] Biblioteca {lib} instalada com sucesso')
            
    print('Verificação de bibliotecas concluída')