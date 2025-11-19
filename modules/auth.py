## modules/auth.py - VERSÃO ATUALIZADA COM SEGURANÇA
import json
import os
from datetime import datetime

class Authentication:
    def __init__(self):
        self.users_file = "data/users.json"
        from modules.security import Security  # 🔐 IMPORT CORRIGIDO
        self.security = Security()  # 🔐 INSTÂNCIA DE SEGURANÇA
        self._criar_admin_se_nao_existir()
    
    def _criar_admin_se_nao_existir(self):
        """Cria o usuário admin se não existir"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        
        if not os.path.exists(self.users_file):
            # 🔐 AGORA COM SENHA CRIPTOGRAFADA
            users = {
                "admin": {
                    "nome": "Gerente Principal",
                    "senha": self.security.hash_password("admin123"),  # 🔐 CRIPTOGRAFADA
                    "tipo": "gerente",
                    "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "funcionario": {
                    "nome": "Funcionário Exemplo", 
                    "senha": self.security.hash_password("func123"),  # 🔐 CRIPTOGRAFADA
                    "tipo": "funcionario",
                    "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
            
            # 🔐 LOG DO EVENTO
            self.security.log_security_event("Sistema Inicializado", "Sistema", "Usuários padrão criados")
        else:
            # 🔐 MIGRAR SENHAS EXISTENTES PARA CRIPTOGRAFIA
            self._migrar_senhas_para_criptografia()
    
    def _migrar_senhas_para_criptografia(self):
        """Migra senhas em texto plano para criptografia"""
        users = self._carregar_usuarios()
        migrados = False
        
        for username, dados in users.items():
            # Se a senha não está criptografada (menos de 20 caracteres)
            if 'senha' in dados and len(dados['senha']) < 20:
                # Criptografa a senha
                dados['senha'] = self.security.hash_password(dados['senha'])
                migrados = True
                self.security.log_security_event("Senha Migrada", "Sistema", f"Usuário: {username}")
        
        if migrados:
            self._salvar_usuarios(users)
            self.security.log_security_event("Migração Concluída", "Sistema", "Todas as senhas foram criptografadas")
    
    def _carregar_usuarios(self):
        """Carrega todos os usuários do arquivo"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _salvar_usuarios(self, usuarios):
        """Salva usuários no arquivo"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)
    
    def login(self, username, password):
        """Faz login do usuário"""
        try:
            users = self._carregar_usuarios()
            
            if username in users:
                # 🔐 VERIFICA SENHA CRIPTOGRAFADA
                if self.security.verify_password(password, users[username]['senha']):
                    # 🔐 LOG DE LOGIN BEM-SUCEDIDO
                    self.security.log_security_event("Login Bem-Sucedido", username)
                    
                    return {
                        'username': username,
                        'nome': users[username]['nome'],
                        'tipo': users[username]['tipo']
                    }
                else:
                    # 🔐 LOG DE TENTATIVA FALHA
                    self.security.log_security_event("Tentativa de Login Falha", username, "Senha incorreta")
            else:
                # 🔐 LOG DE USUÁRIO NÃO ENCONTRADO
                self.security.log_security_event("Tentativa de Login Falha", username, "Usuário não existe")
            
            return None
            
        except Exception as e:
            self.security.log_security_event("Erro no Login", "Sistema", str(e))
            return None
    
    def listar_usuarios(self):
        """Lista todos os usuários no formato para a interface"""
        users = self._carregar_usuarios()
        usuarios_lista = []
        
        for username, dados in users.items():
            usuarios_lista.append({
                'username': username,
                'nome': dados['nome'],
                'tipo': dados['tipo'],
                'data_criacao': dados.get('data_criacao', 'N/A')
            })
        
        return usuarios_lista
    
    def criar_usuario(self, username, senha, nome, tipo="funcionario"):
        """Cria um novo usuário"""
        users = self._carregar_usuarios()
        
        # Verificar se usuário já existe
        if username in users:
            return False, "Usuário já existe!"
        
        # 🔐 CRIPTOGRAFA A SENHA ANTES DE SALVAR
        senha_criptografada = self.security.hash_password(senha)
        
        # Criar novo usuário
        users[username] = {
            "nome": nome,
            "senha": senha_criptografada,  # 🔐 AGORA CRIPTOGRAFADA
            "tipo": tipo,
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self._salvar_usuarios(users)
        
        # 🔐 LOG DA CRIAÇÃO DE USUÁRIO
        self.security.log_security_event("Usuário Criado", "Sistema", f"Novo {tipo}: {username}")
        
        return True, f"Usuário {nome} criado com sucesso!"
    
    def excluir_usuario(self, username):
        """Exclui um usuário"""
        users = self._carregar_usuarios()
        
        # Não permitir excluir admin
        if username == 'admin':
            return False
        
        if username in users:
            # 🔐 LOG ANTES DE EXCLUIR
            self.security.log_security_event("Usuário Excluído", "Sistema", f"Usuário: {username}")
            
            del users[username]
            self._salvar_usuarios(users)
            return True
        
        return False
    
    def editar_usuario(self, username_antigo, novo_username=None, nome=None, tipo=None):
        """Edita um usuário"""
        users = self._carregar_usuarios()
        
        if username_antigo not in users:
            return False, "Usuário não encontrado!"
        
        # Se mudou o username, precisa criar nova entrada e excluir a antiga
        if novo_username and novo_username != username_antigo:
            if novo_username in users:
                return False, "Novo username já existe!"
            
            # Copiar dados para novo username (SENHA MANTÉM CRIPTOGRAFADA)
            users[novo_username] = users[username_antigo].copy()
            # Excluir entrada antiga
            del users[username_antigo]
            
            # Atualizar outros campos se fornecidos
            if nome:
                users[novo_username]['nome'] = nome
            if tipo:
                users[novo_username]['tipo'] = tipo
        else:
            # Apenas atualizar dados (SENHA PERMANECE A MESMA)
            if nome:
                users[username_antigo]['nome'] = nome
            if tipo:
                users[username_antigo]['tipo'] = tipo
        
        self._salvar_usuarios(users)
        
        # 🔐 LOG DA EDIÇÃO
        self.security.log_security_event("Usuário Editado", "Sistema", f"Usuário: {username_antigo}")
        
        return True, "Usuário atualizado com sucesso!"
    
    def redefinir_senha(self, username, nova_senha):
        """Redefine a senha de um usuário (apenas para admin)"""
        users = self._carregar_usuarios()
        
        if username not in users:
            return False, "Usuário não encontrado!"
        
        # 🔐 CRIPTOGRAFA A NOVA SENHA
        users[username]['senha'] = self.security.hash_password(nova_senha)
        self._salvar_usuarios(users)
        
        # 🔐 LOG DA REDEFINIÇÃO
        self.security.log_security_event("Senha Redefinida", "Sistema", f"Usuário: {username}")
        
        return True, "Senha redefinida com sucesso!"