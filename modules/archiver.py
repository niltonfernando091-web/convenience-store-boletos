# modules/archiver.py
import json
import os
from datetime import datetime, timedelta

class BoletosArchiver:
    def __init__(self, database):
        self.db = database
        self.arquivados_file = "data/boletos_arquivados.json"
        self._criar_arquivo_arquivados()
    
    def _criar_arquivo_arquivados(self):
        """Cria o arquivo de boletos arquivados se não existir"""
        os.makedirs(os.path.dirname(self.arquivados_file), exist_ok=True)
        if not os.path.exists(self.arquivados_file):
            with open(self.arquivados_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)
    
    def arquivar_boletos_antigos(self, meses=1):
        """
        Arquiva boletos pagos com mais de X meses
        Retorna: (quantidade_arquivada, mensagem)
        """
        try:
            # Carrega boletos atuais
            with open(self.db.boletos_file, 'r', encoding='utf-8') as f:
                boletos_atuais = json.load(f)
            
            # Carrega boletos arquivados
            with open(self.arquivados_file, 'r', encoding='utf-8') as f:
                boletos_arquivados = json.load(f)
            
            # Data limite (boletos mais antigos que esta data serão arquivados)
            data_limite = datetime.now() - timedelta(days=meses*30)
            
            boletos_para_manter = []
            boletos_para_arquivar = []
            
            for boleto in boletos_atuais:
                try:
                    # Verifica se é pago e antigo
                    if boleto.get('status') == 'pago':
                        data_pagamento_str = boleto.get('data_pagamento')
                        if data_pagamento_str:
                            data_pagamento = datetime.strptime(data_pagamento_str, "%Y-%m-%d %H:%M:%S")
                            if data_pagamento < data_limite:
                                boletos_para_arquivar.append(boleto)
                                continue
                    
                    # Se não for para arquivar, mantém na lista atual
                    boletos_para_manter.append(boleto)
                    
                except Exception as e:
                    print(f"Erro ao processar boleto {boleto.get('id')}: {e}")
                    boletos_para_manter.append(boleto)  # Mantém em caso de erro
            
            # Se não há boletos para arquivar, retorna
            if not boletos_para_arquivar:
                return 0, "Nenhum boleto antigo para arquivar"
            
            # Adiciona os boletos arquivados à lista de arquivados
            boletos_arquivados.extend(boletos_para_arquivar)
            
            # Salva os boletos atualizados (sem os arquivados)
            with open(self.db.boletos_file, 'w', encoding='utf-8') as f:
                json.dump(boletos_para_manter, f, indent=4, ensure_ascii=False)
            
            # Salva os boletos arquivados
            with open(self.arquivados_file, 'w', encoding='utf-8') as f:
                json.dump(boletos_arquivados, f, indent=4, ensure_ascii=False)
            
            quantidade = len(boletos_para_arquivar)
            return quantidade, f"✅ {quantidade} boletos arquivados com sucesso!"
            
        except Exception as e:
            return 0, f"❌ Erro ao arquivar boletos: {str(e)}"
    
    def obter_boletos_arquivados(self):
        """Retorna todos os boletos arquivados"""
        try:
            with open(self.arquivados_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def restaurar_boleto(self, boleto_id):
        """Restaura um boleto arquivado para a lista principal"""
        try:
            # Carrega boletos arquivados
            with open(self.arquivados_file, 'r', encoding='utf-8') as f:
                boletos_arquivados = json.load(f)
            
            # Carrega boletos atuais
            with open(self.db.boletos_file, 'r', encoding='utf-8') as f:
                boletos_atuais = json.load(f)
            
            # Encontra e remove o boleto dos arquivados
            boleto_restaurado = None
            novos_arquivados = []
            
            for boleto in boletos_arquivados:
                if boleto.get('id') == boleto_id:
                    boleto_restaurado = boleto
                else:
                    novos_arquivados.append(boleto)
            
            if not boleto_restaurado:
                return False, "Boleto não encontrado nos arquivos"
            
            # Adiciona o boleto aos atuais
            boletos_atuais.append(boleto_restaurado)
            
            # Salva as listas atualizadas
            with open(self.arquivados_file, 'w', encoding='utf-8') as f:
                json.dump(novos_arquivados, f, indent=4, ensure_ascii=False)
            
            with open(self.db.boletos_file, 'w', encoding='utf-8') as f:
                json.dump(boletos_atuais, f, indent=4, ensure_ascii=False)
            
            return True, f"✅ Boleto #{boleto_id} restaurado com sucesso!"
            
        except Exception as e:
            return False, f"❌ Erro ao restaurar boleto: {str(e)}"
    
    def limpar_arquivados_antigos(self, anos=2):
        """Remove boletos arquivados mais antigos que X anos"""
        try:
            with open(self.arquivados_file, 'r', encoding='utf-8') as f:
                boletos_arquivados = json.load(f)
            
            data_limite = datetime.now() - timedelta(days=anos*365)
            boletos_para_manter = []
            boletos_removidos = 0
            
            for boleto in boletos_arquivados:
                try:
                    data_pagamento_str = boleto.get('data_pagamento')
                    if data_pagamento_str:
                        data_pagamento = datetime.strptime(data_pagamento_str, "%Y-%m-%d %H:%M:%S")
                        if data_pagamento >= data_limite:
                            boletos_para_manter.append(boleto)
                        else:
                            boletos_removidos += 1
                    else:
                        boletos_para_manter.append(boleto)  # Mantém se não tem data
                except:
                    boletos_para_manter.append(boleto)  # Mantém em caso de erro
            
            # Salva a lista filtrada
            with open(self.arquivados_file, 'w', encoding='utf-8') as f:
                json.dump(boletos_para_manter, f, indent=4, ensure_ascii=False)
            
            return boletos_removidos, f"🗑️ {boletos_removidos} boletos arquivados antigos removidos"
            
        except Exception as e:
            return 0, f"❌ Erro ao limpar arquivados: {str(e)}"
    
    def get_estatisticas_arquivamento(self):
        """Retorna estatísticas do sistema de arquivamento"""
        try:
            boletos_arquivados = self.obter_boletos_arquivados()
            with open(self.db.boletos_file, 'r', encoding='utf-8') as f:
                boletos_atuais = json.load(f)
            
            total_arquivados = len(boletos_arquivados)
            total_atuais = len(boletos_atuais)
            
            # Calcula espaço economizado (estimativa)
            tamanho_arquivados = len(json.dumps(boletos_arquivados))
            tamanho_atuais = len(json.dumps(boletos_atuais))
            
            return {
                'total_boletos_atuais': total_atuais,
                'total_boletos_arquivados': total_arquivados,
                'espaco_economizado_kb': (tamanho_arquivados / 1024),
                'percentual_arquivado': (total_arquivados / (total_atuais + total_arquivados)) * 100 if (total_atuais + total_arquivados) > 0 else 0
            }
        except Exception as e:
            return {
                'total_boletos_atuais': 0,
                'total_boletos_arquivados': 0,
                'espaco_economizado_kb': 0,
                'percentual_arquivado': 0
            }