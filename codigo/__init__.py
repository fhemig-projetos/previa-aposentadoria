from .modelos import Servidor
from .modelos import DadosTempo
from .modelos import ResultadoRegra
from .repositorio import RepositorioServidores

from .regra_modelo import RegraAposentadoria
from .regra_pedagio import RegraDireitoAdquirido
from .regra_compulsoria import RegraCompulsoria
from .regra_geral import RegraGeral
from .regra_pontos import RegraPontos

from .simulador import SimuladorAposentadoria
from .gerador_pdf import PDFGenerator


#python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True); shutil.rmtree('codigo/__pycache__', ignore_errors=True)"