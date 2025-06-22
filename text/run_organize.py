import os
from utils import WikipediaProcessor

class Organizer:
    def __init__(self):
        self.wikipedia_processor = WikipediaProcessor()

    def option_4_wikipedia_extraction(self):
        """Option 4: Wikipedia-Wissen-Extraktion."""
        print("\n[WIKIPEDIA-WISSEN-EXTRAKTION]")
        print("Extrahiert Wissen aus Wikipedia-Dumps für Zettelkasten-Integration.")
        print("-"*60)
        
        # Wikipedia-Dump-Pfad
        default_paths = ["databases/wikipedia/b3wiki", "databases/wikipedia/wikipedia_dumps"]
        dump_path = input(f"Pfad zu Wikipedia-Dump (Enter für Standard: {default_paths[0]}): ").strip()
        if not dump_path:
            # Auto-detect
            for path in default_paths:
                if os.path.exists(path):
                    dump_path = path
                    print(f"Verwende gefundenen Dump-Pfad: {dump_path}")
                    break
            else:
                print(f"Kein Standard-Wikipedia-Dump-Ordner gefunden. Bitte gib einen Pfad an.")
                dump_path = input("Pfad zu Wikipedia-Dump: ").strip()
                if not dump_path or not os.path.exists(dump_path):
                    print("Abbruch: Kein gültiger Dump-Pfad angegeben.")
                    return
        elif not os.path.exists(dump_path):
            print(f"Wikipedia-Dump-Pfad '{dump_path}' existiert nicht.")
            create_dump = input("Soll der Pfad erstellt werden? (j/n): ").strip().lower()
            if create_dump == 'j':
                os.makedirs(dump_path, exist_ok=True)
                print(f"Pfad '{dump_path}' erstellt.")
            else:
                return
        
        # Extraktionsparameter
        topic = input("Thema für Extraktion (oder Enter für allgemeine Extraktion): ").strip()
        max_articles = input("Maximale Anzahl Artikel (Standard: 100): ").strip()
        max_articles = int(max_articles) if max_articles.isdigit() else 100
        
        print(f"\nStarte Wikipedia-Extraktion...")
        print(f"Thema: {topic if topic else 'Allgemein'}")
        print(f"Max. Artikel: {max_articles}")
        
        # Use a user-writable output directory
        output_path = "databases/wikipedia/extracted"
        extraction_params = {
            "dump_path": dump_path,
            "topic": topic,
            "max_articles": max_articles,
            "output_path": output_path
        }
        
        while True:
            try:
                result = self.wikipedia_processor.process_wikipedia_dump(
                    dump_path, output_dir=output_path
                )
                if "error" not in result:
                    print(f"\n[OK] Extraktion erfolgreich!")
                    print(f"Artikel extrahiert: {result.get('total_articles', 0)}")
                    print(f"Ausgabepfad: {result.get('output_directory', '')}")
                    break
                else:
                    print(f"\n[ERROR] Extraktionsfehler: {result['error']}")
                    if 'Permission denied' in result['error']:
                        print("Sie haben keine Berechtigung für das gewählte Verzeichnis.")
                        output_path = input("Bitte geben Sie einen anderen Ausgabepfad an (z.B. 'databases/wikipedia/extracted'): ").strip()
                        if not output_path:
                            print("Abbruch: Kein gültiger Ausgabepfad angegeben.")
                            return
                    else:
                        break
            except Exception as e:
                print(f"\n[ERROR] Fehler bei der Extraktion: {e}")
                break
        input("\nDrücke Enter zum Fortfahren...") 