import tkinter as tk
from tkinter import filedialog, messagebox
import csv


class ShooterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shooter Information")
        self.shooter_data = []
        self.shooter_number = 3000
        self.entries = []

        # Frame für Scrollbar und Eingabefelder
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        # Canvas für die Scrollbar und dynamische Anpassung
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = tk.Scrollbar(
            self.frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: [
                self.canvas.configure(scrollregion=self.canvas.bbox("all")),
                self.adjust_window_size(),
            ],
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Label und Eingabefeld für die Anzahl der Personen
        tk.Label(root, text="Anzahl der Personen:").pack(padx=5, pady=5)
        self.person_count_entry = tk.Entry(root)
        self.person_count_entry.pack(padx=5, pady=5)

        self.create_entries_button = tk.Button(
            root, text="Eingabefelder erstellen", command=self.create_entries
        )
        self.create_entries_button.pack(padx=5, pady=5)

        # Button zum Exportieren in CSV
        self.export_button = tk.Button(
            root, text="Export to CSV", command=self.export_to_csv
        )
        self.export_button.pack(pady=10)

    def create_entries(self):
        # Löschen der vorherigen Eingabefelder
        for entry in self.entries:
            entry[0].destroy()
            entry[1].destroy()
        self.entries.clear()

        # Anzahl der Personen aus dem Eingabefeld lesen
        try:
            count = int(self.person_count_entry.get())
            for i in range(count):
                tk.Label(self.scrollable_frame, text=f"Vorname {i + 1}:").grid(
                    row=i, column=0, padx=5, pady=5
                )
                tk.Label(self.scrollable_frame, text=f"Nachname {i + 1}:").grid(
                    row=i, column=2, padx=5, pady=5
                )
                first_name_entry = tk.Entry(self.scrollable_frame)
                first_name_entry.grid(row=i, column=1, padx=5, pady=5)
                last_name_entry = tk.Entry(self.scrollable_frame)
                last_name_entry.grid(row=i, column=3, padx=5, pady=5)
                self.entries.append((first_name_entry, last_name_entry))
            self.adjust_window_size()
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Anzahl ein.")

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return
        try:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                for first_name_entry, last_name_entry in self.entries:
                    first_name = first_name_entry.get().strip()
                    last_name = last_name_entry.get().strip()
                    if first_name and last_name:
                        shooter_id = self.shooter_number
                        short_name = f"{first_name[0]}. {last_name}"
                        writer.writerow(
                            [shooter_id, last_name, first_name, short_name]
                            + ["" for _ in range(6)]
                        )
                        self.shooter_number += 1
            messagebox.showinfo("Erfolg", "Daten erfolgreich exportiert!")
        except Exception as e:
            messagebox.showerror(
                "Fehler", f"Fehler beim Exportieren der Daten: {str(e)}"
            )

    def adjust_window_size(self):
        self.root.update_idletasks()  # Aktualisiert das Layout, um die neue Größe zu berechnen
        self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ShooterApp(root)
    root.mainloop()
