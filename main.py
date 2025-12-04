import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
import webbrowser

# Importações do ReportLab para PDF
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class CalculadoraOrcamentoPF: 
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Calculadora de orçamento por Pontos de Função")
        self.janela.geometry("920x700")
        self.janela.configure(bg="#f0f0f0")
        
        # Variáveis
        self.funcionalidades = []
        self.valor_hora = 50.00
        self.total_pf = 0
        self.total_horas = 0
        
        # Tentar registrar fontes (opcional)
        try:
            # Tente registrar fontes TrueType se disponíveis
            pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
            pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
        except:
            print("Fontes Arial não encontradas. Usando fontes padrão do ReportLab.")
        
        self.criar_widgets()
        
    def criar_widgets(self):
        # Cabeçalho
        header_frame = tk.Frame(self.janela, bg="#2c3e50", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        titulo = tk.Label(header_frame, text="CALCULADORA DE ORÇAMENTO POR PONTOS DE FUNÇÕES", 
                         font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        titulo.pack(expand=True)
        
        # Frame principal com dois painéis
        main_frame = tk.Frame(self.janela, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Painel esquerdo - Configurações
        left_frame = tk.LabelFrame(main_frame, text="Configurações do Projeto", 
                                  font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # Painel direito - Funcionalidades e Resultados
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side="right", fill="both", expand=True)
        
        # ============ PAINEL ESQUERDO ============
        # Projeto
        tk.Label(left_frame, text="Nome do Projeto:", bg="white", anchor="w").pack(fill="x", pady=(5, 2))
        self.entry_projeto = tk.Entry(left_frame, width=30)
        self.entry_projeto.pack(fill="x", pady=(0, 10))
        self.entry_projeto.insert(0, "Digite o nome aqui")
        
        tk.Label(left_frame, text="Nome do Cliente:", bg="white", anchor="w").pack(fill="x", pady=(5, 2))
        self.entry_cliente = tk.Entry(left_frame, width=30)
        self.entry_cliente.pack(fill="x", pady=(0, 10))
        self.entry_cliente.insert(0, "Digite o nome aqui")
        
        # Configurações Financeiras
        tk.Label(left_frame, text="Valor da Hora (R$):", bg="white", anchor="w").pack(fill="x", pady=(5, 2))
        self.entry_valor_hora = tk.Entry(left_frame, width=30)
        self.entry_valor_hora.pack(fill="x", pady=(0, 10))
        self.entry_valor_hora.insert(0, "50.00")
        
        # Separador
        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Adicionar Funcionalidade
        tk.Label(left_frame, text="Adicionar Funcionalidade", font=("Arial", 10, "bold"), 
                bg="white").pack(fill="x", pady=(0, 10))
        
        tk.Label(left_frame, text="Descrição:", bg="white", anchor="w").pack(fill="x", pady=(2, 0))
        self.entry_descricao = tk.Entry(left_frame, width=30)
        self.entry_descricao.pack(fill="x", pady=(0, 5))
        self.entry_descricao.insert(0, "Tela de Login")
        
        # Tipo da Funcionalidade
        tk.Label(left_frame, text="Tipo:", bg="white", anchor="w").pack(fill="x", pady=(5, 2))
        self.combo_tipo = ttk.Combobox(left_frame, values=[
            "Entrada Externa (EE)",
            "Saída Externa (SE)",
            "Consulta Externa (CE)",
            "Arquivo Lógico Interno (ALI)",
            "Arquivo de Interface Externa (AIE)"
        ], state="readonly", width=28)
        self.combo_tipo.pack(fill="x", pady=(0, 5))
        self.combo_tipo.set("Arquivo Lógico Interno (ALI)")
        
        # Complexidade
        tk.Label(left_frame, text="Complexidade:", bg="white", anchor="w").pack(fill="x", pady=(5, 2))
        self.combo_complexidade = ttk.Combobox(left_frame, values=[
            "Baixa", "Média", "Alta"
        ], state="readonly", width=28)
        self.combo_complexidade.pack(fill="x", pady=(0, 5))
        self.combo_complexidade.set("Baixa")
        
        # Botão Adicionar
        btn_adicionar = tk.Button(left_frame, text="ADICIONAR FUNCIONALIDADE", 
                                 command=self.adicionar_funcionalidade,
                                 bg="#3498db", fg="white", font=("Arial", 10, "bold"))
        btn_adicionar.pack(fill="x", pady=10)
        
        # ============ PAINEL DIREITO ============
        # Frame para tabela de funcionalidades
        table_frame = tk.LabelFrame(right_frame, text="Funcionalidades Adicionadas", 
                                   font=("Arial", 10, "bold"), bg="white", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Cabeçalho da tabela
        headers = ["Descrição", "Tipo", "Complexidade", "PF"]
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, font=("Arial", 9, "bold"), 
                           bg="#ecf0f1", padx=10, pady=5)
            label.grid(row=0, column=i, sticky="ew", padx=1, pady=1)
            table_frame.grid_columnconfigure(i, weight=1)
        
        # Área para as funcionalidades (vai ser preenchida dinamicamente)
        self.table_rows_frame = tk.Frame(table_frame, bg="white")
        self.table_rows_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")
        table_frame.grid_rowconfigure(1, weight=1)
        
        # Scrollbar para a tabela
        scrollbar = tk.Scrollbar(self.table_rows_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas_table = tk.Canvas(self.table_rows_frame, bg="white", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.canvas_table.yview)
        self.canvas_table.pack(side="left", fill="both", expand=True)
        
        self.inner_table_frame = tk.Frame(self.canvas_table, bg="white")
        self.canvas_table.create_window((0, 0), window=self.inner_table_frame, anchor="nw")
        
        # Frame para resultados
        result_frame = tk.Frame(right_frame, bg="white", relief="solid", borderwidth=1)
        result_frame.pack(fill="x", pady=(10, 0))
        
        # Total PF
        tk.Label(result_frame, text="TOTAL PF:", font=("Arial", 12, "bold"), 
                bg="white").pack(side="left", padx=20, pady=15)
        self.label_total_pf = tk.Label(result_frame, text="0", font=("Arial", 14, "bold"), 
                                      bg="white", fg="#e74c3c")
        self.label_total_pf.pack(side="left", padx=(0, 40), pady=15)
        
        # Estimativa de Horas
        tk.Label(result_frame, text="Estimativa de Horas:", font=("Arial", 12, "bold"), 
                bg="white").pack(side="left", padx=20, pady=15)
        self.label_total_horas = tk.Label(result_frame, text="0h", font=("Arial", 14, "bold"), 
                                         bg="white", fg="#e74c3c")
        self.label_total_horas.pack(side="left", padx=(0, 40), pady=15)
        
        # Orçamento Final
        tk.Label(result_frame, text="Orçamento Final:", font=("Arial", 12, "bold"), 
                bg="white").pack(side="left", padx=20, pady=15)
        self.label_orcamento = tk.Label(result_frame, text="R$ 0,00", font=("Arial", 16, "bold"), 
                                       bg="white", fg="#27ae60")
        self.label_orcamento.pack(side="left", padx=(0, 20), pady=15)
        
        # Frame para botões inferiores
        button_frame = tk.Frame(right_frame, bg="#f0f0f0")
        button_frame.pack(fill="x", pady=(20, 10))
        
        # Botão Exportar PDF
        btn_exportar = tk.Button(button_frame, text="EXPORTAR PDF REAL", 
                                command=self.exportar_pdf,
                                bg="#27ae60", fg="white", 
                                font=("Arial", 11, "bold"), padx=20, pady=10)
        btn_exportar.pack(side="left", padx=(0, 10))
        
        # Botão Limpar
        btn_limpar = tk.Button(button_frame, text="LIMPAR TUDO", 
                              command=self.limpar_tudo,
                              bg="#e74c3c", fg="white", 
                              font=("Arial", 11, "bold"), padx=20, pady=10)
        btn_limpar.pack(side="left")
        
        # Rodapé
        footer_frame = tk.Frame(self.janela, bg="#f0f0f0", height=50)
        footer_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        copyright_label = tk.Label(footer_frame, 
                                  text="Copyright©. Todos os direitos reservados.", 
                                  font=("Arial", 8), bg="#f0f0f0", fg="#7f8c8d")
        copyright_label.pack(side="left", padx=20)
        
        windows_label = tk.Label(footer_frame, 
                                text="Ativar o Windows\nAcesse Configurações", 
                                font=("Arial", 8), bg="#f0f0f0", fg="#7f8c8d", justify="right")
        windows_label.pack(side="right", padx=20)
        
        # Configurar bind para scroll
        self.inner_table_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas_table.bind("<Configure>", self.on_canvas_configure)
    
    def on_frame_configure(self, event):
        self.canvas_table.configure(scrollregion=self.canvas_table.bbox("all"))
    
    def on_canvas_configure(self, event):
        self.canvas_table.itemconfig(self.canvas_table.find_all()[0], width=event.width)
    
    def calcular_pf(self, tipo, complexidade):
        """Calcula pontos de função baseado na matriz de complexidade"""
        # Matriz simplificada de pontos de função
        matriz_pf = {
            "Entrada Externa (EE)": {"Baixa": 3, "Média": 4, "Alta": 6},
            "Saída Externa (SE)": {"Baixa": 4, "Média": 5, "Alta": 7},
            "Consulta Externa (CE)": {"Baixa": 3, "Média": 4, "Alta": 6},
            "Arquivo Lógico Interno (ALI)": {"Baixa": 7, "Média": 10, "Alta": 15},
            "Arquivo de Interface Externa (AIE)": {"Baixa": 5, "Média": 7, "Alta": 10}
        }
        
        return matriz_pf.get(tipo, {}).get(complexidade, 0)
    
    def adicionar_funcionalidade(self):
        descricao = self.entry_descricao.get()
        tipo = self.combo_tipo.get()
        complexidade = self.combo_complexidade.get()
        
        if not descricao or descricao == "Digite a descrição aqui":
            messagebox.showwarning("Aviso", "Por favor, insira uma descrição para a funcionalidade.")
            return
        
        # Calcular PF
        pf = self.calcular_pf(tipo, complexidade)
        
        # Adicionar à lista
        funcionalidade = {
            "descricao": descricao,
            "tipo": tipo,
            "complexidade": complexidade,
            "pf": pf
        }
        self.funcionalidades.append(funcionalidade)
        
        # Atualizar tabela
        self.atualizar_tabela()
        
        # Atualizar totais
        self.atualizar_totais()
        
        # Limpar campo de descrição
        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, "Nova Funcionalidade")
    
    def atualizar_tabela(self):
        # Limpar tabela atual
        for widget in self.inner_table_frame.winfo_children():
            widget.destroy()
        
        # Adicionar novas linhas
        for i, func in enumerate(self.funcionalidades):
            # Descrição
            desc_label = tk.Label(self.inner_table_frame, text=func["descricao"], 
                                 bg="white", padx=10, pady=5, anchor="w")
            desc_label.grid(row=i, column=0, sticky="ew", padx=1, pady=1)
            
            # Tipo
            tipo_label = tk.Label(self.inner_table_frame, text=func["tipo"].split("(")[0], 
                                 bg="white", padx=10, pady=5)
            tipo_label.grid(row=i, column=1, sticky="ew", padx=1, pady=1)
            
            # Complexidade
            comp_label = tk.Label(self.inner_table_frame, text=func["complexidade"], 
                                 bg="white", padx=10, pady=5)
            comp_label.grid(row=i, column=2, sticky="ew", padx=1, pady=1)
            
            # PF
            pf_label = tk.Label(self.inner_table_frame, text=str(func["pf"]), 
                               bg="white", padx=10, pady=5, fg="#e74c3c", font=("Arial", 9, "bold"))
            pf_label.grid(row=i, column=3, sticky="ew", padx=1, pady=1)
            
            # Configurar pesos das colunas
            for j in range(4):
                self.inner_table_frame.grid_columnconfigure(j, weight=1)
    
    def atualizar_totais(self):
        # Calcular total PF
        self.total_pf = sum(func["pf"] for func in self.funcionalidades)
        self.label_total_pf.config(text=str(self.total_pf))
        
        # Calcular horas (aproximadamente 8 horas por PF)
        self.total_horas = self.total_pf * 8
        self.label_total_horas.config(text=f"{self.total_horas}h")
        
        # Calcular orçamento
        try:
            valor_hora = float(self.entry_valor_hora.get().replace(",", "."))
        except:
            valor_hora = 50.00
        
        orcamento = self.total_horas * valor_hora
        self.label_orcamento.config(text=f"R$ {orcamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    def exportar_pdf(self):
        """Exporta o orçamento para um arquivo PDF real usando ReportLab"""
        try:
            # Abrir caixa de diálogo para salvar arquivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")],
                title="Exportar Orçamento para PDF"
            )
            
            if not file_path:
                return
            
            # Criar documento PDF
            doc = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Obter estilos padrão
            styles = getSampleStyleSheet()
            
            # Criar estilos personalizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#2c3e50'),
                alignment=1,  # Centralizado
                spaceAfter=20
            )
            
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor('#34495e'),
                spaceAfter=10
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6
            )
            
            # Conteúdo do PDF
            story = []
            
            # Título
            story.append(Paragraph("ORÇAMENTO POR PONTOS DE FUNÇÃO", title_style))
            story.append(Spacer(1, 20))
            
            # Informações do projeto
            story.append(Paragraph(f"<b>PROJETO:</b> {self.entry_projeto.get()}", normal_style))
            story.append(Paragraph(f"<b>CLIENTE:</b> {self.entry_cliente.get()}", normal_style))
            story.append(Paragraph(f"<b>DATA:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
            
            # Valor da hora
            try:
                valor_hora = float(self.entry_valor_hora.get().replace(",", "."))
                valor_formatado = f"R$ {valor_hora:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                story.append(Paragraph(f"<b>VALOR DA HORA:</b> {valor_formatado}", normal_style))
            except:
                story.append(Paragraph(f"<b>VALOR DA HORA:</b> R$ 50,00", normal_style))
            
            story.append(Spacer(1, 20))
            
            # Tabela de funcionalidades
            if self.funcionalidades:
                story.append(Paragraph("<b>FUNCIONALIDADES DO PROJETO</b>", subtitle_style))
                story.append(Spacer(1, 10))
                
                # Cabeçalho da tabela
                table_data = []
                headers = ["Descrição", "Tipo", "Complexidade", "PF"]
                table_data.append(headers)
                
                # Dados da tabela
                for func in self.funcionalidades:
                    row = [
                        func['descricao'],
                        func['tipo'].split('(')[0],  # Remove o código entre parênteses
                        func['complexidade'],
                        str(func['pf'])
                    ]
                    table_data.append(row)
                
                # Criar tabela
                table = Table(table_data, colWidths=[200, 150, 80, 50])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ecf0f1')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (3, 0), (3, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ]))
                
                story.append(table)
                story.append(Spacer(1, 20))
            
            # Resumo do orçamento
            story.append(Paragraph("RESUMO DO ORÇAMENTO", subtitle_style))
            story.append(Spacer(1, 10))
            
            # Calcular valores
            try:
                valor_hora = float(self.entry_valor_hora.get().replace(",", "."))
            except:
                valor_hora = 50.00
            
            total_horas = self.total_pf * 8
            orcamento = total_horas * valor_hora
            
            # Formatar valores monetários
            valor_hora_formatado = f"R$ {valor_hora:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            orcamento_formatado = f"R$ {orcamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
            resumo_data = [
                ["Descrição", "Valor"],
                ["Total de Pontos de Função (PF)", str(self.total_pf)],
                ["Estimativa de Horas (8h por PF)", f"{total_horas}h"],
                ["Valor por Hora", valor_hora_formatado],
                ["", ""],
                ["ORÇAMENTO FINAL", f"<b>{orcamento_formatado}</b>"]
            ]
            
            resumo_table = Table(resumo_data, colWidths=[250, 100])
            resumo_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('LINEABOVE', (0, 5), (-1, 5), 1, colors.grey),
                ('LINEBELOW', (0, 5), (-1, 5), 1, colors.grey),
                ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#f8f9fa')),
            ]))
            
            story.append(resumo_table)
            story.append(Spacer(1, 30))
            
            # Observações
            story.append(Paragraph("<b>OBSERVAÇÕES:</b>", normal_style))
            story.append(Paragraph("1. Este orçamento é baseado na metodologia de Pontos de Função (Function Points)", normal_style))
            story.append(Paragraph("2. A estimativa de horas considera 8 horas de trabalho por PF", normal_style))
            story.append(Paragraph("3. Valores sujeitos a alterações conforme escopo definido", normal_style))
            story.append(Paragraph("4. Orçamento válido por 30 dias a partir da data de emissão", normal_style))
            story.append(Spacer(1, 20))
            
            # Assinatura
            story.append(Paragraph("_" * 50, normal_style))
            story.append(Spacer(1, 5))
            story.append(Paragraph("<b>Responsável Técnico</b>", normal_style))
            story.append(Paragraph("Assinatura: ___________________________", normal_style))
            story.append(Spacer(1, 20))
            
            # Rodapé
            story.append(Paragraph("_" * 78, normal_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph("Copyright© - Todos os direitos reservados", 
                                 ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                                               textColor=colors.grey, alignment=1)))
            story.append(Paragraph("Gerado por: Calculadora de Orçamento por Pontos de Função", 
                                 ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                                               textColor=colors.grey, alignment=1)))
            story.append(Paragraph(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 
                                 ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                                               textColor=colors.grey, alignment=1)))
            
            # Gerar PDF
            doc.build(story)
            
            # Perguntar se deseja abrir o PDF
            if messagebox.askyesno("Sucesso", 
                                  f"PDF gerado com sucesso!\n\nArquivo: {os.path.basename(file_path)}\n\nDeseja abrir o arquivo?"):
                webbrowser.open(file_path)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o PDF:\n\n{str(e)}\n\nCertifique-se de que tem permissão para escrever no diretório.")
    
    def limpar_tudo(self):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar todos os dados?"):
            # Limpar funcionalidades
            self.funcionalidades = []
            self.atualizar_tabela()
            
            # Resetar totais
            self.total_pf = 0
            self.total_horas = 0
            self.label_total_pf.config(text="0")
            self.label_total_horas.config(text="0h")
            self.label_orcamento.config(text="R$ 0,00")
            
            # Resetar campos
            self.entry_projeto.delete(0, tk.END)
            self.entry_projeto.insert(0, "Digite o nome aqui")
            
            self.entry_cliente.delete(0, tk.END)
            self.entry_cliente.insert(0, "Digite o nome aqui")
            
            self.entry_descricao.delete(0, tk.END)
            self.entry_descricao.insert(0, "Tela de Login")
            
            self.entry_valor_hora.delete(0, tk.END)
            self.entry_valor_hora.insert(0, "50.00")
            
            messagebox.showinfo("Sucesso", "Todos os dados foram limpos!")
    
    def executar(self):
        self.janela.mainloop()

# ==============================================
# FUNÇÃO PARA TESTAR O PDF SEM INTERFACE GRÁFICA
# ==============================================
def testar_geracao_pdf():
    """Função para testar a geração de PDF sem abrir a interface"""
    print("Testando geração de PDF...")
    
    # Dados de exemplo
    funcionalidades_teste = [
        {"descricao": "Tela de Login", "tipo": "Entrada Externa (EE)", "complexidade": "Baixa", "pf": 3},
        {"descricao": "Relatório de Vendas", "tipo": "Saída Externa (SE)", "complexidade": "Média", "pf": 5},
        {"descricao": "Cadastro de Clientes", "tipo": "Arquivo Lógico Interno (ALI)", "complexidade": "Alta", "pf": 15},
    ]
    
    # Criar PDF de teste
    doc = SimpleDocTemplate("teste_orcamento.pdf", pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Adicionar conteúdo
    story.append(Paragraph("TESTE DE ORÇAMENTO PDF", styles['Heading1']))
    story.append(Spacer(1, 20))
    
    # Tabela de exemplo
    table_data = [["Funcionalidade", "PF"]]
    for func in funcionalidades_teste:
        table_data.append([func["descricao"], str(func["pf"])])
    
    table = Table(table_data)
    story.append(table)
    
    # Gerar PDF
    doc.build(story)
    print("PDF de teste gerado: teste_orcamento.pdf")
    
    # Abrir PDF
    webbrowser.open("teste_orcamento.pdf")

# ==============================================
# INSTRUÇÕES DE INSTALAÇÃO E USO
# ==============================================
def mostrar_instrucoes():
    print("=" * 60)
    print("CALCULADORA DE ORÇAMENTO POR PONTOS DE FUNÇÃO")
    print("=" * 60)
    print("\nINSTRUÇÕES DE INSTALAÇÃO:")
    print("1. Instale as dependências:")
    print("   pip install reportlab")
    print("\n2. Execute o programa:")
    print("   python calculadora_orcamento_pf.py")
    print("\n3. Para testar apenas a geração de PDF:")
    print("   Descomente a linha: testar_geracao_pdf()")
    print("\n4. Recursos incluídos:")
    print("   - Interface gráfica com Tkinter")
    print("   - Cálculo automático de PF, horas e orçamento")
    print("   - Exportação para PDF profissional")
    print("   - Tabela com scroll")
    print("   - Formatação monetária brasileira")
    print("=" * 60)

# ==============================================
# EXECUÇÃO PRINCIPAL
# ==============================================
if __name__ == "__main__":
    # Descomente a linha abaixo para testar apenas a geração de PDF
    # testar_geracao_pdf()
    
    # Mostrar instruções no console
    mostrar_instrucoes()
    
    # Executar a aplicação principal
    app = CalculadoraOrcamentoPF()
    app.executar()