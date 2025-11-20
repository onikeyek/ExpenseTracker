import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Expenses"
    page.padding = 20
    page.scroll = "adaptive"
    
    # Expenses data
    expenses = []
    categories = ["Food", "Shopping", "Transport", "Utilities"]
    
    # Category colors for pie chart
    category_colors = {
        "Food": "orange400",
        "Shopping": "purple300",
        "Transport": "green300",
        "Utilities": "blue600"
    }

    
    # Pie chart
    pie_chart = ft.PieChart(
        sections=[],
        sections_space=2,
        center_space_radius=50,
        width=200,
        height=200,
    )

    # ***  CHART CONTAINER ***
    chart_container = ft.Container(
        content=pie_chart,
        width=350,      # adjust size as needed
        height=350,
        bgcolor="#1E1E1E",
        padding=20,
        border_radius=12,
    )
    
    # Legend
    legend_items = ft.Column(spacing=10)

    # Data table
    expense_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Date", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Amount", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Description", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.border.all(1, "grey300"),
        border_radius=10,
        horizontal_lines=ft.border.BorderSide(1, "grey200"),
    )

    # Recent expenses section
    recent_expenses_section = ft.Column(
        [
            ft.Text("Recent Expenses", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(content=expense_table, padding=10)
        ],
        spacing=10
    )

    # ---------- FUNCTIONS ----------
    
    def calculate_category_totals():
        totals = {cat: 0 for cat in categories}
        for expense in expenses:
            totals[expense["category"]] += expense["amount"]
        return totals
    
    def update_pie_chart():
        totals = calculate_category_totals()
        total_amount = sum(totals.values())
        
        if total_amount == 0:
            pie_chart.sections = []
            pie_chart.update()
            return
        
        sections = []
        for cat in categories:
            if totals[cat] > 0:
                percentage = (totals[cat] / total_amount) * 100
                sections.append(
                    ft.PieChartSection(
                        value=totals[cat],
                        title=f"{percentage:.0f}%",
                        color=category_colors[cat],
                        radius=100,
                    )
                )
        
        pie_chart.sections = sections
        pie_chart.update()
    
    def update_expense_table():
        expense_table.rows.clear()
        
        for exp in reversed(expenses):
            expense_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(exp["date"])),
                        ft.DataCell(ft.Text(exp["category"])),
                        ft.DataCell(ft.Text(f"${exp['amount']:.2f}")),
                        ft.DataCell(ft.Text(exp["description"])),
                    ]
                )
            )
        
        expense_table.update()
        recent_expenses_section.update()

    def update_legend():
        totals = calculate_category_totals()
        legend_items.controls.clear()

        for cat in categories:
            if totals[cat] > 0:
                legend_items.controls.append(
                    ft.Row(
                        [
                            ft.Container(
                                width=20,
                                height=20,
                                bgcolor=category_colors[cat],
                                border_radius=4,
                            ),
                            ft.Text(
                                cat,
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color="white",
                            )
                        ],
                        spacing=8
                    )
                )

        legend_items.update()

    
    def add_expense_click(e):
        if not amount_field.value or float(amount_field.value or 0) <= 0:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid amount"))
            page.snack_bar.open = True
            page.update()
            return
        
        expense = {
            "date": datetime.now().strftime("%b %d, %Y"),
            "category": category_dropdown.value,
            "amount": float(amount_field.value),
            "description": description_field.value or ""
        }
        
        expenses.append(expense)
        
        # Clear form
        amount_field.value = "0.00"
        description_field.value = ""
        
        # Update UI
        update_expense_table()
        update_pie_chart()
        update_legend()
        
        page.update()

    # ---------- INPUT FIELDS ----------
    
    category_dropdown = ft.Dropdown(
        label="Category",
        value="Food",
        options=[ft.dropdown.Option(cat) for cat in categories],
        width=300,
        filled=True,
    )
    
    amount_field = ft.TextField(
        label="Amount",
        value="0.00",
        prefix_text="$ ",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        filled=True,
    )
    
    description_field = ft.TextField(
        label="Description",
        hint_text="e.g., Lunch with colleagues",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=300,
        filled=True,
    )
    
    add_button = ft.ElevatedButton(
        "Add Expense",
        on_click=add_expense_click,
        width=300,
        height=50,
        bgcolor="blue700",
        color="white",
    )

    # ---------- PAGE LAYOUT ----------
    
    page.add(
        ft.Row(
            [
                # Left panel
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Add New Expense", size=24, weight=ft.FontWeight.BOLD),
                            ft.Container(height=20),
                            category_dropdown,
                            amount_field,
                            ft.Text("Description", size=14, color="grey700"),
                            ft.Text("(Optional)", size=12, color="grey500"),
                            description_field,
                            ft.Container(height=20),
                            add_button,
                        ],
                        spacing=10,
                    ),
                    padding=20,
                    width=350,
                ),

                # Right panel
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Spending Overview", size=24, weight=ft.FontWeight.BOLD),
                            
                            # Overview box
                            ft.Container(
                                content=ft.Row(
                                    [
                                        chart_container,    # *** UPDATED HERE ***
                                        ft.Container(width=20),
                                        legend_items,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                padding=20,
                                border=ft.border.all(1, "grey300"),
                                border_radius=10,
                                bgcolor="#1E1E1E",
                            ),

                            ft.Container(height=20),
                            recent_expenses_section,
                        ],
                        spacing=10,
                    ),
                    padding=20,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=20,
        )
    )

ft.app(target=main)
