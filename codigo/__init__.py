from .modelos import Servidor
from .modelos import DadosTempo
from .modelos import ResultadoRegra
from .repositorio import RepositorioServidores
from .regras import RegraAposentadoria
from .regras import RegraDireitoAdquirido
from .regras import RegraGeral
from .simulador import SimuladorAposentadoria
from .gerador_pdf import PDFGenerator
from .converter_json import converter_excel_para_json


#python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True); shutil.rmtree('codigo/__pycache__', ignore_errors=True)"