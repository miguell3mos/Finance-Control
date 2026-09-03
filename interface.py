from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox
)

import banco
from datetime import datetime

banco.criar_tabela()

app = QApplication([])

janela = QWidget()
janela.setWindowTitle("Finance Control")
janela.resize(800,500)

titulo = QLabel("Finance Control")
label_saldo = QLabel("Saldo: R$ 0.00")

botao_registrar = QPushButton("Registrar Transação")
botao_consultar = QPushButton("Consultar Transações")

def abrir_registro():
    janela_registro = QDialog(janela)
    janela_registro.setWindowTitle("Registrar Transação")
    janela_registro.resize(400,300)

    layout_registro = QVBoxLayout()

    tipo = QComboBox()
    tipo.addItems(["Despesa", "Receita"])

    descricao = QLineEdit()
    descricao.setPlaceholderText("Descrição")

    valor = QDoubleSpinBox()
    valor.setMaximum(999999999999)
    valor.setDecimals(2)
    valor.setPrefix("R$ ")

    categoria = QComboBox()
    categoria.addItems([
        "Alimentação",
        "Transporte",
        "Lazer",
        "Estudos",
        "Salário",
        "Outros"
    ])

    botao_salvar = QPushButton("Salvar")

    def salvar():
        transacao = {
            "Tipo": tipo.currentText().lower(),
            "Descrição": descricao.text().strip(),
            "Valor": valor.value(),
            "Categoria": categoria.currentText().lower(),
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        banco.salvar_transacao(transacao)

        novo_saldo = banco.calcular_saldo()
        label_saldo.setText(f"Saldo: R${novo_saldo:.2f}")

        janela_registro.accept()

    botao_salvar.clicked.connect(salvar)

    layout_registro.addWidget(QLabel("Tipo"))
    layout_registro.addWidget(tipo)

    layout_registro.addWidget(QLabel("Descrição"))
    layout_registro.addWidget(descricao)

    layout_registro.addWidget(QLabel("Valor"))
    layout_registro.addWidget(valor)

    layout_registro.addWidget(QLabel("Categoria"))
    layout_registro.addWidget(categoria)

    layout_registro.addWidget(botao_salvar)

    janela_registro.setLayout(layout_registro)

    janela_registro.exec()

botao_registrar.clicked.connect(abrir_registro)


layout = QVBoxLayout()

layout.addWidget(titulo)
layout.addWidget(label_saldo)
layout.addWidget(botao_registrar)
layout.addWidget(botao_consultar)

janela.setLayout(layout)

janela.show()
app.exec()