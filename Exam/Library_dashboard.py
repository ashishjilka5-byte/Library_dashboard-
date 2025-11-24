import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class LibraryDashboard:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        try:
            df = pd.read_csv(self.file_path)
            print(df.head())  # <-- add this line
            df.dropna(inplace=True)
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            self.data = df
            print(" Data loaded successfully!")
        except Exception as e:
            print(" Error:", e)


    def calculate_statistics(self):
        print("\n LIBRARY STATISTICS:")

        most_borrowed = self.data["Book Title"].value_counts().idxmax()
        avg_duration = self.data["Borrowing Duration (Days)"].mean()
        busiest_day = self.data["Date"].dt.day_name().value_counts().idxmax()

        print(f"Most Borrowed Book: {most_borrowed}")
        print(f"Average Borrow Duration: {avg_duration:.2f} days")
        print(f"Busiest Day: {busiest_day}")

    def filter_transactions(self, column, value):
        filtered = self.data[self.data[column] == value]
        print(f"\nFiltered transactions for {column} = {value}")
        print(filtered)
        return filtered


    def generate_report(self):
        print("\n SUMMARY REPORT")
        print(self.data.describe(include='all'))


    def visualize(self):
        print("\n Generating charts...")

        # Bar Chart – Top 5 Books
        top_books = self.data["Book Title"].value_counts().head(5)
        plt.figure(figsize=(8, 5))
        top_books.plot(kind="bar", color='skyblue', edgecolor='black')
        plt.title("Top 5 Borrowed Books")
        plt.xlabel("Books")
        plt.ylabel("Number of Borrowings")
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()  # adjust layout to prevent label cutoff
        plt.show()


        # Line Graph – Borrowing Trend by Month
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.data["Month"] = self.data["Date"].dt.month
        monthly_counts = self.data.groupby("Month")["Transaction ID"].count()
        monthly_counts.plot(kind="line", marker='o')  # marker makes points visible
        plt.title("Borrowing Trend Over Months")
        plt.xlabel("Month")
        plt.ylabel("Transactions")
        plt.xticks(range(1, 13))
        plt.grid(True)
        plt.show()

        # Pie Chart – Books by Genre
        genre_counts = self.data["Genre"].value_counts()
        plt.figure(figsize=(7, 7))
        plt.pie(genre_counts,
                labels=genre_counts.index,
                autopct="%1.1f%%",
                startangle=140,
                shadow=True)
        plt.title("Books Borrowed by Genre")
        plt.axis("equal")  
        plt.show()

        # Heatmap –  Day & Hour
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.data["Day"] = self.data["Date"].dt.day_name()
        self.data["Hour"] = self.data.get("Hour", 0)
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        pivot = self.data.pivot_table(index="Day", columns="Hour",
                                      values="Transaction ID",
                                      aggfunc="count",
                                      fill_value=0)
        pivot = pivot.reindex(days_order)

        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot, cmap="Blues", linewidths=0.5, annot=True, fmt="d")
        plt.title("Borrowing Heatmap (Day vs Hour)")
        plt.xlabel("Hour")
        plt.ylabel("Day")
        plt.show()


# MAIN PROGRAM

if __name__ == "__main__":
    dashboard = LibraryDashboard("Library_transactions.csv")

    dashboard.load_data()
    dashboard.calculate_statistics()
    dashboard.filter_transactions("Genre", "Fiction")  # Example filter
    dashboard.generate_report()
    dashboard.visualize()