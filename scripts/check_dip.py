import argparse
import sys
import os
import re

def check_dip(module_name):
    domain_path = os.path.join("src", module_name, "domain")
    if not os.path.exists(domain_path):
        print(f"La ruta del dominio no existe: {domain_path}")
        return 0
    
    violations = 0
    # Patrón para buscar importaciones de infraestructura en dominio
    # Por ejemplo: 'import ...infrastructure', 'from ...infrastructure import ...'
    infra_import_pattern = re.compile(r'(import\s+.*infrastructure|from\s+.*infrastructure\s+import)')
    
    for root, dirs, files in os.walk(domain_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if infra_import_pattern.search(line):
                            print(f"VIOLACIÓN DIP en {file_path}:{line_num} -> {line.strip()}")
                            violations += 1
                            
    return violations

def main():
    parser = argparse.ArgumentParser(description="Verificar el Principio de Inversión de Dependencias (DIP).")
    parser.add_argument("--module", required=True, help="Nombre del módulo a verificar")
    args = parser.parse_args()

    print(f"Verificando DIP para el módulo: {args.module}...")
    violations = check_dip(args.module)
    
    if violations > 0:
        print(f"Fallo: Se encontraron {violations} violaciones de la regla DIP.")
        return 1
    
    print("DIP verificado con éxito: 0 violaciones encontradas.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
