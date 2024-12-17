import os
import sys
import datetime
from collections import defaultdict

def parse_logs(input_file, output_file):
    """
    Analyse un fichier de log pour détecter les SUPI non légitimes.
    Les SUPI qui envoient 5 requêtes ou plus dans une minute sont considérés comme suspects.

    Args:
        input_file (str): Chemin vers le fichier de logs.
        output_file (str): Chemin pour le fichier de sortie contenant les SUPI suspects.
    """

    # Vérifier si le fichier existe
    if not os.path.exists(input_file):
        print(f"Erreur : Le fichier '{input_file}' n'existe pas.")
        sys.exit(1)

    # Structure pour stocker les timestamps des requêtes par SUPI
    supi_requests = defaultdict(list)

    # Lire et analyser le fichier de log
    print("\nAnalyse des logs en cours...\n")
    with open(input_file, 'r') as log_file:
        for line_number, line in enumerate(log_file, 1):
            try:
                line = line.strip()
                if not line:  # Ignorer les lignes vides
                    continue
                parts = line.split()
                timestamp_str = f"{parts[0]} {parts[1]}"
                supi = parts[2].split(":")[1]  # Extraction du SUPI

                timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                supi_requests[supi].append(timestamp)

            except (IndexError, ValueError):
                print(f"[WARNING] Ligne ignorée (format invalide) à la ligne {line_number} -> {line}")
                continue

    # Détecter les SUPI suspects
    print("\nDétection des SUPI suspects...\n")
    suspicious_supi = set()
    for supi, timestamps in supi_requests.items():
        timestamps.sort()  # Trier les timestamps
        for i in range(len(timestamps) - 4):  # Fenêtre de 5 requêtes
            if (timestamps[i + 4] - timestamps[i]).total_seconds() < 60:  # Strictement moins de 60 secondes
                suspicious_supi.add(supi)
                print(f"[ALERT] SUPI suspect détecté : {supi}")
                break  # Passer au SUPI suivant

    # Écrire les SUPI suspects dans un fichier de sortie
    with open(output_file, 'w') as out_file:
        for supi in suspicious_supi:
            out_file.write(f"{supi}\n")

    print("\nAnalyse terminée.")
    print(f"Nombre total de SUPI suspects détectés : {len(suspicious_supi)}")
    print(f"SUPI suspects sauvegardés dans : {output_file}")

    # Afficher les SUPI suspects à la sortie standard (stdout)
    if suspicious_supi:
        print("\n[RESULT] SUPI suspects détectés :")
        for supi in suspicious_supi:
            print(supi)
    else:
        print("\n[RESULT] Aucun SUPI suspect détecté.")

if __name__ == "__main__":
    # Vérifier les arguments
    if len(sys.argv) != 3:
        print("Usage : python3 analyse_supi_logs.py <fichier_log> <fichier_sortie>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    parse_logs(input_file, output_file)

