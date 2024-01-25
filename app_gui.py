import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from pdf_processing import process_pdf_file

class PDFtoCSVConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF to CSV Converter')
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.btn_upload = QPushButton('Upload PDFs', self)
        self.btn_upload.clicked.connect(self.upload_pdfs)
        layout.addWidget(self.btn_upload)

        self.setLayout(layout)

    def upload_pdfs(self):
        try:
            pdf_paths, _ = QFileDialog.getOpenFileNames(self, 'Open files', '', "PDF files (*.pdf)")
            if not pdf_paths:
                return  # No PDFs selected

            csv_path, _ = QFileDialog.getOpenFileName(self, 'Open CSV file', '', "CSV files (*.csv)")
            if not csv_path:
                return  # No CSV file selected

            with open(csv_path, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for pdf_path in pdf_paths:
                    try:
                        data = process_pdf_file(pdf_path)
                        for number in data["Phone Numbers"]:
                            writer.writerow([data["Name"], data["DOB"], number, data["Source Name"]])
                    except Exception as e:
                        QMessageBox.warning(self, "Processing Error", f"Error processing {pdf_path}: {e}")
                        continue  # Continue processing the next PDF
            QMessageBox.information(self, "Success", "Data from all PDFs has been appended to the CSV file.")
        except FileNotFoundError:
            QMessageBox.warning(self, "File Error", "The specified CSV file could not be opened.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")



def main():
    app = QApplication(sys.argv)
    ex = PDFtoCSVConverter()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

