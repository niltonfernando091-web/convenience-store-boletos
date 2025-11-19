# modules/pdf_reports.py
import os
import pandas as pd
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import plotly.express as px
import plotly.graph_objects as go

class PDFReports:
    def __init__(self, database):
        self.db = database
        self.reports_dir = "relatorios"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def gerar_relatorio_mensal(self, mes=None, ano=None):
        """Gera relatório mensal completo em PDF"""
        try:
            # Define mês e ano
            if mes is None:
                mes = datetime.now().month
            if ano is None:
                ano = datetime.now().year
            
            # Obtém dados do mês
            boletos = self._obter_boletos_do_mes(mes, ano)
            
            if not boletos:
                return None, "Nenhum dado encontrado para o período"
            
            # Cria nome do arquivo
            nome_arquivo = f"relatorio_mensal_{mes:02d}_{ano}.pdf"
            caminho_completo = os.path.join(self.reports_dir, nome_arquivo)
            
            # Cria o PDF
            doc = SimpleDocTemplate(
                caminho_completo,
                pagesize=A4,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )
            
            # Elementos do PDF
            elementos = []
            
            # 1. Cabeçalho
            elementos.extend(self._criar_cabecalho(mes, ano))
            
            # 2. Resumo Executivo
            elementos.extend(self._criar_resumo_executivo(boletos, mes, ano))
            
            # 3. Detalhamento por Categoria
            elementos.extend(self._criar_detalhes_categoria(boletos))
            
            # 4. Lista de Boletos
            elementos.extend(self._criar_lista_boletos(boletos))
            
            # 5. Rodapé
            elementos.extend(self._criar_rodape())
            
            # Gera o PDF
            doc.build(elementos)
            
            return caminho_completo, f"Relatório gerado: {nome_arquivo}"
            
        except Exception as e:
            return None, f"Erro ao gerar relatório: {str(e)}"
    
    def _obter_boletos_do_mes(self, mes, ano):
        """Obtém boletos de um mês específico"""
        boletos = self.db.obter_boletos()
        
        boletos_mes = []
        for boleto in boletos:
            try:
                data_vencimento = datetime.strptime(boleto['vencimento'], "%Y-%m-%d")
                if data_vencimento.month == mes and data_vencimento.year == ano:
                    boletos_mes.append(boleto)
            except:
                continue
        
        return boletos_mes
    
    def _criar_cabecalho(self, mes, ano):
        """Cria o cabeçalho do relatório"""
        elementos = []
        styles = getSampleStyleSheet()
        
        # Título principal
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Centro
            textColor=colors.HexColor('#2E86AB')
        )
        
        titulo = Paragraph(f"CONVENIENCIA 24 HORAS - RELATÓRIO MENSAL", titulo_style)
        elementos.append(titulo)
        
        # Subtítulo
        subtitulo_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=1,
            textColor=colors.HexColor('#A23B72')
        )
        
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        
        subtitulo = Paragraph(f"{meses[mes]} de {ano}", subtitulo_style)
        elementos.append(subtitulo)
        
        elementos.append(Spacer(1, 20))
        
        return elementos
    
    def _criar_resumo_executivo(self, boletos, mes, ano):
        """Cria a seção de resumo executivo"""
        elementos = []
        styles = getSampleStyleSheet()
        
        # Título da seção
        titulo_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.HexColor('#2E86AB')
        )
        
        titulo = Paragraph("RESUMO EXECUTIVO", titulo_style)
        elementos.append(titulo)
        
        # Calcula estatísticas
        total_boletos = len(boletos)
        total_pago = sum(b['valor'] for b in boletos if b['status'] == 'pago')
        total_pendente = sum(b['valor'] for b in boletos if b['status'] in ['pendente', 'atrasado'])
        total_atrasado = sum(b['valor'] for b in boletos if b['status'] == 'atrasado')
        
        # Tabela de resumo
        dados_resumo = [
            ['📊 Total de Boletos', f"{total_boletos}"],
            ['💰 Total Pago', f"R$ {total_pago:,.2f}"],
            ['⏳ Total Pendente', f"R$ {total_pendente:,.2f}"],
            ['🚨 Total Atrasado', f"R$ {total_atrasado:,.2f}"]
        ]
        
        tabela_resumo = Table(dados_resumo, colWidths=[3*inch, 2*inch])
        tabela_resumo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elementos.append(tabela_resumo)
        elementos.append(Spacer(1, 20))
        
        return elementos
    
    def _criar_detalhes_categoria(self, boletos):
        """Cria a seção de detalhes por categoria"""
        elementos = []
        styles = getSampleStyleSheet()
        
        # Título da seção
        titulo_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.HexColor('#2E86AB')
        )
        
        titulo = Paragraph("GASTOS POR CATEGORIA", titulo_style)
        elementos.append(titulo)
        
        # Agrupa por categoria
        categorias = {}
        for boleto in boletos:
            categoria = boleto['categoria']
            if categoria not in categorias:
                categorias[categoria] = {'total': 0, 'quantidade': 0}
            categorias[categoria]['total'] += boleto['valor']
            categorias[categoria]['quantidade'] += 1
        
        # Prepara dados para tabela
        dados_categoria = [['Categoria', 'Quantidade', 'Valor Total']]
        for categoria, dados in categorias.items():
            dados_categoria.append([
                categoria,
                str(dados['quantidade']),
                f"R$ {dados['total']:,.2f}"
            ])
        
        # Ordena por valor total (decrescente)
        if len(dados_categoria) > 1:
            dados_categoria[1:] = sorted(dados_categoria[1:], key=lambda x: float(x[2].replace('R$ ', '').replace(',', '')), reverse=True)
        
        # Cria tabela
        tabela_categoria = Table(dados_categoria, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        tabela_categoria.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#A23B72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elementos.append(tabela_categoria)
        elementos.append(Spacer(1, 20))
        
        return elementos
    
    def _criar_lista_boletos(self, boletos):
        """Cria a lista detalhada de boletos"""
        elementos = []
        styles = getSampleStyleSheet()
        
        # Título da seção
        titulo_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.HexColor('#2E86AB')
        )
        
        titulo = Paragraph("DETALHAMENTO DOS BOLETOS", titulo_style)
        elementos.append(titulo)
        
        # Prepara dados para tabela
        dados_boletos = [['Pagador', 'Categoria', 'Vencimento', 'Valor', 'Status']]
        
        for boleto in boletos:
            status_color = {
                'pago': '🟢',
                'pendente': '🟡', 
                'atrasado': '🔴'
            }
            
            dados_boletos.append([
                boleto['pagador'][:20],  # Limita tamanho
                boleto['categoria'],
                boleto['vencimento'],
                f"R$ {boleto['valor']:,.2f}",
                f"{status_color.get(boleto['status'], '⚪')} {boleto['status'].upper()}"
            ])
        
        # Cria tabela
        tabela_boletos = Table(dados_boletos, colWidths=[1.8*inch, 1.2*inch, 1*inch, 1*inch, 1*inch])
        tabela_boletos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elementos.append(tabela_boletos)
        elementos.append(Spacer(1, 20))
        
        return elementos
    
    def _criar_rodape(self):
        """Cria o rodapé do relatório"""
        elementos = []
        styles = getSampleStyleSheet()
        
        # Data de geração
        rodape_style = ParagraphStyle(
            'Rodape',
            parent=styles['Normal'],
            fontSize=8,
            alignment=1,  # Centro
            textColor=colors.grey
        )
        
        rodape = Paragraph(
            f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} | "
            f"CONVENIENCIA 24 HORAS - Sistema de Gestão de Boletos",
            rodape_style
        )
        
        elementos.append(rodape)
        
        return elementos
    
    def listar_relatorios(self):
        """Lista todos os relatórios disponíveis"""
        try:
            if not os.path.exists(self.reports_dir):
                return []
            
            relatorios = []
            for arquivo in os.listdir(self.reports_dir):
                if arquivo.endswith('.pdf'):
                    caminho = os.path.join(self.reports_dir, arquivo)
                    stat = os.stat(caminho)
                    relatorios.append({
                        'nome': arquivo,
                        'caminho': caminho,
                        'tamanho': stat.st_size,
                        'data_criacao': datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y %H:%M')
                    })
            
            return sorted(relatorios, key=lambda x: x['data_criacao'], reverse=True)
        except Exception as e:
            print(f"Erro ao listar relatórios: {e}")
            return []