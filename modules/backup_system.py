# modules/backup_system.py
import json
import os
import shutil
from datetime import datetime
import logging

class BackupSystem:
    def __init__(self):
        self.backup_dir = "data/backups"
        self.logs_dir = "logs"
        self._criar_diretorios_se_nao_existir()
        self._configurar_logs()
    
    def _criar_diretorios_se_nao_existir(self):
        """Cria os diretórios necessários se não existirem"""
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def _configurar_logs(self):
        """Configura o sistema de logs"""
        logging.basicConfig(
            filename=os.path.join(self.logs_dir, 'sistema.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
    
    def criar_backup(self):
        """Cria backup dos arquivos de dados"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Arquivos para backup
            arquivos = ["data/boletos.json", "data/users.json"]
            backups_criados = []
            
            for arquivo in arquivos:
                if os.path.exists(arquivo):
                    # Nome do arquivo de backup
                    nome_arquivo = os.path.basename(arquivo)
                    nome_backup = f"{nome_arquivo.replace('.json', '')}_backup_{timestamp}.json"
                    caminho_backup = os.path.join(self.backup_dir, nome_backup)
                    
                    # Copia o arquivo
                    shutil.copy2(arquivo, caminho_backup)
                    backups_criados.append(nome_backup)
                    
                    logging.info(f"Backup criado: {nome_backup}")
            
            if backups_criados:
                return f"Backups criados: {', '.join(backups_criados)}"
            else:
                return "Nenhum arquivo para backup"
                
        except Exception as e:
            error_msg = f"Erro ao criar backup: {e}"
            logging.error(error_msg)
            return error_msg
    
    def obter_info_backups(self):
        """Obtém informações sobre os backups existentes"""
        try:
            if not os.path.exists(self.backup_dir):
                return {"total_backups": 0, "ultimo_backup": "Nenhum"}
            
            # Lista todos os arquivos de backup
            arquivos_backup = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
            
            if not arquivos_backup:
                return {"total_backups": 0, "ultimo_backup": "Nenhum"}
            
            # Ordena por data (do mais recente para o mais antigo)
            arquivos_backup.sort(reverse=True)
            
            # Pega o backup mais recente
            ultimo_backup = arquivos_backup[0]
            
            # Tenta extrair a data do nome do arquivo
            try:
                # Formato: boletos_backup_20241205_143045.json
                partes = ultimo_backup.split('_')
                if len(partes) >= 3:
                    data_backup = partes[2]  # 20241205
                    hora_backup = partes[3].replace('.json', '')  # 143045
                    data_formatada = f"{data_backup[6:8]}/{data_backup[4:6]}/{data_backup[:4]} {hora_backup[:2]}:{hora_backup[2:4]}"
                else:
                    data_formatada = ultimo_backup
            except:
                data_formatada = ultimo_backup
            
            return {
                "total_backups": len(arquivos_backup),
                "ultimo_backup": data_formatada,
                "backups_recentes": arquivos_backup[:5]  # Últimos 5 backups
            }
            
        except Exception as e:
            logging.error(f"Erro ao obter info backups: {e}")
            return {"total_backups": 0, "ultimo_backup": f"Erro: {e}"}
    
    def restaurar_backup(self, nome_arquivo_backup):
        """Restaura um backup específico"""
        try:
            caminho_backup = os.path.join(self.backup_dir, nome_arquivo_backup)
            
            if not os.path.exists(caminho_backup):
                return "Arquivo de backup não encontrado"
            
            # Determina qual arquivo restaurar baseado no nome do backup
            if "boletos" in nome_arquivo_backup:
                arquivo_destino = "data/boletos.json"
            elif "users" in nome_arquivo_backup:
                arquivo_destino = "data/users.json"
            else:
                return "Tipo de backup não reconhecido"
            
            # Cria backup antes de restaurar (segurança)
            self.criar_backup()
            
            # Restaura o backup
            shutil.copy2(caminho_backup, arquivo_destino)
            
            logging.info(f"Backup restaurado: {nome_arquivo_backup} -> {arquivo_destino}")
            return f"Backup {nome_arquivo_backup} restaurado com sucesso"
            
        except Exception as e:
            error_msg = f"Erro ao restaurar backup: {e}"
            logging.error(error_msg)
            return error_msg
    
    def listar_backups(self):
        """Lista todos os backups disponíveis"""
        try:
            if not os.path.exists(self.backup_dir):
                return []
            
            arquivos_backup = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
            arquivos_backup.sort(reverse=True)  # Mais recentes primeiro
            
            backups_info = []
            for arquivo in arquivos_backup:
                caminho_completo = os.path.join(self.backup_dir, arquivo)
                tamanho = os.path.getsize(caminho_completo)
                data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_completo))
                
                backups_info.append({
                    'nome': arquivo,
                    'tamanho': tamanho,
                    'data_criacao': data_modificacao.strftime("%d/%m/%Y %H:%M"),
                    'tipo': 'boletos' if 'boletos' in arquivo else 'usuarios'
                })
            
            return backups_info
            
        except Exception as e:
            logging.error(f"Erro ao listar backups: {e}")
            return []
    
    def limpar_backups_antigos(self, dias_manter=30):
        """Remove backups mais antigos que X dias"""
        try:
            if not os.path.exists(self.backup_dir):
                return 0, "Nenhum backup para limpar"
            
            arquivos_backup = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
            data_limite = datetime.now().timestamp() - (dias_manter * 24 * 60 * 60)
            
            backups_removidos = 0
            
            for arquivo in arquivos_backup:
                caminho_completo = os.path.join(self.backup_dir, arquivo)
                data_modificacao = os.path.getmtime(caminho_completo)
                
                if data_modificacao < data_limite:
                    os.remove(caminho_completo)
                    backups_removidos += 1
                    logging.info(f"Backup antigo removido: {arquivo}")
            
            return backups_removidos, f"{backups_removidos} backups antigos removidos"
            
        except Exception as e:
            error_msg = f"Erro ao limpar backups antigos: {e}"
            logging.error(error_msg)
            return 0, error_msg
    
    def excluir_backup(self, nome_backup):
        """Exclui um backup específico"""
        try:
            caminho_backup = os.path.join(self.backup_dir, nome_backup)
            
            if not os.path.exists(caminho_backup):
                return False
            
            os.remove(caminho_backup)
            logging.info(f"Backup excluído: {nome_backup}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao excluir backup: {e}")
            return False
    
    def get_estatisticas_backup(self):
        """Retorna estatísticas detalhadas do sistema de backup"""
        info = self.obter_info_backups()
        backups_lista = self.listar_backups()
        
        estatisticas = {
            "total_backups": info["total_backups"],
            "ultimo_backup": info["ultimo_backup"],
            "backups_boletos": len([b for b in backups_lista if b['tipo'] == 'boletos']),
            "backups_usuarios": len([b for b in backups_lista if b['tipo'] == 'usuarios']),
            "tamanho_total": sum(b['tamanho'] for b in backups_lista),
            "backups_recentes": backups_lista[:3]  # 3 mais recentes
        }
        
        return estatisticas