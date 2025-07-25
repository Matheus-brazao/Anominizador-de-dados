import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import json

class AnonimizadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Anonimizador de Documentos - Protótipo")
        self.mapa = {}

        # Layout
        # Entrada texto
        tk.Label(root, text="Carregar arquivo .txt ou colar texto:").pack()
        btn_load = tk.Button(root, text="Carregar arquivo TXT", command=self.carregar_arquivo)
        btn_load.pack(pady=5)

        self.txt_entrada = scrolledtext.ScrolledText(root, height=10)
        self.txt_entrada.pack(fill=tk.BOTH, expand=True)

        # Botão anonimizar (remove dados sensíveis)
        btn_anonimizar = tk.Button(root, text="Anonimizar Texto", command=self.anonimizar_texto_interface)
        btn_anonimizar.pack(pady=10)

        # Saída texto anonimizado (sem criptografia)
        tk.Label(root, text="Texto anonimizado (dados sensíveis substituídos por placeholders):").pack()
        self.txt_saida = scrolledtext.ScrolledText(root, height=10)
        self.txt_saida.pack(fill=tk.BOTH, expand=True)

        # Botões salvar mapa e texto
        frame_botoes = tk.Frame(root)
        frame_botoes.pack(pady=5)
        btn_salvar_mapa = tk.Button(frame_botoes, text="Salvar mapa JSON", command=self.salvar_mapa)
        btn_salvar_mapa.pack(side=tk.LEFT, padx=10)
        btn_salvar_texto = tk.Button(frame_botoes, text="Salvar texto anonimizado", command=self.salvar_texto)
        btn_salvar_texto.pack(side=tk.LEFT, padx=10)

    def carregar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if caminho:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            self.txt_entrada.delete('1.0', tk.END)
            self.txt_entrada.insert(tk.END, conteudo)

    def anonimizar_texto(self, texto):
        self.mapa = {}
        contador = 1

        def substituir(match, tipo):
            nonlocal contador
            valor = match.group()
            chave = f"[{tipo}_{contador}]"  # Placeholder, ex: [CPF_1]
            self.mapa[chave] = valor        # Salva valor real no mapa
            contador += 1
            return chave

        # Substitui CPF
        texto = re.sub(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', lambda m: substituir(m, "CPF"), texto)
        # Substitui CNPJ
        texto = re.sub(r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b', lambda m: substituir(m, "CNPJ"), texto)

        # Substitui nomes fixos (exemplo)
        nomes = ['João', 'Maria', 'Pedro', 'Ana', 'Carlos']
        for nome in nomes:
            texto = re.sub(rf'\b{nome}\b', lambda m: substituir(m, "NOME"), texto, flags=re.IGNORECASE)

        return texto

    def anonimizar_texto_interface(self):
        texto = self.txt_entrada.get('1.0', tk.END)
        texto_anon = self.anonimizar_texto(texto)
        self.txt_saida.delete('1.0', tk.END)
        self.txt_saida.insert(tk.END, texto_anon)

    def salvar_mapa(self):
        if not self.mapa:
            messagebox.showwarning("Aviso", "Nenhum mapa gerado ainda.")
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if caminho:
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(self.mapa, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Sucesso", f"Mapa salvo em:\n{caminho}")

    def salvar_texto(self):
        texto = self.txt_saida.get('1.0', tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Nenhum texto anonimizado para salvar.")
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if caminho:
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(texto)
            messagebox.showinfo("Sucesso", f"Texto anonimizado salvo em:\n{caminho}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnonimizadorApp(root)
    root.geometry("800x600")
    root.mainloop()
