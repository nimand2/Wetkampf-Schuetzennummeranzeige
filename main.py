import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os


class ShooterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shooter Information")

        self.shooter_data = []
        self.shooter_number = 3000

        self.entries = []
        for i in range(8):
            tk.Label(root, text=f"Vorname {i + 1}:").grid(
                row=i, column=0, padx=5, pady=5
            )
            tk.Label(root, text=f"Nachname {i + 1}:").grid(
                row=i, column=2, padx=5, pady=5
            )

            first_name_entry = tk.Entry(root)
            first_name_entry.grid(row=i, column=1, padx=5, pady=5)
            last_name_entry = tk.Entry(root)
            last_name_entry.grid(row=i, column=3, padx=5, pady=5)

            self.entries.append((first_name_entry, last_name_entry))

        self.export_button = tk.Button(
            root, text="Export to CSV", command=self.export_to_csv
        )
        self.export_button.grid(row=9, column=0, columnspan=4, pady=10)

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
            messagebox.showinfo("Success", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ShooterApp(root)
    root.mainloop()
