from fpdf import FPDF
from datetime import datetime
from pathlib import Path


class BookingInvoice(FPDF):
    def __init__(self, hotel_name, hotel_address, room_no,
                 customer_name, customer_aadhar, customer_phone, customer_age,
                 booked_from, booked_to, customer_email,
                 rooms, total_amount,  app_name, app_logo_path, booking_id):
        super().__init__()
        self.hotel_name = hotel_name
        self.hotel_address = hotel_address
        self.room_no = room_no
        self.customer_name = customer_name
        self.customer_aadhar = customer_aadhar
        self.customer_phone = customer_phone
        self.customer_age = customer_age
        self.booked_from = booked_from
        self.booked_to = booked_to
        self.customer_email = customer_email
        self.rooms = rooms
        self.total_amount = total_amount
        self.app_name = app_name
        self.app_logo_path = app_logo_path
        self.booking_id = booking_id

        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.create_invoice()
        self.downloads_folder = Path.home() / "Downloads"
        self.pdf_path = self.downloads_folder / f"{self.booking_id}.pdf"

    def header(self):
        if self.app_logo_path:
            self.image(self.app_logo_path, 10, 8, 25)  # x, y, width
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, self.hotel_name, ln=True, align="C")
        self.set_font("Arial", "", 12)
        self.cell(0, 5, self.hotel_address, ln=True, align="C")
        self.ln(10)
        # App Name
        self.set_font("Arial", "I", 10)
        self.cell(0, 5, f"Booked via {self.app_name}", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def create_invoice(self):
        # Invoice Info
        self.set_font("Arial", "B", 12)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 10, f"Booking No: {self.booking_id}", ln=True, fill=True)
        self.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, fill=True)
        self.ln(5)

        # Customer Info
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Customer Details:", ln=True)
        self.set_font("Arial", "", 12)
        self.cell(0, 8, f"Name: {self.customer_name}", ln=True)
        self.cell(0, 8, f"Aadhar Card: {self.customer_aadhar}", ln=True)
        self.cell(0, 8, f"Phone: {self.customer_phone}", ln=True)
        self.cell(0, 8, f"Email: {self.customer_email}", ln=True)
        self.cell(0, 8, f"Age: {self.customer_age}", ln=True)
        self.cell(0, 8, f"Booking Period: {self.booked_from} to {self.booked_to}", ln=True)
        self.ln(5)

        # Hotel Info
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Hotel / Room Info:", ln=True)
        self.set_font("Arial", "", 12)
        self.cell(0, 8, f"Room No.: {self.room_no}", ln=True)
        self.ln(5)

        # Rooms Table Header
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 200, 200)
        self.cell(60, 10, "Room Type", 1, 0, "C", fill=True)
        self.cell(30, 10, "Qty", 1, 0, "C", fill=True)
        self.cell(40, 10, "Price/Room", 1, 0, "C", fill=True)
        self.cell(40, 10, "Total", 1, 1, "C", fill=True)

        # Rooms Table Data
        self.set_font("Arial", "", 12)
        for room in self.rooms:
            total_price = room['qty'] * room['price']
            self.cell(60, 10, room['type'], 1)
            self.cell(30, 10, str(room['qty']), 1, 0, "C")
            self.cell(40, 10, f"{room['price']:.2f}", 1, 0, "C")
            self.cell(40, 10, f"{total_price:.2f}", 1, 1, "C")

        # Total Amount
        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.set_fill_color(220, 220, 220)
        self.cell(130, 10, "Total Amount", 1, 0, "C", fill=True)
        self.cell(40, 10, f"{self.total_amount:.2f}", 1, 1, "C", fill=True)

        # Thank You Note
        self.ln(20)
        self.set_font("Arial", "I", 12)
        self.cell(0, 10, "Thank you for your booking!", ln=True, align="C")


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    invoice = BookingInvoice(
        hotel_name="Sunrise Hotel",
        hotel_address="123 Beach Road, Mumbai",
        room_no="101",
        customer_name="John Doe",
        customer_aadhar="1234-5678-9012",
        customer_phone="9876543210",
        customer_age=30,
        booked_from="2025-10-01",
        booked_to="2025-10-05",
        customer_email="john@example.com",
        rooms="rooms",
        total_amount="total_amount",
        invoice_no="INV-001",
        app_name="EasyStay",
        app_logo_path="Icons/Hotel.svg"
    )


import os
from fpdf import FPDF

# Get the Downloads folder of the current user


# Create instance of FPDF class
pdf = FPDF()
pdf.add_page()

# Set font
pdf.set_font("Arial", "B", 24)
pdf.cell(0, 20, "Dummy PDF File", ln=True, align="C")

pdf.set_font("Arial", "", 14)
pdf.ln(10)  # Line break
pdf.multi_cell(0, 10, "This is a dummy PDF generated for testing purposes.\nYou can add more text, images, or tables here.")

# Save the PDF
pdf.output(str(pdf_path))

print(f"PDF generated successfully at: {pdf_path}")


