import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re
import json
import random
import string
import spacy
import docx
import pdfplumber

class AnonimizadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Anonimizador Completo com Tokens Aleatórios")
        self.mapa = {}
        self.contadores = {
            "CPF":0, "CNPJ":0, "NOME":0, "TELEFONE":0, "ENDERECO":0, "APELIDO":0, "AUTO":0
        }
        self.siglas_whitelist = {
            "ANTT", "GEAUT", "SEI", "GDF", "BR", "CPF", "CNPJ", "ME", "LTDA", "EIRELI", "FELVP"
        }

        self.nlp = spacy.load("pt_core_news_sm")

        self.notebook = tk.ttk.Notebook(root)
        self.frame_anonimizar = tk.Frame(self.notebook)
        self.frame_revelar = tk.Frame(self.notebook)
        self.notebook.add(self.frame_anonimizar, text="Anonimizar")
        self.notebook.add(self.frame_revelar, text="Revelar")
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.setup_anonimizar()
        self.setup_revelar()

    def gerar_id_aleatorio(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def gerar_token(self, tipo):
        self.contadores[tipo] += 1
        id_aleatorio = self.gerar_id_aleatorio()
        token = f"{tipo}_{self.contadores[tipo]}_{id_aleatorio}"
        return token

    def anonimizar_texto(self, texto):
        self.mapa = {}
        self.contadores = {k:0 for k in self.contadores}

        # Preservar autos do tipo FELVP1234567
        autos_encontrados = re.findall(r'\bFELVP\d+\b', texto, flags=re.IGNORECASE)
        for auto in autos_encontrados:
            chave = f"AUTO_{self.contadores['AUTO']+1}_{self.gerar_id_aleatorio()}"
            self.contadores["AUTO"] += 1
            self.mapa[chave] = auto
            texto = re.sub(re.escape(auto), chave, texto, flags=re.IGNORECASE)

        # Substituir CPF
        def substituir_cpf(m):
            valor = m.group()
            token = self.gerar_token("CPF")
            self.mapa[token] = valor
            return token
        cpf_pattern = r'\b\d{3}\.?\d{3}\.?\d{3}-\d{2}\b'
        texto = re.sub(cpf_pattern, substituir_cpf, texto)

        # Substituir CNPJ
        def substituir_cnpj(m):
            valor = m.group()
            token = self.gerar_token("CNPJ")
            self.mapa[token] = valor
            return token
        cnpj_pattern = r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b'
        texto = re.sub(cnpj_pattern, substituir_cnpj, texto)

        # Substituir telefones, ignorando autos
        def substituir_telefone(m):
            valor = m.group()
            # Se valor está dentro de algum token AUTO, não substituir
            if any(valor in self.mapa[a] for a in self.mapa if a.startswith("AUTO_")):
                return valor
            token = self.gerar_token("TELEFONE")
            self.mapa[token] = valor
            return token
        telefone_pattern = r'\(?\d{2}\)?\s*\d{4,5}-?\d{4}'
        texto = re.sub(telefone_pattern, substituir_telefone, texto)

        # spaCy para nomes, endereços, locais e organizações
        doc = self.nlp(texto)
        entidades = [(ent.start_char, ent.end_char, ent.text, ent.label_) for ent in doc.ents]
        entidades = sorted(entidades, key=lambda x: x[0], reverse=True)

        for start, end, texto_ent, label in entidades:
            if label in ("PER", "LOC", "GPE", "ORG"):
                if label == "PER":
                    tipo_token = "NOME"
                elif label == "ORG":
                    tipo_token = "APELIDO"
                else:
                    tipo_token = "ENDERECO"
                token = self.gerar_token(tipo_token)
                self.mapa[token] = texto_ent
                texto = texto[:start] + token + texto[end:]

        # Regex extra para nomes após "RESPONSÁVEL:"
        def anonimizar_responsavel(match):
            prefixo = match.group(1)
            nome = match.group(2)
            token = self.gerar_token("NOME")
            self.mapa[token] = nome
            return f"{prefixo}{token}"
        texto = re.sub(
            r'(RESPONS[ÁA]VEL:\s*)([A-Z][A-Za-zÀ-ÿ]+(?:\s[A-Z][A-Za-zÀ-ÿ]+)+)',
            anonimizar_responsavel,
            texto
        )

        # Regex para nomes fantasia / apelidos comerciais (palavras + termo comercial)
        termos_empresas = r'\b(\w+\s+(Transportes|Transportadora|Logística|Logistica|LTDA|ME|EIRELI|Comércio|Comercial))\b'
        def substituir_apelido(m):
            valor = m.group(1)
            token = self.gerar_token("APELIDO")
            self.mapa[token] = valor
            return token
        texto = re.sub(termos_empresas, substituir_apelido, texto, flags=re.IGNORECASE)

        # Regex para palavras isoladas em maiúsculas (>=3 letras) exceto siglas whitelist
        def substituir_maiusculas(match):
            palavra = match.group()
            if palavra in self.siglas_whitelist:
                return palavra
            token = self.gerar_token("NOME")
            self.mapa[token] = palavra
            return token
        texto = re.sub(r'\b[A-Z]{3,}\b', substituir_maiusculas, texto)

        # Restaurar tokens AUTO para texto original
        for chave, valor in self.mapa.items():
            if chave.startswith("AUTO_"):
                texto = texto.replace(chave, valor)

        return texto

    def setup_anonimizar(self):
        tk.Label(self.frame_anonimizar, text="Carregar arquivo (.txt, .pdf, .docx) ou colar texto:").pack()
        btn_load = tk.Button(self.frame_anonimizar, text="Carregar arquivo", command=self.carregar_arquivo_anonim)
        btn_load.pack(pady=5)

        self.txt_entrada_anonim = scrolledtext.ScrolledText(self.frame_anonimizar, height=10)
        self.txt_entrada_anonim.pack(fill=tk.BOTH, expand=True)

        btn_anonimizar = tk.Button(self.frame_anonimizar, text="Anonimizar Texto", command=self.anonimizar_texto_interface)
        btn_anonimizar.pack(pady=10)

        tk.Label(self.frame_anonimizar, text="Texto anonimizado (tokens no lugar de dados sensíveis):").pack()
        self.txt_saida_anonim = scrolledtext.ScrolledText(self.frame_anonimizar, height=10)
        self.txt_saida_anonim.pack(fill=tk.BOTH, expand=True)

        frame_botoes = tk.Frame(self.frame_anonimizar)
        frame_botoes.pack(pady=5)
        btn_salvar_mapa = tk.Button(frame_botoes, text="Salvar mapa JSON", command=self.salvar_mapa)
        btn_salvar_mapa.pack(side=tk.LEFT, padx=10)
        btn_salvar_texto = tk.Button(frame_botoes, text="Salvar texto anonimizado", command=self.salvar_texto)
        btn_salvar_texto.pack(side=tk.LEFT, padx=10)

    def setup_revelar(self):
        tk.Label(self.frame_revelar, text="Carregar texto anonimizado (com tokens):").pack()
        btn_load = tk.Button(self.frame_revelar, text="Carregar arquivo TXT", command=self.carregar_arquivo_revelar)
        btn_load.pack(pady=5)

        self.txt_entrada_revelar = scrolledtext.ScrolledText(self.frame_revelar, height=10)
        self.txt_entrada_revelar.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame_revelar, text="Anexar arquivo JSON do mapa:").pack()
        btn_load_json = tk.Button(self.frame_revelar, text="Carregar mapa JSON", command=self.carregar_mapa_json)
        btn_load_json.pack(pady=5)

        self.lbl_mapa_status = tk.Label(self.frame_revelar, text="Nenhum mapa carregado.")
        self.lbl_mapa_status.pack()

        btn_revelar = tk.Button(self.frame_revelar, text="Revelar Texto Original", command=self.revelar_texto)
        btn_revelar.pack(pady=10)

        tk.Label(self.frame_revelar, text="Texto restaurado (original):").pack()
        self.txt_saida_revelar = scrolledtext.ScrolledText(self.frame_revelar, height=10)
        self.txt_saida_revelar.pack(fill=tk.BOTH, expand=True)

        btn_salvar_restaurado = tk.Button(self.frame_revelar, text="Salvar texto restaurado", command=self.salvar_texto_restaurado)
        btn_salvar_restaurado.pack(pady=10)

        self.mapa_revelar = {}

    def carregar_arquivo_anonim(self):
        caminho = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),
                                                       ("PDF files", "*.pdf"),
                                                       ("Word files", "*.docx")])
        if caminho:
            if caminho.endswith(".txt"):
                with open(caminho, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
            elif caminho.endswith(".pdf"):
                conteudo = self.extrair_texto_pdf(caminho)
            elif caminho.endswith(".docx"):
                conteudo = self.extrair_texto_docx(caminho)
            else:
                messagebox.showerror("Erro", "Formato de arquivo não suportado.")
                return
            self.txt_entrada_anonim.delete('1.0', tk.END)
            self.txt_entrada_anonim.insert(tk.END, conteudo)

    def extrair_texto_pdf(self, caminho_pdf):
        import pdfplumber
        texto = ""
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() + "\n"
        return texto

    def extrair_texto_docx(self, caminho_docx):
        import docx
        doc = docx.Document(caminho_docx)
        texto = "\n".join([p.text for p in doc.paragraphs])
        return texto

    def anonimizar_texto_interface(self):
        texto = self.txt_entrada_anonim.get('1.0', tk.END)
        texto_anon = self.anonimizar_texto(texto)
        self.txt_saida_anonim.delete('1.0', tk.END)
        self.txt_saida_anonim.insert(tk.END, texto_anon)

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
        texto = self.txt_saida_anonim.get('1.0', tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Nenhum texto anonimizado para salvar.")
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if caminho:
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(texto)
            messagebox.showinfo("Sucesso", f"Texto anonimizado salvo em:\n{caminho}")

    def carregar_arquivo_revelar(self):
        caminho = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if caminho:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            self.txt_entrada_revelar.delete('1.0', tk.END)
            self.txt_entrada_revelar.insert(tk.END, conteudo)

    def carregar_mapa_json(self):
        caminho = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if caminho:
            with open(caminho, 'r', encoding='utf-8') as f:
                self.mapa_revelar = json.load(f)
            self.lbl_mapa_status.config(text=f"Mapa carregado: {caminho}")

    def revelar_texto(self):
        texto_anon = self.txt_entrada_revelar.get('1.0', tk.END)
        if not self.mapa_revelar:
            messagebox.showwarning("Aviso", "Nenhum mapa JSON carregado.")
            return
        texto_restaurado = texto_anon
        for chave, valor in self.mapa_revelar.items():
            texto_restaurado = texto_restaurado.replace(chave, valor)
        self.txt_saida_revelar.delete('1.0', tk.END)
        self.txt_saida_revelar.insert(tk.END, texto_restaurado)

    def salvar_texto_restaurado(self):
        texto = self.txt_saida_revelar.get('1.0', tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Nenhum texto restaurado para salvar.")
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if caminho:
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(texto)
            messagebox.showinfo("Sucesso", f"Texto restaurado salvo em:\n{caminho}")

if __name__ == "__main__":
    import tkinter.ttk as ttk
    root = tk.Tk()
    app = AnonimizadorApp(root)
    root.geometry("900x700")
    root.mainloop()
