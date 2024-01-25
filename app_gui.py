import sys
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

        self.btn_upload = QPushButton('Upload PDF', self)
        self.btn_upload.clicked.connect(self.upload_pdf)
        layout.addWidget(self.btn_upload)

        self.setLayout(layout)

    def upload_pdf(self):
        pdf_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "PDF files (*.pdf)")
        if pdf_path:
            try:
                csv_path = process_pdf_file(pdf_path)
                QMessageBox.information(self, "Success", f"CSV file has been created: {csv_path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

def main():
    app = QApplication(sys.argv)
    ex = PDFtoCSVConverter()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
