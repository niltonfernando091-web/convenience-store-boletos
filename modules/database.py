# modules/database.py
import json
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.boletos_file = "data/boletos.json"
        self.users_file = "data/users.json"
        self._criar_arquivos_se_nao_existirem()
    
    def _criar_arquivos_se_nao_existirem(self):
        """Cria os arquivos de dados se não existirem"""
        # Garante que a pasta data existe
        os.makedirs(os.path.dirname(self.boletos_file), exist_ok=True)
        
        # Cria arquivo de boletos vazio
        if not os.path.exists(self.boletos_file):
            with open(self.boletos_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)
        
        # Cria arquivo de usuários com admin padrão se não existir
        if not os.path.exists(self.users_file):
            users = {
                "admin": {
                    "nome": "Gerente Principal",
                    "senha": "admin123",
                    "tipo": "gerente",
                    "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "funcionario": {
                    "nome": "Funcionário Teste", 
                    "senha": "func123",
                    "tipo": "funcionario",
                    "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
    
    # ===== FUNÇÕES DE BOLETOS =====
    
    def salvar_boleto(self, boleto_data):
        """Salva um novo boleto no banco de dados"""
        try:
            with open(self.boletos_file, 'r', encoding='utf-8') as f:
                boletos = json.load(f)
            
            # Adiciona dados automáticos
            boleto_data['id'] = len(boletos) + 1
            boleto_data['data_cadastro'] = self._data_atual()
            boleto_data['status'] = 'pendente'
            
            boletos.append(boleto_data)
            
            # Salva no arquivo
            with open(self.boletos_file, 'w', encoding='utf-8') as f:
                json.dump(boletos, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Boleto salvo: {boleto_data['pagador']} - ID: {boleto_data['id']}")
            return boleto_data
            
        except Exception as e:
            print(f"❌ Erro ao salvar boleto: {e}")
            return None

    def atualizar_foto_boleto(self, boleto_id, caminho_foto, nome_arquivo):
        """Atualiza informações da foto no boleto"""
        try:
            with open(self.boletos_file, 'r', encoding='utf-8') as f:
                boletos = json.load(f)
            
            # Encontra o boleto e atualiza as informações da foto
            for boleto in boletos:
                if boleto['id'] == boleto_id:
                    boleto['tem_foto'] = True
                    boleto['caminho_foto'] = caminho_foto
                    boleto['nome_arquivo'] = nome_arquivo
                    break
            
            # Salva as alterações
            with open(self.boletos_file, 'w', encoding='utf-8') as f:
                json.dump(boletos, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Foto atualizada para boleto ID: {boleto_id}")
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar foto do boleto: {e}")
            return False
    
    def obter_boletos(self, usuario=None):
        """Obtém boletos do banco de dados"""
        try:
            with open(self.boletos_file, 'r', encoding='utf-8') as f:
                boletos = json.load(f)
            
            # Atualiza status baseado na data atual
            for boleto in boletos:
                self._atualizar_status_boleto(boleto)
            
            # Filtra por usuário se for funcionário
            if usuario and usuario['tipo'] == 'funcionario':
                boletos = [b for b in boletos if b.get('cadastrado_por') == usuario['username']]
            
            return boletos
            
        except Exception as e:
            print(f"❌ Erro ao carregar boletos: {e}")
            return []
    
    def obter_boleto_por_id(self, boleto_id):
        """Obtém um boleto específico pelo ID"""
        try:
            boleto_id = int(boleto_id)  # 🔥 CORREÇÃO: Converter para inteiro
            boletos = self.obter_boletos()
            for boleto in boletos:
                if boleto['id'] == boleto_id:
                    return boleto
            return None
        except ValueError:
            print(f"❌ ID inválido: {boleto_id}")
            return None
    
    def marcar_como_pago(self, boleto_id):
        """Marca um boleto como pago"""
        try:
            boleto_id = int(boleto_id)  # 🔥 CORREÇÃO: Converter para inteiro
            
            with open(self.boletos_file, 'r', encoding='utf-8') as f:
                boletos = json.load(f)
            
            for boleto in boletos:
                if boleto['id'] == boleto_id:
                    boleto['status'] = 'pago'
                    boleto['data_pagamento'] = self._data_atual()
                    break
            
            with open(self.boletos_file, 'w', encoding='utf-8') as f:
                json.dump(boletos, f, indent=4, ensure_ascii=False)
            
            return True, "✅ Boleto marcado como pago!"
            
        except Exception as e:
            return False, f"❌ Erro ao marcar como pago: {str(e)}"
    
    def excluir_boleto(self, boleto_id):
        """Exclui um boleto do sistema DEFINITIVAMENTE"""
        try:
            # 🔥 CORREÇÃO: Converter para inteiro
            boleto_id = int(boleto_id)
            
            with open(self.boletos_file, 'r', encoding='utf-8') as f:
                boletos = json.load(f)
            
            # Encontra o boleto para mostrar informações antes de excluir
            boleto_encontrado = None
            for b in boletos:
                if b['id'] == boleto_id:
                    boleto_encontrado = b
                    break
            
            if not boleto_encontrado:
                return False, "❌ Boleto não encontrado!"
            
            # Remove a foto do boleto se existir
            if boleto_encontrado.get('caminho_foto') and os.path.exists(boleto_encontrado['caminho_foto']):
                try:
                    os.remove(boleto_encontrado['caminho_foto'])
                    print(f"✅ Foto do boleto {boleto_id} removida")
                except Exception as e:
                    print(f"⚠️ Não foi possível remover a foto: {e}")
            
            # Filtra removendo o boleto com o ID especificado
            boletos = [b for b in boletos if b['id'] != boleto_id]
            
            with open(self.boletos_file, 'w', encoding='utf-8') as f:
                json.dump(boletos, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Boleto ID {boleto_id} excluído: {boleto_encontrado['pagador']}")
            return True, f"✅ Boleto **{boleto_encontrado['pagador']}** excluído definitivamente!"
            
        except ValueError:
            return False, f"❌ ID inválido: {boleto_id}"
        except Exception as e:
            print(f"❌ Erro ao excluir boleto {boleto_id}: {e}")
            return False, f"❌ Erro ao excluir boleto: {str(e)}"
    
    def _atualizar_status_boleto(self, boleto):
        """Atualiza o status do boleto baseado na data de vencimento"""
        if boleto['status'] == 'pago':
            return  # Não altera se já está pago
        
        try:
            data_vencimento = datetime.strptime(boleto['vencimento'], "%Y-%m-%d")
            hoje = datetime.now()
            
            if data_vencimento < hoje:
                boleto['status'] = 'atrasado'
            else:
                boleto['status'] = 'pendente'
                
        except Exception as e:
            print(f"❌ Erro ao atualizar status: {e}")
    
    # ===== FUNÇÕES DE ESTATÍSTICAS =====
    
    def obter_estatisticas(self):
        """Obtém estatísticas dos boletos"""
        boletos = self.obter_boletos()
        
        total_pendente = sum(b['valor'] for b in boletos if b['status'] in ['pendente', 'atrasado'])
        total_pago = sum(b['valor'] for b in boletos if b['status'] == 'pago')
        qtd_pendentes = len([b for b in boletos if b['status'] == 'pendente'])
        qtd_atrasados = len([b for b in boletos if b['status'] == 'atrasado'])
        qtd_pagos = len([b for b in boletos if b['status'] == 'pago'])
        total_boletos = len(boletos)
        
        return {
            'total_pendente': total_pendente,
            'total_pago': total_pago,
            'qtd_pendentes': qtd_pendentes,
            'qtd_atrasados': qtd_atrasados,
            'qtd_pagos': qtd_pagos,
            'total_boletos': total_boletos
        }
    
    def obter_alertas(self):
        """Gera alertas de boletos próximos do vencimento"""
        boletos = self.obter_boletos()
        alertas = []
        hoje = datetime.now()
        
        for boleto in boletos:
            if boleto['status'] == 'atrasado':
                alertas.append(f"🚨 {boleto['pagador']} - R$ {boleto['valor']:.2f} - ATRASADO!")
            elif boleto['status'] == 'pendente':
                try:
                    vencimento = datetime.strptime(boleto['vencimento'], "%Y-%m-%d")
                    dias_para_vencer = (vencimento - hoje).days
                    if dias_para_vencer <= 3:
                        alertas.append(f"⚠️ {boleto['pagador']} - Vence em {dias_para_vencer} dias - R$ {boleto['valor']:.2f}")
                except:
                    continue
        
        return alertas
    
    def obter_boletos_por_categoria(self):
        """Agrupa boletos por categoria"""
        boletos = self.obter_boletos()
        categorias = {}
        
        for boleto in boletos:
            categoria = boleto['categoria']
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append(boleto)
        
        return categorias
    
    # ===== FUNÇÕES DE USUÁRIOS =====
    
    def obter_usuarios(self):
        """Obtém todos os usuários do sistema"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def salvar_usuario(self, username, user_data):
        """Salva um novo usuário no sistema"""
        try:
            users = self.obter_usuarios()
            
            if username in users:
                return False, "❌ Usuário já existe!"
            
            users[username] = user_data
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
            
            return True, "✅ Usuário criado com sucesso!"
            
        except Exception as e:
            return False, f"❌ Erro ao criar usuário: {str(e)}"
    
    def verificar_login(self, username, password):
        """Verifica se o login é válido"""
        users = self.obter_usuarios()
        
        if username in users and users[username]['senha'] == password:
            return {
                'username': username,
                'nome': users[username]['nome'],
                'tipo': users[username]['tipo']
            }
        return None
    
    def excluir_usuario(self, username):
        """Exclui um usuário do sistema"""
        try:
            users = self.obter_usuarios()
            
            if username not in users:
                return False, "❌ Usuário não encontrado!"
            
            if username == 'admin':
                return False, "❌ Não é possível excluir o usuário admin!"
            
            del users[username]
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
            
            return True, "✅ Usuário excluído com sucesso!"
            
        except Exception as e:
            return False, f"❌ Erro ao excluir usuário: {str(e)}"
    
    # ===== FUNÇÕES UTILITÁRIAS =====
    
    def _data_atual(self):
        """Retorna a data atual formatada"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def limpar_dados(self):
        """⚠️ LIMPA TODOS OS DADOS (apenas para desenvolvimento)"""
        try:
            with open(self.boletos_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)
            return True, "✅ Dados limpos com sucesso!"
        except Exception as e:
            return False, f"❌ Erro ao limpar dados: {str(e)}"
    
    def exportar_dados(self):
        """Exporta todos os dados para backup"""
        try:
            boletos = self.obter_boletos()
            users = self.obter_usuarios()
            
            return {
                'boletos': boletos,
                'usuarios': users,
                'data_exportacao': self._data_atual()
            }
        except Exception as e:
            return None