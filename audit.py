import os
import sys

# Colores para la consola (compatibles con Git Bash)
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_file(path):
    if os.path.exists(path) and os.path.isfile(path):
        print(f"{GREEN}[OK]{RESET} Archivo encontrado: {path}")
        return True
    else:
        print(f"{RED}[ERROR]{RESET} Falta el archivo: {path}")
        return False

def check_folder(path):
    if os.path.exists(path) and os.path.isdir(path):
        print(f"{GREEN}[OK]{RESET} Carpeta encontrada: {path}/")
        return True
    else:
        print(f"{RED}[ERROR]{RESET} Falta la carpeta: {path}/")
        return False

def check_absent(path):
    if os.path.exists(path):
        print(f"{RED}[CRÍTICO]{RESET} El archivo '{path}' NO DEBERÍA estar aquí. Borralo.")
        return False
    else:
        print(f"{GREEN}[OK]{RESET} Limpieza correcta: '{path}' no existe en raíz.")
        return True

def audit_content(file_path, bad_string, warning_msg):
    if not os.path.exists(file_path): return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if bad_string in content:
            print(f"{RED}[FAIL]{RESET} {file_path}: {warning_msg}")
            return False
        return True

def main():
    print(f"\n--- 🕵️‍♂️ AUDITORÍA DE KITSU FINTECH ENGINE ---\n")

    errors = 0

    # 1. Estructura de Carpetas
    structure_checks = [
        "api",
        "api/core",
        "api/services",
        "scripts",
        "n8n"
    ]
    for folder in structure_checks:
        if not check_folder(folder): errors += 1

    # 2. Archivos Esenciales
    file_checks = [
        "docker-compose.yml",
        "Dockerfile",
        "requirements.txt",
        ".gitignore",
        ".env.example",
        "README.md",
        "LICENSE",
        "api/main.py",
        "api/core/config.py",
        "api/core/security.py",
        "api/services/ollama_client.py",
        "api/services/sanitization.py",
        "scripts/init.sql",
        "n8n/workflow.json" # <--- Importante
    ]
    for file in file_checks:
        if not check_file(file): errors += 1

    # 3. Limpieza (No main.py en root)
    if not check_absent("main.py"): errors += 1

    # 4. Auditoría de Contenido (Hardcoded Paths)
    print(f"\n--- 🔍 REVISANDO CONTENIDO ---")

    # Revisar rutas de Windows en docker-compose
    if not audit_content("docker-compose.yml", ":\\", "Se encontraron rutas absolutas de Windows (Z:\\ o C:\\). Usá rutas relativas (./)."):
        errors += 1
    else:
        print(f"{GREEN}[OK]{RESET} docker-compose.yml usa rutas relativas.")

    # Revisar si n8n tiene el workflow
    if os.path.exists("n8n") and not os.listdir("n8n"):
        print(f"{RED}[FAIL]{RESET} La carpeta 'n8n/' está vacía. ¡Falta exportar el workflow.json!")
        errors += 1

    print(f"\n---------------------------------------")
    if errors == 0:
        print(f"{GREEN}✅ TODO PERFECTO. LISTO PARA EL PUSH.{RESET}")
        print("   (Podés borrar este archivo audit_repo.py antes de subirlo)")
    else:
        print(f"{RED}❌ SE ENCONTRARON {errors} ERRORES.{RESET}")
        print("   Corregilos antes de subir a GitHub.")

if __name__ == "__main__":
    main()