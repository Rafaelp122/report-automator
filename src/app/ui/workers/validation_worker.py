import os
import pandas as pd
import tomllib
import time
from PySide6.QtCore import QObject, Signal, Slot
from src.app.core.logger import logger

class ValidationWorker(QObject):
    """
    Worker para validar a integridade dos dados e mapeamentos.
    """
    progress_log = Signal(str)
    validation_finished = Signal(bool, list)
    finished = Signal() # Sinal técnico para fechar a thread

    @Slot()
    def run(self):
        erros = []
        try:
            msg = "Iniciando validação de mapeamento..."
            logger.info(msg)
            self.progress_log.emit(msg)
            time.sleep(0.5) # Pequena pausa para o usuário perceber o início
            
            # 1. Carregar Configurações
            if not os.path.exists("config.toml"):
                erros.append("Arquivo config.toml não encontrado.")
                logger.error("Arquivo config.toml não encontrado.")
                self.validation_finished.emit(False, erros)
                return

            with open("config.toml", "rb") as f:
                config = tomllib.load(f)

            # 2. Verificar Arquivo de Origem
            caminho_dados = config['arquivos'].get('dados_origem')
            if not caminho_dados or not os.path.exists(caminho_dados):
                err_msg = f"Arquivo de origem não encontrado: {caminho_dados}"
                erros.append(err_msg)
                logger.error(err_msg)
            else:
                msg = f"Analisando: {os.path.basename(caminho_dados)}"
                logger.info(msg)
                self.progress_log.emit(msg)
                
                # 3. Validar Abas e Colunas
                try:
                    with pd.ExcelFile(caminho_dados) as xls:
                        abas_no_arquivo = xls.sheet_names
                        
                        col_data = config['colunas'].get('data')
                        col_servico = config['colunas'].get('servico')
                        
                        msg = f"Verificando {len(config['mapeamento'])} abas mapeadas..."
                        logger.info(msg)
                        self.progress_log.emit(msg)

                        for nome_aba in config['mapeamento'].keys():
                            if nome_aba not in abas_no_arquivo:
                                err_msg = f"Aba '{nome_aba}' não encontrada."
                                erros.append(err_msg)
                                logger.warning(err_msg)
                                continue
                            
                            df_header = pd.read_excel(xls, sheet_name=nome_aba, nrows=0)
                            colunas = df_header.columns.tolist()
                            
                            if col_data not in colunas:
                                err_msg = f"Na aba '{nome_aba}', coluna '{col_data}' inexistente."
                                erros.append(err_msg)
                                logger.warning(err_msg)
                            if col_servico not in colunas:
                                err_msg = f"Na aba '{nome_aba}', coluna '{col_servico}' inexistente."
                                erros.append(err_msg)
                                logger.warning(err_msg)
                
                except Exception as e:
                    err_msg = f"Falha ao abrir Excel: {str(e)}"
                    erros.append(err_msg)
                    logger.error(err_msg)

            # 4. Resultado Final
            if erros:
                logger.warning(f"Validação concluída com {len(erros)} erros.")
                self.validation_finished.emit(False, erros)
            else:
                msg = "Tudo ok! Mapeamento validado."
                logger.info(msg)
                self.progress_log.emit(msg)
                self.validation_finished.emit(True, [])

        except Exception as e:
            err_msg = f"Erro fatal na validação: {str(e)}"
            logger.exception(err_msg)
            self.progress_log.emit(err_msg)
            self.validation_finished.emit(False, [str(e)])
        
        finally:
            self.finished.emit()
