# modules/security.py
import hashlib
import secrets
import json
import os
from datetime import datetime

class Security:
    def __init__(self):
        self.log_file = "logs/security.log"
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Garante que a pasta de logs existe"""
        os.makedirs("logs", exist_ok=True)
    
    def hash_password(self, password):
        """
        Criptografa senhas usando SHA-256 com salt
        """
        # Gera um salt único para cada senha
        salt = secrets.token_hex(16)
        # Combina senha + salt e faz hash
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        
        # Retorna o hash e o salt (armazenamos ambos)
        return f"{salt}${password_hash}"
    
    def verify_password(self, password, hashed_password):
        """
        Verifica se a senha corresponde ao hash
        """
        try:
            # Separa o salt do hash
            salt, stored_hash = hashed_password.split('$')
            # Calcula o hash da senha fornecida com o mesmo salt
            computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            # Compara os hashes
            return computed_hash == stored_hash
        except:
            return False
    
    def log_security_event(self, event, user, details=""):
        """
        Registra eventos de segurança no log
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {event} | Usuário: {user} | Detalhes: {details}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Erro ao escrever no log: {e}")
    
    def generate_secure_password(self, length=12):
        """
        Gera uma senha segura para novos usuários
        """
        import string
        import random
        
        # Caracteres permitidos
        characters = string.ascii_letters + string.digits + "!@#$%&*"
        
        # Garante pelo menos um de cada tipo
        password = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase), 
            random.choice(string.digits),
            random.choice("!@#$%&*")
        ]
        
        # Completa o resto aleatoriamente
        password += [random.choice(characters) for _ in range(length - 4)]
        
        # Embaralha a senha
        random.shuffle(password)
        
        return ''.join(password)
    
    def get_security_report(self):
        """
        Gera um relatório de segurança
        """
        try:
            if not os.path.exists(self.log_file):
                return "Nenhum evento de segurança registrado."
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()
            
            # Últimos 50 eventos
            recent_logs = logs[-50:] if len(logs) > 50 else logs
            
            report = f"📊 RELATÓRIO DE SEGURANÇA\n"
            report += f"📅 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            report += f"📋 Total de eventos: {len(logs)}\n"
            report += f"🔍 Últimos eventos:\n"
            report += "─" * 50 + "\n"
            
            for log in recent_logs[-10:]:  # Últimos 10 eventos
                report += log
            
            return report
            
        except Exception as e:
            return f"Erro ao gerar relatório: {e}"