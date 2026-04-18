from PySide6.QtCore import QThread

def run_worker_thread(worker, on_finished=None, on_error=None, on_log=None):
    """
    Abstração para execução de Workers em QThreads.
    
    Gerencia:
    1. Instanciação e movimentação do worker para a thread.
    2. Conexão de sinais padrão (started, finished, error, progress).
    3. Cleanup automático de memória (deleteLater).
    
    Retorna: O objeto QThread (deve ser mantido em escopo para evitar GC).
    """
    thread = QThread()
    worker.moveToThread(thread)
    
    # Inicia o worker quando a thread começar
    thread.started.connect(worker.run)
    
    # Conexões Dinâmicas (Signals para Callbacks)
    if on_log:
        worker.progress_log.connect(on_log)
    if on_finished:
        worker.finished.connect(on_finished)
    if on_error:
        worker.error.connect(on_error)
        
    # Standard Cleanup (Ordem de encerramento segura)
    worker.finished.connect(thread.quit)
    worker.error.connect(thread.quit)
    
    # IMPORTANTE: deleteLater garante que o objeto só seja destruído 
    # após todos os eventos pendentes na thread serem processados.
    worker.finished.connect(worker.deleteLater)
    worker.error.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    
    thread.start()
    return thread
