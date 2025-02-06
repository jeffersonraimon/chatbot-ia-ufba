import pytest
from sqlalchemy import (
    create_engine,
    inspect,
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base  # Novo (SQLAlchemy 2.0+)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import os

Base = declarative_base()


# Definição das tabelas (sem mudanças)
class Localizacao(Base):
    __tablename__ = "localizacao"
    id_localizacao = Column(Integer, primary_key=True, autoincrement=True)
    endereco = Column(String(200))
    cidade = Column(String(100))
    estado = Column(String(50))
    cep = Column(String(10))
    telefone = Column(String(20))
    email = Column(String(100))
    site = Column(String(100))


class Instituto(Base):
    __tablename__ = "instituto"
    id_instituto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    historia = Column(Text)
    fundacao = Column(Date)
    missao = Column(Text)
    visao = Column(Text)
    valores = Column(Text)


class ProgramaAcademico(Base):
    __tablename__ = "programaacademico"
    id_programa = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    duracao = Column(Integer)
    coordenador = Column(String(100))


class Disciplina(Base):
    __tablename__ = "disciplina"
    id_disciplina = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    carga_horaria = Column(Integer)
    professor = Column(String(100))
    programa_academico = Column(Integer, ForeignKey("programaacademico.id_programa"))


class Ementa(Base):
    __tablename__ = "ementa"
    id_ementa = Column(Integer, primary_key=True, autoincrement=True)
    id_disciplina = Column(Integer, ForeignKey("disciplina.id_disciplina"))
    conteudo = Column(Text)
    bibliografia = Column(Text)
    metodologia = Column(Text)
    avaliacao = Column(Text)


class Evento(Base):
    __tablename__ = "evento"
    id_evento = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    data = Column(Date)
    local = Column(String(100))
    organizador = Column(String(100))
    link_inscricao = Column(String(200))


# Configuração do banco MySQL para testes
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "test_chatbot"
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


@pytest.fixture(scope="module")
def engine():
    """Cria e retorna uma conexão com o banco de testes MySQL."""
    engine = create_engine(DB_URL)
    yield engine
    engine.dispose()


@pytest.fixture(scope="module")
def session(engine):
    """Cria e retorna uma sessão do banco de dados."""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="module")
def setup_db(engine):
    """Cria todas as tabelas antes dos testes e remove após."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_tabelas_criadas(engine, setup_db):
    """Verifica se todas as tabelas foram criadas corretamente."""
    inspector = inspect(engine)
    tabelas = inspector.get_table_names()
    assert set(tabelas) == {
        "instituto",
        "programaacademico",
        "disciplina",
        "ementa",
        "evento",
        "localizacao",
    }


def test_inserir_instituto(session, setup_db):
    """Testa a inserção de um Instituto."""
    instituto = Instituto(nome="Instituto de Computação")
    session.add(instituto)
    session.commit()
    assert (
        session.query(Instituto).filter_by(nome="Instituto de Computação").first()
        is not None
    )


def test_inserir_programa_academico(session, setup_db):
    """Testa a inserção de um Programa Acadêmico."""
    programa = ProgramaAcademico(
        nome="Ciência da Computação",
        descricao="Bacharelado em Ciência da Computação",
        duracao=4,
    )
    session.add(programa)
    session.commit()
    assert (
        session.query(ProgramaAcademico).filter_by(nome="Ciência da Computação").first()
        is not None
    )


def test_inserir_disciplina(session, setup_db):
    """Testa a inserção de uma Disciplina vinculada a um Programa Acadêmico."""
    programa = (
        session.query(ProgramaAcademico).filter_by(nome="Ciência da Computação").first()
    )
    disciplina = Disciplina(
        nome="Inteligência Artificial", programa_academico=programa.id_programa
    )
    session.add(disciplina)
    session.commit()
    assert (
        session.query(Disciplina).filter_by(nome="Inteligência Artificial").first()
        is not None
    )





def test_inserir_evento(session, setup_db):
    """Testa a inserção de um Evento."""
    evento = Evento(
        nome="Semana da Computação",
        descricao="Evento anual sobre tecnologia e inovação.",
    )
    session.add(evento)
    session.commit()
    assert (
        session.query(Evento).filter_by(nome="Semana da Computação").first() is not None
    )


def test_constraint_nome_instituto(session, setup_db):
    """Testa a restrição de nulidade no campo nome do Instituto."""
    instituto_invalido = Instituto(nome=None)
    session.add(instituto_invalido)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
