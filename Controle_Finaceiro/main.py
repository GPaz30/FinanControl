import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database as db

# ── Paleta de cores ──────────────────────────────────────────────────────────
BG          = "#0f1117"
SURFACE     = "#1a1d27"
SURFACE2    = "#22263a"
BORDER      = "#2e3250"
ACCENT      = "#4f8ef7"
ACCENT2     = "#7c5cfc"
GREEN       = "#2ecc71"
RED         = "#e74c3c"
TEXT        = "#e8eaf6"
SUBTEXT     = "#8892b0"
WHITE       = "#ffffff"

FONT_TITLE  = ("Georgia", 22, "bold")
FONT_LABEL  = ("Courier New", 10, "bold")
FONT_ENTRY  = ("Courier New", 11)
FONT_BTN    = ("Courier New", 10, "bold")
FONT_TABLE  = ("Courier New", 10)
FONT_RESUME = ("Courier New", 12, "bold")


# ── Helpers ──────────────────────────────────────────────────────────────────
def fmt_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def hoje() -> str:
    return datetime.now().strftime("%d/%m/%Y")


# ── Aplicação principal ──────────────────────────────────────────────────────
class FinanControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        db.criar_tabela()

        self.title("FinanControl")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.resizable(True, True)

        # variáveis de formulário
        self.var_tipo      = tk.StringVar(value="Receita")
        self.var_descricao = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_valor     = tk.StringVar()
        self.var_data      = tk.StringVar(value=hoje())
        self.id_selecionado = None

        self._build_ui()
        self._carregar_tabela()
        self._atualizar_resumo()

    # ── Construção da UI ─────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Cabeçalho ────────────────────────────────────────────────────────
        header = tk.Frame(self, bg=SURFACE, pady=14)
        header.pack(fill="x")

        tk.Label(
            header, text="💰 FinanControl",
            font=FONT_TITLE, bg=SURFACE, fg=WHITE
        ).pack(side="left", padx=24)

        tk.Label(
            header, text="Sistema de Controle Financeiro Pessoal",
            font=("Courier New", 10), bg=SURFACE, fg=SUBTEXT
        ).pack(side="left", padx=6, pady=6)

        # ── Corpo principal ──────────────────────────────────────────────────
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=14)

        # coluna esquerda – formulário
        self._build_form(body)

        # coluna direita – tabela + resumo
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        self._build_table(right)
        self._build_resumo(right)

    def _lbl(self, parent, text):
        tk.Label(parent, text=text, font=FONT_LABEL,
                 bg=SURFACE, fg=SUBTEXT).pack(anchor="w", pady=(10, 2), padx=14)

    def _entry(self, parent, textvariable):
        e = tk.Entry(parent, textvariable=textvariable, font=FONT_ENTRY,
                     bg=SURFACE2, fg=TEXT, insertbackground=TEXT,
                     relief="flat", bd=0, highlightthickness=1,
                     highlightbackground=BORDER, highlightcolor=ACCENT)
        e.pack(fill="x", padx=14, ipady=6)
        return e

    def _build_form(self, parent):
        frame = tk.Frame(parent, bg=SURFACE, width=300)
        frame.pack(side="left", fill="y", padx=(0, 14))
        frame.pack_propagate(False)

        tk.Label(frame, text="Nova Movimentação", font=FONT_RESUME,
                 bg=SURFACE, fg=WHITE).pack(pady=(18, 4), padx=14, anchor="w")

        # Tipo (Radio)
        self._lbl(frame, "TIPO")
        tipo_frame = tk.Frame(frame, bg=SURFACE)
        tipo_frame.pack(fill="x", padx=14)
        for t, cor in [("Receita", GREEN), ("Despesa", RED)]:
            tk.Radiobutton(
                tipo_frame, text=t, variable=self.var_tipo, value=t,
                font=FONT_LABEL, bg=SURFACE, fg=cor,
                selectcolor=SURFACE2, activebackground=SURFACE,
                activeforeground=cor, relief="flat"
            ).pack(side="left", padx=(0, 14))

        # Descrição
        self._lbl(frame, "DESCRIÇÃO")
        self._entry(frame, self.var_descricao)

        # Categoria (Combobox)
        self._lbl(frame, "CATEGORIA")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TCombobox",
                        fieldbackground=SURFACE2, background=SURFACE2,
                        foreground=TEXT, arrowcolor=ACCENT,
                        selectbackground=SURFACE2, selectforeground=TEXT)
        categorias = [
            "Alimentação", "Transporte", "Moradia", "Saúde",
            "Educação", "Lazer", "Salário", "Freelance",
            "Investimento", "Outros"
        ]
        combo = ttk.Combobox(frame, textvariable=self.var_categoria,
                             values=categorias, font=FONT_ENTRY,
                             style="Custom.TCombobox", state="normal")
        combo.pack(fill="x", padx=14, ipady=4)

        # Valor
        self._lbl(frame, "VALOR (R$)")
        self._entry(frame, self.var_valor)

        # Data
        self._lbl(frame, "DATA (DD/MM/AAAA)")
        self._entry(frame, self.var_data)

        # Botões
        btn_frame = tk.Frame(frame, bg=SURFACE)
        btn_frame.pack(fill="x", padx=14, pady=18)

        self._btn(btn_frame, "＋ Cadastrar",  ACCENT,  self._cadastrar).pack(fill="x", pady=3)
        self._btn(btn_frame, "✎  Atualizar",  ACCENT2, self._atualizar).pack(fill="x", pady=3)
        self._btn(btn_frame, "✕  Excluir",    RED,     self._excluir ).pack(fill="x", pady=3)
        self._btn(btn_frame, "↺  Limpar",     BORDER,  self._limpar  ).pack(fill="x", pady=3)

    def _btn(self, parent, text, color, command):
        return tk.Button(
            parent, text=text, font=FONT_BTN, bg=color, fg=WHITE,
            activebackground=SURFACE2, activeforeground=WHITE,
            relief="flat", bd=0, cursor="hand2", pady=8,
            command=command
        )

    def _build_table(self, parent):
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Movimentações", font=FONT_RESUME,
                 bg=BG, fg=WHITE).pack(anchor="w", pady=(0, 6))

        style = ttk.Style()
        style.configure("Treeview",
                        background=SURFACE, fieldbackground=SURFACE,
                        foreground=TEXT, font=FONT_TABLE, rowheight=28,
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background=SURFACE2, foreground=SUBTEXT,
                        font=FONT_LABEL, relief="flat")
        style.map("Treeview", background=[("selected", ACCENT2)])

        colunas = ("ID", "Tipo", "Descrição", "Categoria", "Valor", "Data")
        self.tree = ttk.Treeview(frame, columns=colunas,
                                 show="headings", selectmode="browse")

        widths = {"ID": 40, "Tipo": 80, "Descrição": 200,
                  "Categoria": 110, "Valor": 110, "Data": 90}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")

        self.tree.tag_configure("receita", foreground=GREEN)
        self.tree.tag_configure("despesa", foreground=RED)

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _build_resumo(self, parent):
        frame = tk.Frame(parent, bg=SURFACE, pady=14)
        frame.pack(fill="x", pady=(12, 0))

        self.lbl_receitas  = self._resumo_item(frame, "Total Receitas",  GREEN)
        self.lbl_despesas  = self._resumo_item(frame, "Total Despesas",  RED)
        self.lbl_saldo     = self._resumo_item(frame, "Saldo Final",     ACCENT)

    def _resumo_item(self, parent, label, color):
        col = tk.Frame(parent, bg=SURFACE)
        col.pack(side="left", expand=True)
        tk.Label(col, text=label, font=("Courier New", 9),
                 bg=SURFACE, fg=SUBTEXT).pack()
        lbl = tk.Label(col, text="R$ 0,00", font=FONT_RESUME,
                       bg=SURFACE, fg=color)
        lbl.pack()
        return lbl

    # ── Lógica CRUD ──────────────────────────────────────────────────────────
    def _validar(self):
        if not self.var_descricao.get().strip():
            messagebox.showwarning("Atenção", "Informe a descrição.")
            return False
        if not self.var_categoria.get().strip():
            messagebox.showwarning("Atenção", "Informe a categoria.")
            return False
        try:
            v = float(self.var_valor.get().replace(",", "."))
            if v <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Atenção", "Valor inválido. Use números positivos.")
            return False
        try:
            datetime.strptime(self.var_data.get(), "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Atenção", "Data inválida. Use DD/MM/AAAA.")
            return False
        return True

    def _cadastrar(self):
        if not self._validar():
            return
        db.adicionar_movimentacao(
            self.var_tipo.get(),
            self.var_descricao.get().strip(),
            self.var_categoria.get().strip(),
            float(self.var_valor.get().replace(",", ".")),
            self.var_data.get()
        )
        self._limpar()
        self._carregar_tabela()
        self._atualizar_resumo()
        messagebox.showinfo("Sucesso", "Movimentação cadastrada!")

    def _atualizar(self):
        if self.id_selecionado is None:
            messagebox.showwarning("Atenção", "Selecione um registro para atualizar.")
            return
        if not self._validar():
            return
        db.atualizar_movimentacao(
            self.id_selecionado,
            self.var_tipo.get(),
            self.var_descricao.get().strip(),
            self.var_categoria.get().strip(),
            float(self.var_valor.get().replace(",", ".")),
            self.var_data.get()
        )
        self._limpar()
        self._carregar_tabela()
        self._atualizar_resumo()
        messagebox.showinfo("Sucesso", "Movimentação atualizada!")

    def _excluir(self):
        if self.id_selecionado is None:
            messagebox.showwarning("Atenção", "Selecione um registro para excluir.")
            return
        if not messagebox.askyesno("Confirmar", "Deseja excluir esta movimentação?"):
            return
        db.excluir_movimentacao(self.id_selecionado)
        self._limpar()
        self._carregar_tabela()
        self._atualizar_resumo()

    def _limpar(self):
        self.var_tipo.set("Receita")
        self.var_descricao.set("")
        self.var_categoria.set("")
        self.var_valor.set("")
        self.var_data.set(hoje())
        self.id_selecionado = None
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    # ── Tabela e resumo ──────────────────────────────────────────────────────
    def _carregar_tabela(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for reg in db.listar_movimentacoes():
            id_, tipo, desc, cat, valor, data = reg
            tag = "receita" if tipo == "Receita" else "despesa"
            sinal = "+" if tipo == "Receita" else "-"
            self.tree.insert("", "end", iid=str(id_),
                             values=(id_, tipo, desc, cat,
                                     f"{sinal} {fmt_brl(valor)}", data),
                             tags=(tag,))

    def _atualizar_resumo(self):
        receitas, despesas, saldo = db.calcular_resumo()
        self.lbl_receitas.config(text=fmt_brl(receitas))
        self.lbl_despesas.config(text=fmt_brl(despesas))
        cor_saldo = GREEN if saldo >= 0 else RED
        self.lbl_saldo.config(text=fmt_brl(saldo), fg=cor_saldo)

    def _ao_selecionar(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        id_ = int(sel[0])
        for reg in db.listar_movimentacoes():
            if reg[0] == id_:
                self.id_selecionado = id_
                self.var_tipo.set(reg[1])
                self.var_descricao.set(reg[2])
                self.var_categoria.set(reg[3])
                self.var_valor.set(str(reg[4]))
                self.var_data.set(reg[5])
                break


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = FinanControlApp()
    app.mainloop()
