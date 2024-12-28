import matplotlib

from database import DatabaseManager
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import DateEntry
matplotlib.use("TkAgg")


class FinanceApp:
    def __init__(self, root):
        self.start_date_entry = None
        self.end_date_entry = None
        self.filtered_category_data = None
        self.filtered_monthly_data = None
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

        # Gelir, Gider ve Bakiye Özeti
        summary_frame = tk.Frame(self.main_frame, bg="lightblue", relief="solid", bd=2)
        summary_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        total_income = self.db.get_total_income()  # Toplam gelir
        total_expense = self.db.get_total_expenses()  # Toplam gider
        balance = total_income - total_expense  # Bakiye

        income_label = tk.Label(summary_frame, text=f"Gelir: {total_income:.2f} TL", bg="lightgreen",
                                font=("Arial", 12))
        income_label.grid(row=0, column=0, padx=10, pady=5)

        expense_label = tk.Label(summary_frame, text=f"Gider: {total_expense:.2f} TL", bg="salmon", font=("Arial", 12))
        expense_label.grid(row=0, column=1, padx=10, pady=5)

        balance_label = tk.Label(summary_frame, text=f"Bakiye: {balance:.2f} TL", bg="white", font=("Arial", 12))
        balance_label.grid(row=0, column=2, padx=10, pady=5)

        # Gelir Ekle düğmesi
        income_button = tk.Button(self.main_frame, text="Gelir Ekle", command=self.income_page, width=20)
        income_button.grid(row=2, column=0, pady=10, padx=10)

        # Gider Ekle düğmesi
        expense_button = tk.Button(self.main_frame, text="Gider Ekle", command=self.expense_page, width=20)
        expense_button.grid(row=2, column=1, pady=10, padx=10)

        # Analiz butonu
        analysis_button = tk.Button(self.main_frame, text="Gelir ve Gider Analizi", width=20, command=self.create_analysis_page)
        analysis_button.grid(row=3, column=0, pady=10, padx=10)

        # Verileri Görüntüle düğmesi
        view_data_button = tk.Button(self.main_frame, text="Verileri Görüntüle", command=self.view_data_page, width=20)
        view_data_button.grid(row=3, column=1, pady=10, padx=10)

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

    def view_data_page(self):
        self.clear_window()

        # Başlık
        title = tk.Label(self.main_frame, text="Verileri Görüntüle", font=("Arial", 16))
        title.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

        # Filtre Bölümü
        filter_frame = tk.Frame(self.main_frame)
        filter_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Tarih Girişi
        date_label = tk.Label(filter_frame, text="Tarih (YYYY-MM-DD):")
        date_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = DateEntry(
            filter_frame,
            date_pattern="yyyy-mm-dd",
            state="normal",
            showweeknumbers=False
        )
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Kategori Seçimi
        category_label = tk.Label(filter_frame, text="Kategori:")
        category_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.filter_category_combobox = ttk.Combobox(
            filter_frame,
            values=["Hepsi", "Maaş", "Yatırım", "Yemek", "Ulaşım", "Eğlence", "Diğer"]
        )
        self.filter_category_combobox.set("Hepsi")
        self.filter_category_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Filtreleme Butonu
        filter_button = tk.Button(filter_frame, text="Filtrele", command=self.filter_data)
        filter_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Tablo Başlıkları
        data_frame = tk.Frame(self.main_frame)
        data_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        columns = ("Tür", "Tutar", "Kategori", "Tarih")
        self.data_tree = ttk.Treeview(data_frame, columns=columns, show="headings", height=10)
        self.data_tree.heading("Tür", text="Tür")
        self.data_tree.heading("Tutar", text="Tutar")
        self.data_tree.heading("Kategori", text="Kategori")
        self.data_tree.heading("Tarih", text="Tarih")
        self.data_tree.pack(fill="both", expand=True)

        # Tablo Verilerini Yükle
        self.load_all_data()

        # Geri Butonu
        back_button = tk.Button(self.main_frame, text="Geri", command=self.create_main_page)
        back_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

    def filter_data(self):
        """Filtrelenmiş verileri tabloya yükler."""
        for row in self.data_tree.get_children():
            self.data_tree.delete(row)

        date = self.date_entry.get_date().strftime("%Y-%m-%d")  # Tarihi String olarak al
        category_filter = self.filter_category_combobox.get()

        if category_filter == "Hepsi":
            category_filter = None

        filtered_income = self.db.get_filtered_income(date, category_filter)
        filtered_expenses = self.db.get_filtered_expenses(date, category_filter)

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
        title = tk.Label(self.main_frame, text="Gelir ve Gider Analizi", font=("Helvetica", 16))
        title.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Tarih Aralığı Seçimi
        filter_frame = tk.Frame(self.main_frame)
        filter_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        tk.Label(filter_frame, text="Başlangıç Tarihi:").grid(row=0, column=0, padx=5, pady=5)
        self.start_date_entry = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Bitiş Tarihi:").grid(row=1, column=0, padx=5, pady=5)
        self.end_date_entry = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
        self.end_date_entry.grid(row=1, column=1, padx=5, pady=5)

        filter_button = tk.Button(filter_frame, text="Filtrele", command=self.filter_analysis_data)
        filter_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Grafik Alanı
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.chart_canvas = FigureCanvasTkAgg(self.figure, self.main_frame)
        self.chart_canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)

        # Analiz Butonları
        monthly_button = tk.Button(self.main_frame, text="Aylık Gelir/Gider Grafiği", command=self.plot_monthly_data)
        monthly_button.grid(row=3, column=0, columnspan=2, pady=10, padx=5)

        category_button = tk.Button(self.main_frame, text="Kategorilere Göre Harcama", command=self.plot_category_data)
        category_button.grid(row=4, column=0, columnspan=2, pady=10, padx=5)

        back_button = tk.Button(self.main_frame, text="Geri", command=self.create_main_page)
        back_button.grid(row=5, column=0, columnspan=2, pady=10, padx=5)

    def filter_analysis_data(self):
        """Tarih aralığına göre analiz verilerini filtrele."""
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d")

        try:
            self.filtered_monthly_data = self.db.get_filtered_monthly_data(start_date, end_date)
            self.filtered_category_data = self.db.get_filtered_category_data(start_date, end_date)
            messagebox.showinfo("Başarılı", "Analiz verileri filtrelendi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Veri filtreleme başarısız: {str(e)}")

    def plot_monthly_data(self):
        """Aylık gelir ve gider karşılaştırmasını çubuk grafikte göster."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        data = self.filtered_monthly_data if hasattr(self, "filtered_monthly_data") else self.db.get_monthly_data()
        if not data:
            ax.text(0.5, 0.5, "Veri bulunamadı.", ha="center", va="center", transform=ax.transAxes)
        else:
            months = [item[0] for item in data]
            incomes = [item[1] for item in data if item[2] == 'Gelir']  # Sadece gelirleri al
            expenses = [item[1] for item in data if item[2] == 'Gider']  # Sadece giderleri al

            # Aynı aya ait gelir ve giderleri ayırmak için yeni kod eklendi.
            month_income = {}
            month_expense = {}
            for month, amount, Type in data:
                if Type == 'Gelir':
                    month_income[month] = month_income.get(month, 0) + amount
                elif Type == 'Gider':
                    month_expense[month] = month_expense.get(month, 0) + amount
            months = list(set(month_income.keys()) | set(month_expense.keys()))
            incomes = [month_income.get(month, 0) for month in months]
            expenses = [month_expense.get(month, 0) for month in months]
            months = sorted(months)
            # Grafik Çizdirme
            ax.bar(months, incomes, label="Gelir", color="green", alpha=0.7)
            ax.bar(months, expenses, label="Gider", color="red", alpha=0.7, bottom=incomes)

            ax.set_title("Aylık Gelir ve Gider Karşılaştırması")
            ax.legend()

        self.chart_canvas.draw()

    def plot_category_data(self):
        """Kategoriye göre harcama dağılımını pasta grafikte göster."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        data = self.filtered_category_data if hasattr(self, "filtered_category_data") else self.db.get_category_data()
        if not data:
            ax.text(0.5, 0.5, "Veri bulunamadı.", ha="center", va="center", transform=ax.transAxes)
        else:
            categories = [item[0] for item in data]
            amounts = [item[1] for item in data]
            # ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140) #pie chart çizimi için tek satır
            plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
            plt.title("Kategoriye Göre Harcama Dağılımı")
            plt.show()

        self.chart_canvas.draw()

    def clear_window(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def close_app(self):
        self.db.close()
        self.root.destroy()


