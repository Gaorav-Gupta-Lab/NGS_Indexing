from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

# from main import generate_indices


class IndexGeneratorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NGS Index Generator")
        self.resize(760, 440)
        self.setMinimumSize(560, 320)
        self.indices = []

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Index kit:"))
        self.kit_box = QComboBox()
        self.kit_box.addItems(["trueseq", "udp"])
        controls.addWidget(self.kit_box)

        controls.addWidget(QLabel("Number of libraries:"))
        self.count_box = QSpinBox()
        self.count_box.setRange(1, 100)
        self.count_box.setValue(5)
        controls.addWidget(self.count_box)

        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.generate)
        controls.addWidget(generate_button)
        controls.addStretch(1)
        layout.addLayout(controls)

        self.results = QTableWidget(0, 2)
        self.results.setHorizontalHeaderLabels(["Index ID", "Manifest Sequence"])
        self.results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results.setSelectionBehavior(QTableWidget.SelectRows)
        self.results.setAlternatingRowColors(True)
        layout.addWidget(self.results)

        actions = QHBoxLayout()
        copy_button = QPushButton("Copy TSV")
        copy_button.clicked.connect(self.copy_tsv)
        actions.addWidget(copy_button)
        save_button = QPushButton("Save TSV…")
        save_button.clicked.connect(self.save_tsv)
        actions.addWidget(save_button)
        actions.addStretch(1)
        layout.addLayout(actions)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Choose a kit and generate index pairs.")

    def generate(self):
        try:
            indices = generate_indices(self.kit_box.currentText(), self.count_box.value())
        except ValueError as error:
            QMessageBox.critical(self, "Invalid library count", str(error))
            return

        self.indices = indices
        self.results.setRowCount(len(indices))
        for row, (index_id, manifest_sequence) in enumerate(indices):
            id_item = QTableWidgetItem(index_id)
            seq_item = QTableWidgetItem(manifest_sequence)
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            seq_item.setFlags(seq_item.flags() & ~Qt.ItemIsEditable)
            self.results.setItem(row, 0, id_item)
            self.results.setItem(row, 1, seq_item)
        self.status.showMessage("Generated {} index pairs.".format(len(indices)))

    def _tsv_text(self):
        lines = ["Index ID\tManifest Sequence"]
        lines.extend("{}\t{}".format(index_id, sequence) for index_id, sequence in self.indices)
        return "\n".join(lines) + "\n"

    def copy_tsv(self):
        if not self.indices:
            QMessageBox.information(self, "No results", "Generate index pairs before copying.")
            return
        QGuiApplication.clipboard().setText(self._tsv_text())
        self.status.showMessage("Copied results as TSV.")

    def save_tsv(self):
        if not self.indices:
            QMessageBox.information(self, "No results", "Generate index pairs before saving.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save index pairs",
            "",
            "Tab-separated values (*.tsv);;All files (*.*)",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8", newline="") as output_file:
                output_file.write(self._tsv_text())
        except OSError as error:
            QMessageBox.critical(self, "Save failed", str(error))
            return
        self.status.showMessage("Saved {} index pairs.".format(len(self.indices)))


def main():
    app = QApplication([])
    window = IndexGeneratorWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
