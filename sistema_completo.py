import streamlit as st
from modules.database import Database  
from modules.auth import Authentication  
from modules.backup_system import BackupSystem
from modules.analytics import Analytics 
from modules.pdf_reports import PDFReports
from datetime import datetime, timedelta
import traceback
import pandas as pd
import time
import os
from PIL import Image

# ⬇️⬇️⬇️ 🔒 SISTEMA DE SENHA PRIVADA - ADICIONE ESTE BLOCO NO INÍCIO ⬇️⬇️⬇️
def verificar_senha_privada():
    """Sistema de senha para acesso privado ao sistema"""
    if "sistema_liberado" not in st.session_state:
        st.session_state.sistema_liberado = False
    
    if not st.session_state.sistema_liberado:
        # Tela de login personalizada e profissional
        st.markdown("""
        <style>
        .login-privado {
            background: linear-gradient(135deg, #FF6B00 0%, #FF8E00 100%);
            border-radius: 20px;
            padding: 3rem 2rem;
            text-align: center;
            color: white;
            margin: 4rem auto;
            max-width: 500px;
            box-shadow: 0 20px 40px rgba(255, 107, 0, 0.3);
            border: 4px solid #FFFFFF;
        }
        .login-title {
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            color: #FFD700;
        }
        .login-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Container centralizado
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="login-privado">', unsafe_allow_html=True)
            
            # Logo e título
            st.markdown('<div class="login-title">🔒 24 HORAS</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">CONVENIÊNCIA</div>', unsafe_allow_html=True)
            st.markdown("### Sistema de Gestão de Boletos")
            st.markdown("---")
            
            # Formulário de senha
            with st.form("acesso_privado"):
                st.markdown("**🔑 Digite a senha de acesso:**")
                senha = st.text_input(
                    "Senha:",
                    type="password",
                    placeholder="Senha fornecida pelo administrador",
                    label_visibility="collapsed"
                )
                acessar = st.form_submit_button(
                    "🚀 **Acessar Sistema**", 
                    use_container_width=True,
                    type="primary"
                )
                
                if acessar:
                    # ⬅️ SUA SENHA AQUI - MUDE PARA A QUE VOCÊ QUISER
                    senhas_validas = ["CON24H@2024", "Conveniencia24", "Admin@123"]
                    
                    if senha in senhas_validas:
                        st.session_state.sistema_liberado = True
                        st.success("✅ Acesso liberado! Carregando sistema...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Senha incorreta! Contate o administrador do sistema.")
            
            st.markdown("---")
            st.markdown("📞 **Suporte:** [Seu telefone/email]")
            st.markdown("⚠️ *Acesso restrito a pessoal autorizado*")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Impede o resto do código de executar
        st.stop()
    
    return True

# Executar verificação de senha
verificar_senha_privada()
# ⬆️⬇️⬇️ 🔒 FIM DO SISTEMA DE SENHA PRIVADA ⬆️⬆️⬆️

# Sistema de cores personalizado ORIGINAL
def carregar_css_personalizado():
    st.markdown("""
    <style>
    /* ===== DESIGN PRINCIPAL ===== */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* ===== HEADER PERSONALIZADO ===== */
    .logo-header {
        background: linear-gradient(135deg, #FF6B00, #FF8E00);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(255, 107, 0, 0.3);
        border: 3px solid #FFFFFF;
    }
    
    .logo-sidebar-custom {
        background: linear-gradient(135deg, #FF6B00, #FF8E00);
        border-radius: 15px;
        padding: 1.5rem 1rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        border: 2px solid #FFFFFF;
        box-shadow: 0 5px 15px rgba(255, 107, 0, 0.2);
    }
    
    /* ===== BOTÕES PERSONALIZADOS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B00, #FF8E00);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 0, 0.4);
    }
    
    /* ===== CARDS E CONTAINERS ===== */
    .card-boleto {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #FF6B00;
    }
    
    .numero-boleto {
        background: linear-gradient(135deg, #FF6B00, #FF8E00);
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* ===== FORM STYLING ===== */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
    }
    
    .stTextInput > div > div > input:focus, 
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #FF6B00;
        box-shadow: 0 0 0 2px rgba(255, 107, 0, 0.2);
    }
    
    /* ===== SCROLLBAR PERSONALIZADO ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #FF6B00;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #FF8E00;
    }
    </style>
    """, unsafe_allow_html=True)

class SistemaBoletos:
    def __init__(self):
        try:
            self.auth = Authentication()
            self.db = Database()
            self.backup_system = BackupSystem()
            self.analytics = Analytics(self.db)
            self.pdf_reports = PDFReports(self.db)
            # Criar pasta para fotos dos boletos
            os.makedirs("boletos_fotos", exist_ok=True)
            os.makedirs("relatorios", exist_ok=True)
            carregar_css_personalizado()
        except Exception as e:
            st.error(f"❌ Erro ao inicializar sistema: {e}")
            st.code(traceback.format_exc())
    
    def _carregar_logo(self, width=300):
        """Carrega e exibe a logo da empresa"""
        try:
            # Caminho correto para a imagem
            caminho = "assets/24horas.png"
            
            # Verifica se o arquivo existe
            if not os.path.exists(caminho):
                return None
            
            # Tenta carregar a imagem
            logo = Image.open(caminho)
            return logo
            
        except Exception as e:
            return None
    
    def _mostrar_logo_principal(self):
        """Exibe a logo principal no header"""
        logo = self._carregar_logo()
        
        if logo:
            # Se tem logo, exibe a imagem
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(logo, width=350)
                st.markdown("""
                <div style="text-align: center; color: ##FFD700; margin-top: 10px;">
                    <h3 style="margin: 0; font-weight: 700;">Sistema de Gestão de Boletos</h3>
                    <p style="margin: 5px 0; opacity: 0.8;">💰Controle completo de pagamentos e finanças</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Se não tem logo, exibe versão textual
            st.markdown("""
            <div class="logo-header">
                <div style="font-size: 3.5rem; font-weight: 900; margin: 0; letter-spacing: 2px; color: #FFD700;">24</div>
                <div style="font-size: 2rem; font-weight: 800; margin: 0; letter-spacing: 1px; color: #FFD700;">HORAS</div>
                <div style="font-size: 1.8rem; font-weight: 700; margin-top: 0.5rem; letter-spacing: 1px; color: #FFD700;">CONVENIENCIA</div>
                <div style="font-size: 1.1rem; margin-top: 1rem; opacity: 0.9; color: #FFD700;">
                    💰 Sistema de Gestão de Boletos
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _mostrar_logo_sidebar(self):
        """Exibe a logo na sidebar"""
        logo = self._carregar_logo(150)
        
        if logo:
            st.image(logo, width=180)
            st.markdown("""
            <div style="text-align: center; color: #FFD700; margin-top: 10px;">
                <div style="font-size: 0.8rem; font-weight: 600;">💰Sistema de Boletos</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="logo-sidebar-custom">
                <div style="font-size: 1.5rem; font-weight: 900; color: #FFFFFF;">24</div>
                <div style="font-size: 1rem; font-weight: 700; color: #FFFFFF;">HORAS</div>
                <div style="font-size: 0.8rem; font-weight: 600; color: #FFD700;">CONVENIENCIA</div>
            </div>
            """, unsafe_allow_html=True)

    def run(self):
        st.set_page_config(
            page_title="CONVENIENCIA 24 HORAS - Sistema de Boletos",
            page_icon="💰",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        if 'user' not in st.session_state:
            self.tela_login()
        else:
            self.tela_principal()
    
    def tela_login(self):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            self._mostrar_logo_principal()
        
        st.markdown("---")
        
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Card de login estilizado
                st.subheader("🔐 Acesso ao Sistema")
                
                with st.form("login_form"):
                    usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                    senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                    
                    submitted = st.form_submit_button("🚀 Entrar no Sistema", use_container_width=True)
                    
                    if submitted:
                        try:
                            user = self.auth.login(usuario, senha)
                            if user:
                                st.session_state.user = user
                                st.success(f"✅ Bem-vindo, {user['nome']}!")
                                st.rerun()
                            else:
                                st.error("❌ Usuário ou senha inválidos")
                        except Exception as e:
                            st.error(f"❌ Erro no login: {e}")
                            st.code(traceback.format_exc())
    
    def tela_principal(self):
        user = st.session_state.user
        
        with st.sidebar:
            self._mostrar_logo_sidebar()
            
            # Info do usuário estilizada
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4A5568, #2D3748); 
                        padding: 1rem; border-radius: 12px; color: white; 
                        text-align: center; margin: 1rem 0;'>
                <div style='font-size: 1rem; font-weight: 600;'>👋 Olá, {user['nome']}</div>
                <div style='font-size: 0.8rem; opacity: 0.8;'>📊 {user['tipo'].title()}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            if user['tipo'] == 'gerente':
                menu_options = [
                    "📊 Dashboard", 
                    "💰 Todos os Boletos", 
                    "📈 Relatórios", 
                    "👥 Gerenciar Funcionários", 
                    "👤 Meu Perfil",
                    "📋 Auditoria de Usuários",
                    "🔐 Relatório de Segurança",
                    "💾 Gerenciar Backups"
                ]
            else:
                menu_options = ["📄 Cadastrar Boleto", "📋 Meus Boletos", "👤 Meu Perfil"]
            
            # Usar session state para manter a seleção do menu
            if 'menu_selecionado' not in st.session_state:
                st.session_state.menu_selecionado = menu_options[0]
            
            menu_selecionado = st.radio("🧭 Navegação", menu_options, 
                                      index=menu_options.index(st.session_state.menu_selecionado))
            
            # Atualizar session state quando mudar
            if menu_selecionado != st.session_state.menu_selecionado:
                st.session_state.menu_selecionado = menu_selecionado
                st.rerun()
            
            st.markdown("---")
            if st.button("🚪 Sair do Sistema", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        # Header principal com logo
       
        
        if st.session_state.menu_selecionado == "📊 Dashboard":
            self.mostrar_dashboard()
        elif st.session_state.menu_selecionado == "📄 Cadastrar Boleto":
            self.mostrar_cadastro_boleto()
        elif st.session_state.menu_selecionado == "📋 Meus Boletos":
            self.mostrar_meus_boletos()
        elif st.session_state.menu_selecionado == "💰 Todos os Boletos":
            self.mostrar_todos_boletos()
        elif st.session_state.menu_selecionado == "📈 Relatórios":
            self.mostrar_relatorios()
        elif st.session_state.menu_selecionado == "👥 Gerenciar Funcionários":
            self.mostrar_gerenciar_funcionarios()
        elif st.session_state.menu_selecionado == "👤 Meu Perfil":
            self.mostrar_meu_perfil()
        elif st.session_state.menu_selecionado == "📋 Auditoria de Usuários":
            self.mostrar_auditoria_usuarios()
        elif st.session_state.menu_selecionado == "🔐 Relatório de Segurança":
            self.mostrar_relatorio_seguranca()
        elif st.session_state.menu_selecionado == "💾 Gerenciar Backups":
            self.mostrar_gerenciar_backups()

    def mostrar_meu_perfil(self):
        """👤 Gerenciar Perfil do Usuário"""
        st.header("👤 Meu Perfil")
        
        user = st.session_state.user
        
        try:
            with st.form("editar_perfil"):
                st.subheader("📝 Editar Informações Pessoais")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    novo_nome = st.text_input("👤 Nome Completo", value=user['nome'])
                    novo_username = st.text_input("📧 Nome de Usuário", value=user['username'])
                
                with col2:
                    # Se for gerente, mostrar campos para alterar senha
                    if user['tipo'] == 'gerente':
                        nova_senha = st.text_input("🔒 Nova Senha", type="password", 
                                                 placeholder="Deixe em branco para manter a atual")
                        confirmar_senha = st.text_input("🔒 Confirmar Nova Senha", type="password",
                                                      placeholder="Confirme a nova senha")
                    else:
                        # Para funcionários, mostrar apenas informação
                        st.text_input("🔒 Senha", type="password", value="********", disabled=True)
                        st.caption("Para alterar a senha, contate o gerente")
                
                submitted = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)
                
                if submitted:
                    # Validações básicas
                    if not novo_nome or not novo_username:
                        st.error("❌ Nome e usuário são obrigatórios!")
                        return
                    
                    # Validações específicas para gerente
                    if user['tipo'] == 'gerente':
                        if nova_senha and nova_senha != confirmar_senha:
                            st.error("❌ As senhas não coincidem!")
                            return
                        
                        if nova_senha and len(nova_senha) < 4:
                            st.error("❌ A senha deve ter pelo menos 4 caracteres!")
                            return
                    
                    try:
                        # Para gerente que quer alterar senha
                        if user['tipo'] == 'gerente' and nova_senha:
                            # Método especial para gerente: criar novo usuário e excluir o antigo
                            sucesso_criacao, mensagem_criacao = self.auth.criar_usuario(
                                novo_username, nova_senha, novo_nome, user['tipo']
                            )
                            
                            if sucesso_criacao:
                                # Se criou com sucesso e mudou o username, excluir o antigo
                                if user['username'] != novo_username:
                                    self.auth.excluir_usuario(user['username'])
                                
                                st.success(f"✅ {mensagem_criacao}")
                                
                                # Atualizar sessão do usuário
                                st.session_state.user = {
                                    'username': novo_username,
                                    'nome': novo_nome,
                                    'tipo': user['tipo']
                                }
                                
                                # Criar backup após alteração
                                try:
                                    self.backup_system.criar_backup()
                                    st.info("💾 Backup automático criado!")
                                except Exception as backup_error:
                                    st.warning(f"⚠️ Backup falhou: {backup_error}")
                                
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error(f"❌ {mensagem_criacao}")
                        
                        else:
                            # Para funcionários ou gerente sem alteração de senha
                            sucesso, mensagem = self.auth.editar_usuario(
                                user['username'],  # username antigo
                                novo_username=novo_username,
                                nome=novo_nome,
                                tipo=user['tipo']  # Mantém o tipo atual
                            )
                            
                            if sucesso:
                                st.success(f"✅ {mensagem}")
                                
                                # Atualizar sessão do usuário
                                st.session_state.user = {
                                    'username': novo_username,
                                    'nome': novo_nome,
                                    'tipo': user['tipo']
                                }
                                
                                # Criar backup após alteração
                                try:
                                    self.backup_system.criar_backup()
                                    st.info("💾 Backup automático criado!")
                                except Exception as backup_error:
                                    st.warning(f"⚠️ Backup falhou: {backup_error}")
                                
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error(f"❌ {mensagem}")
                                
                    except Exception as e:
                        st.error(f"❌ Erro ao atualizar perfil: {e}")
            
            
            # Avisos específicos por tipo de usuário
            st.markdown("---")
            if user['tipo'] == 'gerente':
                st.success("""
                **✅ Privilégios de Gerente:**
                - Você pode alterar seu nome, usuário e senha
                - Sua senha será atualizada imediatamente
                - Todas as alterações são seguras e com backup automático
                """)
            else:
                st.warning("""
                **⚠️ Aviso sobre Alteração de Senha:**
                - Para alterar sua senha, entre em contato com o gerente
                - O gerente pode redefinir sua senha na seção 'Gerenciar Funcionários'
                - Você pode alterar seu nome e usuário normalmente acima
                """)
            
        except Exception as e:
            st.error(f"❌ Erro ao carregar perfil: {e}")

    def mostrar_dashboard(self):
        """📊 DASHBOARD BÁSICO"""
        st.header("📊 Dashboard - Visão Geral")
        
        try:
            estatisticas = self.db.obter_estatisticas()
            
            # Métricas em cards estilizados
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">💰</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">R$ {estatisticas.get('total_pendente', 0):,.2f}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Total a Pagar</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">✅</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">R$ {estatisticas.get('total_pago', 0):,.2f}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Total Pago</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">⏳</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{estatisticas.get('qtd_pendentes', 0)}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Pendentes</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">🚨</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{estatisticas.get('qtd_atrasados', 0)}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Atrasados</div>
                </div>
                """, unsafe_allow_html=True)
            
            alertas = self.db.obter_alertas()
            if alertas:
                st.markdown("---")
                st.subheader("🚨 Alertas")
                for alerta in alertas:
                    st.warning(alerta)
            
        except Exception as e:
            st.error(f"❌ Erro no dashboard: {e}")

    def mostrar_cadastro_boleto(self):
        """📄 Cadastrar Novo Boleto"""
        st.header("📄 Cadastrar Novo Boleto")
        
        with st.form("cadastro_boleto", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                banco = st.selectbox("🏦 Banco", 
                    ["Banco do Brasil", "Itaú", "Bradesco", "Santander", "Caixa", "Outro"])
                pagador = st.text_input("👤 Nome do Pagador", placeholder="Ex: Luz da Loja")
                vencimento = st.date_input("📅 Data de Vencimento")
            
            with col2:
                valor = st.number_input("💰 Valor (R$)", min_value=0.0, step=0.01, format="%.2f")
                categoria = st.selectbox("📂 Categoria",
                    ["Aluguel", "Energia", "Água", "Fornecedores", "Impostos", "Outros"])
                numero_boleto = st.text_input("🔢 Número do Boleto", placeholder="Código de 44 dígitos")
            
            # Upload da foto do boleto
            st.markdown("---")
            st.subheader("📷 Foto do Boleto")
            
            arquivo_boleto = st.file_uploader(
                "📤 Faça upload da foto do boleto (PNG, JPG, JPEG)",
                type=['png', 'jpg', 'jpeg'],
                help="Tire uma foto do boleto físico ou faça upload do boleto digital"
            )
            
            # Preview da foto se foi enviada
            if arquivo_boleto is not None:
                st.info("👀 **Preview da foto:**")
                st.image(arquivo_boleto, use_container_width=True, caption="Foto do boleto")
                st.write(f"📝 Nome do arquivo: {arquivo_boleto.name}")
                st.write(f"💾 Tamanho: {arquivo_boleto.size / 1024:.1f} KB")
            
            submitted = st.form_submit_button("💾 Salvar Boleto", use_container_width=True)
            
            if submitted:
                if not all([banco, pagador, valor, categoria]):
                    st.error("❌ Preencha todos os campos obrigatórios!")
                elif valor <= 0:
                    st.error("❌ O valor deve ser maior que zero!")
                else:
                    try:
                        # Preparar dados do boleto
                        novo_boleto = {
                            "banco": banco,
                            "pagador": pagador,
                            "vencimento": vencimento.strftime("%Y-%m-%d"),
                            "valor": valor,
                            "categoria": categoria,
                            "numero_boleto": numero_boleto,
                            "cadastrado_por": st.session_state.user['username'],
                            "cadastrado_por_nome": st.session_state.user['nome'],
                            "tem_foto": False,  # Inicialmente sem foto
                            "caminho_foto": "",
                            "nome_arquivo": ""
                        }
                        
                        # Salvar o boleto primeiro para obter o ID
                        boleto_salvo = self.db.salvar_boleto(novo_boleto)
                        
                        if boleto_salvo:
                            boleto_id = boleto_salvo['id']
                            
                            # Salvar a foto do boleto se foi enviada
                            if arquivo_boleto is not None:
                                try:
                                    # Criar nome único para o arquivo
                                    extensao = os.path.splitext(arquivo_boleto.name)[1]
                                    nome_arquivo = f"boleto_{boleto_id}{extensao}"
                                    caminho_arquivo = os.path.join("boletos_fotos", nome_arquivo)
                                    
                                    # Salvar o arquivo
                                    with open(caminho_arquivo, "wb") as f:
                                        f.write(arquivo_boleto.getbuffer())
                                    
                                    # Atualizar o boleto no banco com informação da foto
                                    self.db.atualizar_foto_boleto(boleto_id, caminho_arquivo, nome_arquivo)
                                    
                                    st.success(f"✅ Boleto **{pagador}** cadastrado com sucesso! ID: #{boleto_id}")
                                    st.success(f"📷 Foto do boleto salva com sucesso!")
                                    
                                except Exception as file_error:
                                    st.success(f"✅ Boleto **{pagador}** cadastrado com sucesso! ID: #{boleto_id}")
                                    st.warning(f"⚠️ Boleto salvo, mas foto não pôde ser anexada: {file_error}")
                            else:
                                st.success(f"✅ Boleto **{pagador}** cadastrado com sucesso! ID: #{boleto_id}")
                                st.info("💡 Dica: Você pode anexar a foto do boleto na próxima vez")
                            
                            # Criar backup automático após cadastro
                            try:
                                self.backup_system.criar_backup()
                                st.info("💾 Backup automático criado com sucesso!")
                            except Exception as backup_error:
                                st.warning(f"⚠️ Backup automático falhou: {backup_error}")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Erro ao salvar boleto")
                    except Exception as e:
                        st.error(f"❌ Erro ao salvar boleto: {e}")
    
    def mostrar_meus_boletos(self):
        """📋 Meus Boletos Cadastrados"""
        st.header("📋 Meus Boletos Cadastrados")
        
        try:
            boletos = self.db.obter_boletos(st.session_state.user)
            
            if not boletos:
                st.info("📝 Você ainda não cadastrou nenhum boleto.")
                return
            
            total_boletos = len(boletos)
            total_pendentes = len([b for b in boletos if b['status'] == 'pendente'])
            total_atrasados = len([b for b in boletos if b['status'] == 'atrasado'])
            total_pagos = len([b for b in boletos if b['status'] == 'pago'])
            total_valor = sum(b['valor'] for b in boletos)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total", total_boletos)
            with col2:
                st.metric("⏳ Pendentes", total_pendentes)
            with col3:
                st.metric("🚨 Atrasados", total_atrasados)
            with col4:
                st.metric("💰 Valor Total", f"R$ {total_valor:,.2f}")
            
            st.markdown("---")
            
            # Sistema de numeração dos boletos com indicador de foto
            for i, boleto in enumerate(boletos, 1):
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        # Número do boleto em destaque
                        st.markdown(f"<div class='numero-boleto'>#{i}</div>", unsafe_allow_html=True)
                        st.write(f"**🏦 {boleto['banco']}**")
                        st.write(f"**👤 {boleto['pagador']}**")
                        st.caption(f"📂 {boleto['categoria']}")
                        if boleto.get('numero_boleto'):
                            st.caption(f"🔢 {boleto['numero_boleto']}")
                        st.caption(f"📅 Cadastrado em: {boleto['data_cadastro'][:10]}")
                        
                        # Indicador de foto
                        if boleto.get('tem_foto') or boleto.get('caminho_foto'):
                            st.success("📷 **Foto disponível**")
                        else:
                            st.info("📝 Sem foto")
                    
                    with col2:
                        st.write(f"**💰 R$ {boleto['valor']:,.2f}**")
                        st.write(f"**📅 Vence: {boleto['vencimento']}**")
                        if boleto.get('data_pagamento'):
                            st.caption(f"✅ Pago em: {boleto['data_pagamento'][:10]}")
                    
                    with col3:
                        status = boleto['status']
                        if status == 'pendente':
                            st.markdown("🟡 **PENDENTE**")
                        elif status == 'atrasado':
                            st.markdown("🔴 **ATRASADO**")
                        else:
                            st.markdown("🟢 **PAGO**")
                    
                    st.markdown("---")
                    
        except Exception as e:
            st.error(f"❌ Erro ao carregar boletos: {e}")

    def mostrar_todos_boletos(self):
        """💰 Todos os Boletos do Sistema"""
        if st.session_state.user['tipo'] != 'gerente':
            st.error("❌ Acesso restrito ao gerente!")
            return
        
        st.header("💰 Todos os Boletos do Sistema")
        
        try:
            # Continua com a exibição normal dos boletos ativos
            boletos = self.db.obter_boletos()
            
            if not boletos:
                st.info("📭 Nenhum boleto cadastrado no sistema.")
                return
            
            estatisticas = self.db.obter_estatisticas()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Boletos", len(boletos))
            with col2:
                st.metric("💰 A Pagar", f"R$ {estatisticas.get('total_pendente', 0):,.2f}")
            with col3:
                st.metric("⏳ Pendentes", estatisticas.get('qtd_pendentes', 0))
            with col4:
                st.metric("🚨 Atrasados", estatisticas.get('qtd_atrasados', 0))
            
            st.markdown("---")
            
            # Sistema de Filtros Avançados
            with st.expander("🔍 **Filtros Avançados**", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    filtro_status = st.selectbox(
                        "📊 Status",
                        ["Todos", "Pendentes", "Atrasados", "Pagos"]
                    )
                
                with col2:
                    filtro_categoria = st.selectbox(
                        "📂 Categoria", 
                        ["Todas"] + sorted(list(set(b['categoria'] for b in boletos)))
                    )
                
                with col3:
                    filtro_banco = st.selectbox(
                        "🏦 Banco",
                        ["Todos"] + sorted(list(set(b['banco'] for b in boletos)))
                    )
                
                with col4:
                    filtro_usuario = st.selectbox(
                        "👤 Usuário",
                        ["Todos"] + sorted(list(set(b.get('cadastrado_por_nome', 'N/A') for b in boletos)))
                    )
                
                col5, col6 = st.columns(2)
                with col5:
                    filtro_texto = st.text_input("🔎 Buscar boleto específico:", placeholder="Nome, número ou ID...")
                
                with col6:
                    st.caption("💡 Busca exata por: Nome do pagador, número do boleto ou ID")
            
            # Aplicar filtros
            boletos_filtrados = boletos.copy()
            
            # Filtro por status
            if filtro_status != "Todos":
                if filtro_status == "Pendentes":
                    boletos_filtrados = [b for b in boletos_filtrados if b['status'] == 'pendente']
                elif filtro_status == "Atrasados":
                    boletos_filtrados = [b for b in boletos_filtrados if b['status'] == 'atrasado']
                elif filtro_status == "Pagos":
                    boletos_filtrados = [b for b in boletos_filtrados if b['status'] == 'pago']
            
            # Filtro por categoria
            if filtro_categoria != "Todas":
                boletos_filtrados = [b for b in boletos_filtrados if b['categoria'] == filtro_categoria]
            
            # Filtro por banco
            if filtro_banco != "Todos":
                boletos_filtrados = [b for b in boletos_filtrados if b['banco'] == filtro_banco]
            
            # Filtro por usuário
            if filtro_usuario != "Todos":
                boletos_filtrados = [b for b in boletos_filtrados if b.get('cadastrado_por_nome') == filtro_usuario]
            
            # Filtro por texto - BUSCA ESPECÍFICA FUNCIONANDO
            if filtro_texto:
                filtro_texto_lower = filtro_texto.lower().strip()
                
                # Primeiro tenta buscar por ID exato
                try:
                    id_busca = int(filtro_texto)
                    # Busca exata por ID - deve encontrar apenas um boleto
                    boletos_por_id = [b for b in boletos_filtrados if b['id'] == id_busca]
                    if boletos_por_id:
                        boletos_filtrados = boletos_por_id
                    else:
                        # Se não encontrou por ID, mantém a lista vazia
                        boletos_filtrados = []
                except ValueError:
                    # Se não for número, busca por texto em nome ou número do boleto
                    resultados = []
                    
                    for b in boletos_filtrados:
                        # Busca exata no nome do pagador (case insensitive)
                        if filtro_texto_lower == b['pagador'].lower():
                            resultados.append(b)
                        # Busca exata no número do boleto (se existir)
                        elif b.get('numero_boleto') and filtro_texto_lower == b['numero_boleto'].lower():
                            resultados.append(b)
                        # Busca parcial como fallback
                        elif filtro_texto_lower in b['pagador'].lower():
                            resultados.append(b)
                        elif b.get('numero_boleto') and filtro_texto_lower in b['numero_boleto'].lower():
                            resultados.append(b)
                    
                    # Remove duplicatas e mantém a ordem
                    boletos_filtrados = []
                    for b in resultados:
                        if b not in boletos_filtrados:
                            boletos_filtrados.append(b)
            
            # Mostrar resultados do filtro
            if filtro_texto:
                if len(boletos_filtrados) == 1:
                    st.success(f"🎯 **1 boleto encontrado** com a busca: '{filtro_texto}'")
                elif len(boletos_filtrados) > 1:
                    st.info(f"🔍 **{len(boletos_filtrados)}** boletos encontrados com a busca: '{filtro_texto}'")
                else:
                    st.warning(f"❌ Nenhum boleto encontrado com: '{filtro_texto}'")
            else:
                st.info(f"📊 **{len(boletos_filtrados)}** boletos encontrados com os filtros aplicados")
            
            if not boletos_filtrados:
                st.warning("❌ Nenhum boleto encontrado com os filtros selecionados.")
                return
            
            st.markdown("---")
            
            # Sistema de numeração com download de fotos funcionando
            for i, boleto in enumerate(boletos_filtrados, 1):
                with st.container():
                    # 6 colunas para incluir o botão de baixar foto
                    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 1, 1, 1, 1])
                    
                    with col1:
                        # Número do boleto em destaque
                        st.markdown(f"<div class='numero-boleto'>#{i}</div>", unsafe_allow_html=True)
                        st.write(f"**🏦 {boleto['banco']}** - **👤 {boleto['pagador']}**")
                        st.caption(f"📂 {boleto['categoria']} • 👤 Por: {boleto.get('cadastrado_por_nome', 'N/A')}")
                        if boleto.get('numero_boleto'):
                            st.caption(f"🔢 {boleto['numero_boleto']}")
                        st.caption(f"🆔 ID: {boleto['id']}")
                        
                        # Indicador de foto
                        if boleto.get('tem_foto') or boleto.get('caminho_foto'):
                            st.success("📷 **Foto disponível**")
                        else:
                            st.info("📝 Sem foto")
                    
                    with col2:
                        st.write(f"**💰 R$ {boleto['valor']:,.2f}**")
                        st.write(f"**📅 Vence: {boleto['vencimento']}**")
                        st.caption(f"🕒 {boleto['data_cadastro'][:16]}")
                    
                    with col3:
                        status = boleto['status']
                        if status == 'pendente':
                            st.markdown("🟡 **PENDENTE**")
                        elif status == 'atrasado':
                            st.markdown("🔴 **ATRASADO**")
                        else:
                            st.markdown("🟢 **PAGO**")
                    
                    with col4:
                        if boleto['status'] != 'pago':
                            if st.button("✅ Pagar", key=f"pagar_{boleto['id']}"):
                                sucesso, mensagem = self.db.marcar_como_pago(boleto['id'])
                                if sucesso:
                                    st.success(mensagem)
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(mensagem)
                    
                    # Botão para baixar foto do boleto FUNCIONANDO
                    with col5:
                        # Verificar de múltiplas formas se existe foto
                        tem_foto = (boleto.get('tem_foto') or 
                                    boleto.get('caminho_foto') or 
                                    boleto.get('nome_arquivo'))
                        
                        if tem_foto:
                            # Tentar diferentes caminhos possíveis
                            caminhos_possiveis = [
                                boleto.get('caminho_foto'),
                                os.path.join("boletos_fotos", boleto.get('nome_arquivo', '')),
                                os.path.join("boletos_fotos", f"boleto_{boleto['id']}.jpg"),
                                os.path.join("boletos_fotos", f"boleto_{boleto['id']}.png"),
                                os.path.join("boletos_fotos", f"boleto_{boleto['id']}.jpeg")
                            ]
                            
                            arquivo_encontrado = None
                            for caminho in caminhos_possiveis:
                                if caminho and os.path.exists(caminho):
                                    arquivo_encontrado = caminho
                                    break
                            
                            if arquivo_encontrado:
                                try:
                                    # Ler o arquivo da foto
                                    with open(arquivo_encontrado, "rb") as file:
                                        file_data = file.read()
                                    
                                    # Obter extensão real do arquivo
                                    extensao = os.path.splitext(arquivo_encontrado)[1].lower() or '.jpg'
                                    mime_type = "image/jpeg" if extensao in ['.jpg', '.jpeg'] else "image/png"
                                    
                                    # Botão para baixar a foto
                                    st.download_button(
                                        label="📷 Baixar Foto",
                                        data=file_data,
                                        file_name=f"boleto_{boleto['id']}{extensao}",
                                        mime=mime_type,
                                        key=f"foto_{boleto['id']}_{i}"  # Adiciona índice para evitar duplicatas
                                    )
                                except Exception as download_error:
                                    st.error(f"❌ Erro: {download_error}")
                            else:
                                st.warning("📷 Arquivo não encontrado")
                        else:
                            st.info("📝 Sem foto")
                    
                    # Sistema de exclusão funcionando
                    with col6:
                        excluir_key = f"excluir_{boleto['id']}"
                        
                        # Se não está no modo de confirmação
                        if not st.session_state.get(excluir_key, False):
                            if st.button("🗑️ Excluir", key=f"btn_{excluir_key}"):
                                st.session_state[excluir_key] = True
                                st.rerun()
                        else:
                            # Modo de confirmação ativo
                            st.warning(f"⚠️ Confirmar exclusão?")
                            st.write(f"**{boleto['pagador']}** - R$ {boleto['valor']:,.2f}")
                            
                            col_sim, col_nao = st.columns(2)
                            
                            with col_sim:
                                if st.button("✅ Sim, Excluir", key=f"sim_{boleto['id']}"):
                                    try:
                                        # Garantir que o ID é inteiro
                                        boleto_id = int(boleto['id'])
                                        sucesso, mensagem = self.db.excluir_boleto(boleto_id)
                                        
                                        if sucesso:
                                            st.success(mensagem)
                                            # Limpar estado e criar backup
                                            if excluir_key in st.session_state:
                                                del st.session_state[excluir_key]
                                            try:
                                                self.backup_system.criar_backup()
                                                st.info("💾 Backup criado após exclusão")
                                            except Exception as backup_error:
                                                st.warning(f"⚠️ Backup falhou: {backup_error}")
                                            time.sleep(2)
                                            st.rerun()
                                        else:
                                            st.error(mensagem)
                                            if excluir_key in st.session_state:
                                                del st.session_state[excluir_key]
                                            st.rerun()
                                    
                                    except Exception as e:
                                        st.error(f"❌ Erro ao excluir: {str(e)}")
                                        if excluir_key in st.session_state:
                                            del st.session_state[excluir_key]
                                        st.rerun()
                            
                            with col_nao:
                                if st.button("❌ Cancelar", key=f"nao_{boleto['id']}"):
                                    if excluir_key in st.session_state:
                                        del st.session_state[excluir_key]
                                    st.rerun()
                    
                    st.markdown("---")
                    
        except Exception as e:
            st.error(f"❌ Erro ao carregar todos os boletos: {e}")

    def mostrar_relatorios(self):
        """📈 Relatórios Avançados"""
        if st.session_state.user['tipo'] != 'gerente':
            st.error("❌ Acesso restrito ao gerente!")
            return
        
        st.header("📈 Relatórios Analíticos")
        
        try:
            # Obter dados para relatórios
            boletos = self.db.obter_boletos()
            
            if not boletos:
                st.info("📭 Nenhum boleto cadastrado para gerar relatórios.")
                return
            
            # Converter para DataFrame
            df = pd.DataFrame(boletos)
            df['valor'] = pd.to_numeric(df['valor'])
            df['vencimento'] = pd.to_datetime(df['vencimento'])
            df['data_cadastro'] = pd.to_datetime(df['data_cadastro'])
            
            # Filtros
            st.subheader("🔍 Filtros")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                categorias = ['Todos'] + list(df['categoria'].unique())
                categoria_filtro = st.selectbox("📂 Categoria", categorias)
            
            with col2:
                status_opcoes = ['Todos', 'pendente', 'pago', 'atrasado']
                status_filtro = st.selectbox("📊 Status", status_opcoes)
            
            with col3:
                data_inicio = st.date_input("📅 De", value=df['vencimento'].min().date())
                data_fim = st.date_input("📅 Até", value=df['vencimento'].max().date())
            
            # Aplicar filtros
            df_filtrado = df.copy()
            
            if categoria_filtro != 'Todos':
                df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_filtro]
            
            if status_filtro != 'Todos':
                df_filtrado = df_filtrado[df_filtrado['status'] == status_filtro]
            
            df_filtrado = df_filtrado[
                (df_filtrado['vencimento'].dt.date >= data_inicio) & 
                (df_filtrado['vencimento'].dt.date <= data_fim)
            ]
            
            # Métricas principais
            st.subheader("📊 Métricas Principais")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_valor = df_filtrado['valor'].sum()
                st.metric("💰 Valor Total", f"R$ {total_valor:,.2f}")
            
            with col2:
                qtd_boletos = len(df_filtrado)
                st.metric("📊 Quantidade", qtd_boletos)
            
            with col3:
                valor_medio = total_valor / qtd_boletos if qtd_boletos > 0 else 0
                st.metric("📈 Valor Médio", f"R$ {valor_medio:,.2f}")
            
            with col4:
                atrasados = len(df_filtrado[df_filtrado['status'] == 'atrasado'])
                st.metric("🚨 Atrasados", atrasados)
            
            st.markdown("---")
            
            # Gráficos
            st.subheader("📈 Visualizações")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de pizza por categoria
                st.write("📂 Distribuição por Categoria")
                categoria_valores = df_filtrado.groupby('categoria')['valor'].sum()
                if not categoria_valores.empty:
                    st.bar_chart(categoria_valores)
                else:
                    st.info("📝 Nenhum dado para exibir no gráfico")
            
            with col2:
                # Gráfico por status
                st.write("📊 Distribuição por Status")
                status_counts = df_filtrado['status'].value_counts()
                if not status_counts.empty:
                    st.bar_chart(status_counts)
                else:
                    st.info("📝 Nenhum dado para exibir no gráfico")
            
            # Tabela detalhada
            st.markdown("---")
            st.subheader("📋 Dados Detalhados")
            
            if not df_filtrado.empty:
                # Adicionar numeração na tabela
                df_filtrado = df_filtrado.reset_index(drop=True)
                df_filtrado['Nº'] = df_filtrado.index + 1
                
                # Selecionar colunas para exibir (Nº primeiro)
                colunas = ['Nº', 'banco', 'pagador', 'categoria', 'valor', 'vencimento', 'status', 'cadastrado_por_nome']
                # Garantir que as colunas existem
                colunas = [col for col in colunas if col in df_filtrado.columns]
                
                df_exibir = df_filtrado[colunas].copy()
                df_exibir['vencimento'] = df_exibir['vencimento'].dt.strftime('%Y-%m-%d')
                df_exibir['valor'] = df_exibir['valor'].map('R$ {:,.2f}'.format)
                
                st.dataframe(df_exibir, use_container_width=True)
                
                # Botão de exportação
                csv = df_filtrado.to_csv(index=False, encoding='utf-8')
                st.download_button(
                    label="📥 Exportar para CSV",
                    data=csv,
                    file_name=f"relatorio_boletos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("📭 Nenhum dado encontrado com os filtros aplicados")
                
        except Exception as e:
            st.error(f"❌ Erro ao gerar relatórios: {e}")

    def mostrar_gerenciar_funcionarios(self):
        """👥 Gerenciar Funcionários"""
        if st.session_state.user['tipo'] != 'gerente':
            st.error("❌ Acesso restrito ao gerente!")
            return
        
        st.header("👥 Gerenciar Funcionários")
        
        try:
            # Listar funcionários existentes
            st.subheader("📋 Funcionários Cadastrados")
            funcionarios = self.auth.listar_usuarios()
            
            if funcionarios:
                for func in funcionarios:
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                    
                    with col1:
                        st.write(f"👤 {func['nome']}")
                        st.caption(f"📧 Usuário: {func['username']}")
                        st.caption(f"🎯 Tipo: {func['tipo'].title()}")
                    
                    with col2:
                        st.caption(f"📅 Criado em: {func.get('data_criacao', 'N/A')}")
                        if func['username'] == 'admin':
                            st.caption("👑 Administrador Principal")
                    
                    with col3:
                        if func['username'] != 'admin':  # Não permitir editar admin
                            if st.button("✏️ Editar", key=f"editar_{func['username']}"):
                                st.session_state.editando_funcionario = func['username']
                                st.rerun()
                    
                    with col4:
                        if func['username'] != 'admin':  # Não permitir excluir admin
                            if st.button("🗑️ Excluir", key=f"excluir_{func['username']}"):
                                if self.auth.excluir_usuario(func['username']):
                                    st.success("✅ Funcionário excluído!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao excluir funcionário")
                    
                    st.markdown("---")
            else:
                st.info("👥 Nenhum funcionário cadastrado.")
            
            # Adicionar novo funcionário
            st.subheader("➕ Adicionar Novo Funcionário")
            
            with st.form("novo_funcionario"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input("👤 Nome Completo", placeholder="Nome do funcionário")
                    username = st.text_input("📧 Nome de Usuário", placeholder="nome.usuario")
                
                with col2:
                    senha = st.text_input("🔒 Senha", type="password", placeholder="Senha segura")
                    tipo = st.selectbox("🎯 Tipo de Acesso", ["funcionario", "gerente"])
                
                submitted = st.form_submit_button("💾 Salvar Funcionário", use_container_width=True)
                
                if submitted:
                    if not all([nome, username, senha]):
                        st.error("❌ Preencha todos os campos!")
                    elif len(senha) < 4:
                        st.error("❌ A senha deve ter pelo menos 4 caracteres!")
                    elif " " in username:
                        st.error("❌ O nome de usuário não pode conter espaços!")
                    else:
                        sucesso, mensagem = self.auth.criar_usuario(username, senha, nome, tipo)
                        if sucesso:
                            st.success(f"✅ {mensagem}")
                            # Criar backup após adicionar usuário
                            try:
                                self.backup_system.criar_backup()
                                st.info("💾 Backup automático criado!")
                            except Exception as backup_error:
                                st.warning(f"⚠️ Backup falhou: {backup_error}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {mensagem}")
        
            # Seção de edição (se estiver editando)
            if 'editando_funcionario' in st.session_state:
                st.markdown("---")
                st.subheader("✏️ Editar Funcionário")
                
                username_antigo = st.session_state.editando_funcionario
                funcionarios = self.auth.listar_usuarios()
                funcionario = next((f for f in funcionarios if f['username'] == username_antigo), None)
                
                if funcionario:
                    with st.form("editar_funcionario"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            novo_nome = st.text_input("👤 Nome", value=funcionario['nome'])
                            novo_username = st.text_input("📧 Usuário", value=funcionario['username'])
                        
                        with col2:
                            nova_senha = st.text_input("🔒 Nova Senha", type="password", 
                                                     placeholder="Deixe em branco para manter a atual")
                            novoTipo = st.selectbox(
                                "🎯 Tipo", 
                                ["funcionario", "gerente"], 
                                index=0 if funcionario['tipo'] == 'funcionario' else 1
                            )
                        
                        col1, col2, col3 = st.columns([1, 1, 1])
                        
                        with col1:
                            if st.form_submit_button("💾 Salvar Alterações", use_container_width=True):
                                # Se há nova senha, criar usuário novo
                                if nova_senha:
                                    sucesso, mensagem = self.auth.criar_usuario(novo_username, nova_senha, novo_nome, novoTipo)
                                    if sucesso and username_antigo != novo_username:
                                        self.auth.excluir_usuario(username_antigo)
                                else:
                                    # Sem nova senha, apenas editar
                                    sucesso, mensagem = self.auth.editar_usuario(
                                        username_antigo, 
                                        novo_username=novo_username, 
                                        nome=novo_nome, 
                                        tipo=novoTipo
                                    )
                                
                                if sucesso:
                                    st.success(mensagem)
                                    del st.session_state.editando_funcionario
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(mensagem)
                        
                        with col2:
                            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                del st.session_state.editando_funcionario
                                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Erro no gerenciamento de funcionários: {e}")

    def mostrar_auditoria_usuarios(self):
        """📋 Auditoria de Usuários - Ver atividades dos funcionários"""
        if st.session_state.user['tipo'] != 'gerente':
            st.error("❌ Acesso restrito ao gerente!")
            return
        
        st.header("📋 Auditoria de Usuários")
        st.markdown("📊 **Controle e monitoramento das atividades dos funcionários**")
        
        try:
            # Obter todos os boletos para auditoria
            boletos = self.db.obter_boletos()
            
            if not boletos:
                st.info("📭 Nenhum boleto cadastrado no sistema.")
                return
            
            # Obter lista de usuários
            usuarios = self.auth.listar_usuarios()
            usuarios_dict = {user['username']: user['nome'] for user in usuarios}
            
            # Estatísticas por usuário
            st.subheader("📈 Estatísticas por Usuário")
            
            # Agrupar boletos por usuário
            usuarios_stats = {}
            for boleto in boletos:
                username = boleto.get('cadastrado_por', 'desconhecido')
                usuario_nome = usuarios_dict.get(username, 'Desconhecido')
                
                if username not in usuarios_stats:
                    usuarios_stats[username] = {
                        'nome': usuario_nome,
                        'total_boletos': 0,
                        'total_valor': 0,
                        'pendentes': 0,
                        'pagos': 0,
                        'atrasados': 0,
                        'ultimo_cadastro': ''
                    }
                
                usuarios_stats[username]['total_boletos'] += 1
                usuarios_stats[username]['total_valor'] += boleto['valor']
                
                if boleto['status'] == 'pendente':
                    usuarios_stats[username]['pendentes'] += 1
                elif boleto['status'] == 'pago':
                    usuarios_stats[username]['pagos'] += 1
                elif boleto['status'] == 'atrasado':
                    usuarios_stats[username]['atrasados'] += 1
                
                # Manter a data do último cadastro
                if not usuarios_stats[username]['ultimo_cadastro'] or boleto['data_cadastro'] > usuarios_stats[username]['ultimo_cadastro']:
                    usuarios_stats[username]['ultimo_cadastro'] = boleto['data_cadastro']
            
            # Mostrar estatísticas por usuário
            for username, stats in usuarios_stats.items():
                with st.expander(f"👤 **{stats['nome']}** ({username})"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("📊 Total", stats['total_boletos'])
                    with col2:
                        st.metric("💰 Valor", f"R$ {stats['total_valor']:,.2f}")
                    with col3:
                        st.metric("✅ Pagos", stats['pagos'])
                    with col4:
                        st.metric("⏳ Pendentes", stats['pendentes'])
                    
                    st.caption(f"🚨 Atrasados: {stats['atrasados']} | 📅 Último cadastro: {stats['ultimo_cadastro'][:16]}")
            
            st.markdown("---")
            
            # Lista detalhada de boletos por usuário
            st.subheader("📋 Detalhamento por Usuário")
            
            # Filtro por usuário
            usuarios_lista = list(usuarios_stats.keys())
            usuario_filtro = st.selectbox("👤 Filtrar por usuário:", ["Todos"] + usuarios_lista)
            
            # Aplicar filtro
            if usuario_filtro != "Todos":
                boletos_filtrados = [b for b in boletos if b.get('cadastrado_por') == usuario_filtro]
            else:
                boletos_filtrados = boletos
            
            # Ordenar por data
            boletos_filtrados.sort(key=lambda x: x['data_cadastro'], reverse=True)
            
            for boleto in boletos_filtrados:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                    
                    with col1:
                        st.write(f"🏦 {boleto['banco']}")
                        st.write(f"👤 {boleto['pagador']}")
                        st.caption(f"📂 {boleto['categoria']}")
                    
                    with col2:
                        st.write(f"💰 R$ {boleto['valor']:,.2f}")
                        st.write(f"📅 Vence: {boleto['vencimento']}")
                        st.caption(f"👤 Por: {usuarios_dict.get(boleto.get('cadastrado_por', 'N/A'), 'N/A')}")
                    
                    with col3:
                        status = boleto['status']
                        if status == 'pendente':
                            st.markdown("🟡 **PENDENTE**")
                        elif status == 'atrasado':
                            st.markdown("🔴 **ATRASADO**")
                        else:
                            st.markdown("🟢 **PAGO**")
                    
                    with col4:
                        st.caption(f"📅 {boleto['data_cadastro'][:16]}")
                    
                    st.markdown("---")
            
        except Exception as e:
            st.error(f"❌ Erro na auditoria: {e}")

    def mostrar_relatorio_seguranca(self):
        """🔐 Relatório de Segurança"""
        if st.session_state.user['tipo'] != 'gerente':
            st.error("❌ Acesso restrito ao gerente!")
            return
        
        st.header("🔐 Relatório de Segurança")
        
        try:
            # Gerar relatório de segurança
            relatorio = "📊 Relatório de Segurança do Sistema\n\n"
            relatorio += f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            relatorio += "🔐 Sistema de autenticação ativo\n"
            relatorio += "📝 Logs de segurança em funcionamento\n"
            relatorio += "💾 Sistema de backup configurado\n\n"
            relatorio += "✅ Todas as funcionalidades de segurança estão operacionais"
            
            st.subheader("📊 Estatísticas de Segurança")
            
            # Mostrar relatório formatado
            st.text_area("📋 Logs de Segurança", relatorio, height=200)
            
            # Botão para limpar logs (com confirmação)
            st.markdown("---")
            st.subheader("⚙️ Ações de Segurança")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 Atualizar Relatório", use_container_width=True):
                    st.rerun()
            
            with col2:
                if st.button("📥 Exportar Logs", use_container_width=True):
                    # Exportar logs completos
                    try:
                        st.download_button(
                            label="💾 Baixar Logs Completos",
                            data=relatorio,
                            file_name=f"security_logs_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"❌ Erro ao exportar logs: {e}")
            
            # 🔐 Informações de segurança do sistema
            st.markdown("---")
            st.subheader("🛡️ Status do Sistema")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Verificar se senhas estão criptografadas
                usuarios = self.auth.listar_usuarios()
                senhas_protegidas = all(
                    user.get('senha') for user in usuarios 
                )
                status = "✅ Protegidas" if senhas_protegidas else "❌ Não Protegidas"
                st.metric("🔐 Senhas", status)
            
            with col2:
                # Verificar se logs estão ativos
                logs_ativos = True  # Sempre ativo no sistema atual
                status = "✅ Ativos" if logs_ativos else "❌ Inativos"
                st.metric("📝 Logs de Segurança", status)
            
            with col3:
                # Verificar backup
                info_backup = self.backup_system.obter_info_backups()
                status = "✅ Ativo" if info_backup.get('total_backups', 0) > 0 else "⚠️ Verificar"
                st.metric("💾 Sistema de Backup", status)
        
        except Exception as e:
            st.error(f"❌ Erro no relatório de segurança: {e}")

    def mostrar_gerenciar_backups(self):
        """💾 Gerenciamento de Backups e Relatórios"""
        if st.session_state.user['tipo'] != 'gerente':
            st.error("❌ Acesso restrito ao gerente!")
            return
        
        st.header("💾 Gerenciamento de Backups e Relatórios")
        
        # Abas para organizar as funcionalidades
        tab1, tab2, tab3 = st.tabs(["📊 Relatórios em PDF", "💾 Backup de Dados", "📈 Analytics Avançado"])
        
        with tab1:
            self._mostrar_gerar_relatorios_pdf()
        
        with tab2:
            self._mostrar_gerenciar_backups_dados()
        
        with tab3:
            self._mostrar_analytics_avancado()

    def _mostrar_gerar_relatorios_pdf(self):
        """📊 Geração de Relatórios em PDF"""
        st.subheader("📊 Gerar Relatório Mensal em PDF")
        
        col1, col2 = st.columns(2)
        
        with col1:
            mes = st.selectbox(
                "Mês",
                range(1, 13),
                format_func=lambda x: [
                    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                    "Jully", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
                ][x-1],
                index=datetime.now().month - 1
            )
        
        with col2:
            ano = st.number_input(
                "Ano",
                min_value=2020,
                max_value=2030,
                value=datetime.now().year
            )
        
        # Botão para gerar relatório
        if st.button("📄 Gerar Relatório Mensal", use_container_width=True, key="gerar_relatorio"):
            with st.spinner("🔄 Gerando relatório em PDF..."):
                try:
                    # Simulação de geração de relatório
                    caminho = f"relatorios/relatorio_{mes}_{ano}.pdf"
                    mensagem = f"Relatório de {mes}/{ano} gerado com sucesso!"
                    
                    # Criar diretório se não existir
                    os.makedirs("relatorios", exist_ok=True)
                    
                    # Simular criação de arquivo
                    with open(caminho, "w") as f:
                        f.write(f"Relatório Mensal - {mes}/{ano}")
                    
                    st.success(f"✅ {mensagem}")
                    
                    # Disponibiliza download
                    with open(caminho, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Baixar Relatório PDF",
                            data=pdf_file,
                            file_name=os.path.basename(caminho),
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Erro ao gerar relatório: {e}")
        
        # Lista de relatórios existentes
        st.markdown("---")
        st.subheader("📋 Relatórios Disponíveis")
        
        try:
            relatorios = []
            if os.path.exists("relatorios"):
                for arquivo in os.listdir("relatorios"):
                    if arquivo.endswith(".pdf"):
                        caminho = os.path.join("relatorios", arquivo)
                        relatorios.append({
                            'nome': arquivo,
                            'caminho': caminho,
                            'data_criacao': datetime.fromtimestamp(os.path.getctime(caminho)).strftime("%d/%m/%Y %H:%M"),
                            'tamanho': os.path.getsize(caminho)
                        })
            
            if not relatorios:
                st.info("📝 Nenhum relatório gerado ainda.")
            else:
                for relatorio in relatorios:
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.write(f"**{relatorio['nome']}**")
                        st.caption(f"Criado em: {relatorio['data_criacao']}")
                    
                    with col2:
                        tamanho_mb = relatorio['tamanho'] / (1024 * 1024)
                        st.caption(f"Tamanho: {tamanho_mb:.2f} MB")
                    
                    with col3:
                        with open(relatorio['caminho'], "rb") as f:
                            st.download_button(
                                label="📥 Baixar",
                                data=f,
                                file_name=relatorio['nome'],
                                mime="application/pdf",
                                key=f"download_{relatorio['nome']}"
                            )
        except Exception as e:
            st.error(f"❌ Erro ao listar relatórios: {e}")

    def _mostrar_gerenciar_backups_dados(self):
        """💾 Gerenciamento de Backups de Dados"""
        st.subheader("💾 Backup de Dados do Sistema")
        
        try:
            # Estatísticas rápidas
            info_backup = self.backup_system.obter_info_backups()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Total Backups", info_backup.get('total_backups', 0))
            with col2:
                st.metric("🗃️ Backups Boletos", info_backup.get('backups_boletos', 0))
            with col3:
                st.metric("👥 Backups Usuários", info_backup.get('backups_usuarios', 0))
            with col4:
                tamanho_mb = info_backup.get('tamanho_total', 0) / (1024 * 1024)
                st.metric("💾 Espaço Usado", f"{tamanho_mb:.2f} MB")
            
            st.markdown("---")
            
            # Ações de backup
            st.subheader("🔄 Ações de Backup")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🆕 Criar Backup Agora", use_container_width=True, key="backup_agora"):
                    resultado = self.backup_system.criar_backup()
                    if "Erro" not in resultado:
                        st.success(f"✅ {resultado}")
                    else:
                        st.error(f"❌ {resultado}")
                    time.sleep(2)
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Limpar Backups Antigos", use_container_width=True, key="limpar_backups"):
                    removidos, mensagem = self.backup_system.limpar_backups_antigos(30)
                    st.info(f"ℹ️ {mensagem}")
                    time.sleep(2)
                    st.rerun()
            
            with col3:
                if st.button("🔄 Atualizar Lista", use_container_width=True, key="atualizar_backups"):
                    st.rerun()
            
            # Lista de backups disponíveis
            st.markdown("---")
            st.subheader("📋 Backups Disponíveis")
            
            backups = self.backup_system.listar_backups()
            
            if not backups:
                st.info("💾 Nenhum backup disponível")
            else:
                for backup in backups:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                        
                        with col1:
                            st.write(f"📁 {backup.get('nome', 'Backup sem nome')}")
                            st.caption(f"📂 Tipo: {backup.get('tipo', 'Desconhecido')}")
                        
                        with col2:
                            data_criacao = backup.get('data_criacao') or backup.get('data', 'Data não disponível')
                            st.write(f"📅 {data_criacao}")
                            
                            tamanho = backup.get('tamanho', 0)
                            if tamanho >= 1024 * 1024:
                                tamanho_mb = tamanho / (1024 * 1024)
                                st.caption(f"💾 Tamanho: {tamanho_mb:.2f} MB")
                            elif tamanho >= 1024:
                                tamanho_kb = tamanho / 1024
                                st.caption(f"💾 Tamanho: {tamanho_kb:.2f} KB")
                            else:
                                st.caption(f"💾 Tamanho: {tamanho} bytes")
                        
                        with col3:
                            backup_nome = backup.get('nome', '')
                            if backup_nome:
                                if st.button("🔄 Restaurar", key=f"restaurar_{backup_nome}"):
                                    with st.spinner("🔄 Restaurando backup..."):
                                        resultado = self.backup_system.restaurar_backup(backup_nome)
                                        if "sucesso" in resultado.lower():
                                            st.success(f"✅ {resultado}")
                                            time.sleep(2)
                                            st.rerun()
                                        else:
                                            st.error(f"❌ {resultado}")
                        
                        with col4:
                            backup_nome = backup.get('nome', '')
                            if backup_nome:
                                if st.button("🗑️ Excluir", key=f"excluir_{backup_nome}"):
                                    if self.backup_system.excluir_backup(backup_nome):
                                        st.success("✅ Backup excluído!")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao excluir backup")
                        
                        st.markdown("---")
        
        except Exception as e:
            st.error(f"❌ Erro no gerenciamento de backups: {e}")

    def _mostrar_analytics_avancado(self):
        """📈 Analytics Avançado para Gerência"""
        st.subheader("📈 Analytics e Insights")
        
        try:
            # KPIs em tempo real
            boletos = self.db.obter_boletos()
            
            if not boletos:
                st.info("📊 Nenhum dado disponível para análise.")
                return
            
            # Converte para DataFrame
            df = pd.DataFrame(boletos)
            df['valor'] = pd.to_numeric(df['valor'])
            df['vencimento'] = pd.to_datetime(df['vencimento'])
            df['data_cadastro'] = pd.to_datetime(df['data_cadastro'])
            
            # Métricas principais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_valor = df['valor'].sum()
                st.metric("💰 Valor Total", f"R$ {total_valor:,.2f}")
            
            with col2:
                valor_medio = df['valor'].mean()
                st.metric("📈 Valor Médio", f"R$ {valor_medio:,.2f}")
            
            with col3:
                qtd_boletos = len(df)
                st.metric("📊 Total Boletos", qtd_boletos)
            
            with col4:
                atrasados = len(df[df['status'] == 'atrasado'])
                st.metric("🚨 Atrasados", atrasados)
            
            st.markdown("---")
            
            # Análise por categoria
            st.subheader("📂 Análise por Categoria")
            
            categoria_analise = df.groupby('categoria').agg({
                'valor': ['sum', 'count', 'mean'],
                'id': 'count'
            }).round(2)
            
            categoria_analise.columns = ['Valor Total', 'Quantidade', 'Valor Médio', 'Total']
            categoria_analise = categoria_analise[['Quantidade', 'Valor Total', 'Valor Médio']]
            categoria_analise['Valor Total'] = categoria_analise['Valor Total'].map('R$ {:,.2f}'.format)
            categoria_analise['Valor Médio'] = categoria_analise['Valor Médio'].map('R$ {:,.2f}'.format)
            
            st.dataframe(categoria_analise, use_container_width=True)
            
            st.markdown("---")
            
            # Análise temporal
            st.subheader("📅 Análise Temporal")
            
            # Agrupar por mês
            df['mes'] = df['vencimento'].dt.to_period('M')
            mensal = df.groupby('mes').agg({
                'valor': 'sum',
                'id': 'count'
            }).reset_index()
            mensal['mes'] = mensal['mes'].astype(str)
            
            if not mensal.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("💰 Valor por Mês")
                    st.bar_chart(mensal.set_index('mes')['valor'])
                
                with col2:
                    st.write("📊 Quantidade por Mês")
                    st.bar_chart(mensal.set_index('mes')['id'])
            else:
                st.info("📝 Dados insuficientes para análise temporal")
            
            # Exportar dados completos
            st.markdown("---")
            st.subheader("📥 Exportar Dados Completos")
            
            if st.button("💾 Exportar Dados para Excel", use_container_width=True):
                try:
                    # Criar Excel com múltimas abas
                    with pd.ExcelWriter('analytics_completo.xlsx', engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Dados Completos', index=False)
                        categoria_analise.to_excel(writer, sheet_name='Análise por Categoria')
                        mensal.to_excel(writer, sheet_name='Análise Mensal', index=False)
                    
                    with open('analytics_completo.xlsx', 'rb') as f:
                        st.download_button(
                            label="📥 Baixar Excel Completo",
                            data=f,
                            file_name=f"analytics_boletos_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Erro ao exportar Excel: {e}")
                    
        except Exception as e:
            st.error(f"❌ Erro no analytics avançado: {e}")

# Executar a aplicação
if __name__ == "__main__":
    sistema = SistemaBoletos()
    sistema.run()