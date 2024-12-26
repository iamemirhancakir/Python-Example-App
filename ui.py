from database import DatabaseManager
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import DateEntry


class FinanceApp:
    def __init__(self, root):
        self.database = None
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.chart_canvas = FigureCanvasTkAgg(self.figure)
        self.create_home_page = None
        self.data_tree = None
        self.filter_category_combobox = None
        self.filter_date_entry = None
        self.date_entry = None
        self.category_combobox = None
        self.amount_entry = None
        self.root = root
        self.root.title("Kişisel Finans Takip Uygulaması")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        self.db = DatabaseManager()  # DatabaseManager ile bağlantı oluştur

        self.main_frame = tk.Frame(self.root)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.create_main_page()

    def create_main_page(self):
        self.clear_window()

        # Ana sayfa başlığı
        title = tk.Label(self.main_frame, text="Kişisel Finans Takip Uygulaması", font=("Arial", 16))
        title.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Gelir Ekle düğmesi
        income_button = tk.Button(self.main_frame, text="Gelir Ekle", width=20, command=self.income_page)
        income_button.grid(row=1, column=0, columnspan=2, pady=5)

        # Gider Ekle düğmesi
        expense_button = tk.Button(self.main_frame, text="Gider Ekle", width=20, command=self.expense_page)
        expense_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Raporlar düğmesi
        report_button = tk.Button(self.main_frame, text="Raporlar", width=20, command=self.report_page)
        report_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Ana sayfada analiz butonu ekleyelim
        analysis_button = tk.Button(self.main_frame, text="Gelir ve Gider Analizi", width=20, command=self.create_analysis_page)
        analysis_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Verileri Görüntüle düğmesi
        view_data_button = tk.Button(self.main_frame, text="Verileri Görüntüle", width=20, command=self.view_data_page)
        view_data_button.grid(row=5, column=0, columnspan=2, pady=5)

    def income_page(self):
        self.clear_window()

        title = tk.Label(self.main_frame, text="Gelir Ekle", font=("Arial", 16))
        title.grid(row=0, column=0, columnspan=2, pady=10, padx=20)

        # Tutar Girişi
        amount_label = tk.Label(self.main_frame, text="Tutar:")
        amount_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = tk.Entry(self.main_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        # Kategori Seçimi
        category_label = tk.Label(self.main_frame, text="Kategori:")
        category_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.category_combobox = ttk.Combobox(self.main_frame, values=["Maaş", "Yatırım", "Diğer"])
        self.category_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Tarih Girişi
        date_label = tk.Label(self.main_frame, text="Tarih:")
        date_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = DateEntry(
            self.main_frame,
            date_pattern="yyyy-mm-dd",
            state="normal",  # "readonly" yerine "normal" ile çalışmayı kolaylaştırabiliriz
            showweeknumbers=False  # Haftalık numaraları gizleyebiliriz
        )
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        # Kaydet ve Geri Düğmeleri
        save_button = tk.Button(self.main_frame, text="Kaydet", command=self.save_income)
        save_button.grid(row=4, column=0, pady=10, padx=5)
        back_button = tk.Button(self.main_frame, text="Geri", command=self.create_main_page)
        back_button.grid(row=4, column=1, pady=10, padx=5)

    def save_income(self):
        """Geliri veritabanına kaydet"""
        try:
            amount = float(self.amount_entry.get())
            category = self.category_combobox.get()
            date = self.date_entry.get_date().strftime("%Y-%m-%d")  # Tarihi string olarak al

            if not category or not date:
                raise ValueError("Lütfen tüm alanları doldurun!")

            self.db.add_income(amount, category, date)
            messagebox.showinfo("Başarılı", "Gelir kaydedildi!")
            self.create_main_page()

        except ValueError as e:
            messagebox.showerror("Hata", str(e))

    def expense_page(self):
        self.clear_window()

        title = tk.Label(self.main_frame, text="Gider Ekle", font=("Arial", 16))
        title.grid(row=0, column=0, columnspan=2, pady=10, padx=20)

        # Tutar Girişi
        amount_label = tk.Label(self.main_frame, text="Tutar:")
        amount_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = tk.Entry(self.main_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        # Kategori Seçimi
        category_label = tk.Label(self.main_frame, text="Kategori:")
        category_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.category_combobox = ttk.Combobox(self.main_frame, values=["Ulaşım", "Gıda", "Eğlence", "Diğer"])
        self.category_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Tarih Girişi
        date_label = tk.Label(self.main_frame, text="Tarih (YYYY-MM-DD):")
        date_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = DateEntry(
            self.main_frame,
            date_pattern="yyyy-mm-dd",
            state="normal",  # "readonly" yerine "normal" ile çalışmayı kolaylaştırabiliriz
            showweeknumbers=False  # Haftalık numaraları gizleyebiliriz
        )

        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        # Kaydet ve Geri Düğmeleri
        save_button = tk.Button(self.main_frame, text="Kaydet", command=self.save_expense)
        save_button.grid(row=4, column=0, pady=10, padx=5)
        back_button = tk.Button(self.main_frame, text="Geri", command=self.create_main_page)
        back_button.grid(row=4, column=1, pady=10, padx=5)

    def save_expense(self):
        """Gideri veritabanına kaydet"""
        try:
            amount = float(self.amount_entry.get())
            category = self.category_combobox.get()
            date = self.date_entry.get_date().strftime("%Y-%m-%d")  # Tarihi String olarak al

            if not category or not date:
                raise ValueError("Lütfen tüm alanları doldurun!")

            self.db.add_expense(amount, category, date)
            messagebox.showinfo("Başarılı", "Gider kaydedildi!")
            self.create_main_page()

        except ValueError as e:
            messagebox.showerror("Hata", str(e))

    def report_page(self):
        self.clear_window()

        # Başlık
        title = tk.Label(self.main_frame, text="Raporlar", font=("Arial", 16))
        title.grid(row=0, column=0, columnspan=2, pady=10, padx=20)

        # Toplam Gelir
        total_income = self.db.get_total_income()
        income_label = tk.Label(self.main_frame, text=f"Toplam Gelir: {total_income:.2f} TL", font=("Arial", 12))
        income_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Toplam Gider
        total_expense = self.db.get_total_expenses()
        expense_label = tk.Label(self.main_frame, text=f"Toplam Gider: {total_expense:.2f} TL", font=("Arial", 12))
        expense_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Gelir - Gider Farkı
        difference = total_income - total_expense
        difference_label = tk.Label(
            self.main_frame,
            text=f"Net Bakiye: {difference:.2f} TL",
            font=("Arial", 12),
            fg="green" if difference >= 0 else "red"
        )
        difference_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Geri Butonu
        back_button = tk.Button(self.main_frame, text="Geri", command=self.create_main_page)
        back_button.grid(row=4, column=0, columnspan=2, pady=10)

    def view_data_page(self):
        self.clear_window()

        # Başlık
        title = tk.Label(self.main_frame, text="Verileri Görüntüle", font=("Arial", 16))
        title.grid(row=0, column=0, columnspan=2, pady=10, padx=20)

        # Filtre Bölümü
        filter_frame = tk.Frame(self.main_frame)
        filter_frame.grid(row=1, column=0, columnspan=2, pady=10)

        tk.Label(filter_frame, text="Tarih (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(filter_frame)
        self.filter_date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Kategori:").grid(row=1, column=0, padx=5, pady=5)
        self.filter_category_combobox = ttk.Combobox(
            filter_frame,
            values=["Hepsi", "Maaş", "Yatırım", "Yemek", "Ulaşım", "Eğlence", "Diğer"]
        )
        self.filter_category_combobox.set("Hepsi")
        self.filter_category_combobox.grid(row=1, column=1, padx=5, pady=5)

        filter_button = tk.Button(filter_frame, text="Filtrele", command=self.filter_data)
        filter_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Tablo Başlıkları
        columns = ("Tür", "Tutar", "Kategori", "Tarih")
        self.data_tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10)
        self.data_tree.heading("Tür", text="Tür")
        self.data_tree.heading("Tutar", text="Tutar")
        self.data_tree.heading("Kategori", text="Kategori")
        self.data_tree.heading("Tarih", text="Tarih")
        self.data_tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.load_all_data()

        # Geri Butonu
        back_button = tk.Button(self.main_frame, text="Geri", command=self.create_main_page)
        back_button.grid(row=3, column=0, columnspan=2, pady=10)

    def filter_data(self):
        """Filtrelenmiş verileri tabloya yükler."""
        for row in self.data_tree.get_children():
            self.data_tree.delete(row)

        date_filter = self.filter_date_entry.get()
        category_filter = self.filter_category_combobox.get()

        if category_filter == "Hepsi":
            category_filter = None

        filtered_income = self.db.get_filtered_income(date_filter, category_filter)
        filtered_expenses = self.db.get_filtered_expenses(date_filter, category_filter)

        for income in filtered_income:
            self.data_tree.insert("", "end", values=("Gelir", income[1], income[2], income[3]))

        for expense in filtered_expenses:
            self.data_tree.insert("", "end", values=("Gider", expense[1], expense[2], expense[3]))

    def load_all_data(self):
        """Veritabanındaki tüm verileri tabloya yükler."""
        # Tabloyu temizle
        for row in self.data_tree.get_children():
            self.data_tree.delete(row)

        # Gelir verilerini yükle
        for income in self.db.get_all_income():
            self.data_tree.insert("", "end", values=("Gelir", income[1], income[2], income[3]))

        # Gider verilerini yükle
        for expense in self.db.get_all_expenses():
            self.data_tree.insert("", "end", values=("Gider", expense[1], expense[2], expense[3]))

    def create_analysis_page(self):
        self.clear_window()

        # Başlık
        title = tk.Label(self.main_frame, text="Gelir ve Gider Analizi", font=("Arial", 16))
        title.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Grafik alanı
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.chart_canvas = FigureCanvasTkAgg(self.figure, self.main_frame)
        self.chart_canvas.get_tk_widget().grid(row=1, column=0)

        # Analiz butonları
        monthly_button = tk.Button(self.main_frame, text="Aylık Gelir/Gider Grafiği", command=self.plot_monthly_data)
        monthly_button.grid(row=2, column=0,columnspan=2, pady=10, padx=5)
        category_button = tk.Button(self.main_frame, text="Kategorilere Göre Harcama", command=self.plot_category_data)
        category_button.grid(row=3, column=0, columnspan=2, pady=10, padx=5)
        back_button = tk.Button(self.main_frame, text="Geri", command=self.create_main_page)
        back_button.grid(row=4, column=0,columnspan=2, pady=10, padx=5)

    def plot_monthly_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        try:
            data = self.db.get_monthly_data()  # Ay bazında gelir/gider verilerini çek
            if not data:
                ax.text(0.5, 0.5, "Veri bulunamadı.", ha="center", va="center", transform=ax.transAxes)
                self.chart_canvas.draw()
                return

            months, incomes, expenses = zip(*data)

            ax.bar(months, incomes, label="Gelir", color="green")
            ax.bar(months, expenses, label="Gider", color="red", bottom=incomes)
            ax.set_title("Aylık Gelir ve Gider")
            ax.legend()
        except Exception as e:
            ax.text(0.5, 0.5, f"Hata: {str(e)}", ha="center", va="center", transform=ax.transAxes)

        self.chart_canvas.draw()

    def plot_category_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        try:
            data = self.db.get_category_data()  # Kategorilere göre gider verilerini çek
            if not data:
                ax.text(0.5, 0.5, "Veri bulunamadı.", ha="center", va="center", transform=ax.transAxes)
                self.chart_canvas.draw()
                return

            categories, amounts = zip(*data)

            ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
            ax.set_title("Kategorilere Göre Harcama")
        except Exception as e:
            ax.text(0.5, 0.5, f"Hata: {str(e)}", ha="center", va="center", transform=ax.transAxes)

        self.chart_canvas.draw()

    def clear_window(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def close_app(self):
        self.db.close()
        self.root.destroy()


