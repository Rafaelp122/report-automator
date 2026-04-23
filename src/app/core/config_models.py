from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Optional
from datetime import datetime

class ProjectConfig(BaseModel):
    nome: str = "RDO Automator"
    mes: int = Field(default_factory=lambda: datetime.now().month)
    ano: int = Field(default_factory=lambda: datetime.now().year)

class FilesConfig(BaseModel):
    linha_cabecalho: int = 0
    dados_origem: str = ""
    user_template: str = ""
    template_ativo: str = ""  # Template que será usado de fato

class ContractConfig(BaseModel):
    data_inicio: str = "2026-01-01"
    prazo_dias: int = 365

class ExtractionConfig(BaseModel):
    colunas: List[str] = []
    separador_lista: str = ", "
    conector_final: str = " e "
    formato_final: str = ""

class PositionsConfig(BaseModel):
    celula_data_inicio: str = ""
    celula_prazo_dias: str = ""
    celula_data_final: str = ""
    celula_data_atual: str = ""
    celula_tempo_decorrido: str = ""

class ReportConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    projeto: ProjectConfig = Field(default_factory=ProjectConfig)
    arquivos: FilesConfig = Field(default_factory=FilesConfig)
    contrato: ContractConfig = Field(default_factory=ContractConfig)
    extracao: ExtractionConfig = Field(default_factory=ExtractionConfig, alias="extração")
    posicoes: PositionsConfig = Field(default_factory=PositionsConfig)
    mapeamento: Dict[str, str] = Field(default_factory=dict)
