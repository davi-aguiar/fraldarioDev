-- Criar o banco de dados fraldario se não existir
CREATE DATABASE IF NOT EXISTS fraldario;

-- Usar o banco de dados fraldario
USE fraldario;

-- Criar tabela Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
    
);

-- Criar tabela Autorizador
CREATE TABLE IF NOT EXISTS Autorizador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    historico_cadastro TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
);

-- Criar tabela Farmacia
CREATE TABLE IF NOT EXISTS Farmacia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
);
CREATE TABLE IF NOT EXISTS Prefeitura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
);
ALTER TABLE prefeitura
ADD COLUMN usuario_id INT,
ADD CONSTRAINT fk_usuario
FOREIGN KEY (usuario_id) REFERENCES usuario(id);
CREATE TABLE Beneficiado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_beneficiado VARCHAR(255) NOT NULL,
    cpf_beneficiado VARCHAR(14) NOT NULL,
    cpfPesquisado VARCHAR(14) NOT NULL,
    cartao_sus VARCHAR(20) NOT NULL,
    nome_autorizado VARCHAR(255) NOT NULL,
    cpf_autorizado VARCHAR(14) NOT NULL,
    quantidade_liberada INT NOT NULL,
    quantidade_pego INT NOT NULL,
    quantidade_restante INT NOT NULL,
    tamanho_liberado VARCHAR(50) NOT NULL,
    motivo_liberacao VARCHAR(255) NOT NULL,
    data_inicio DATE NOT NULL,
    validade_meses INT NOT NULL,
    documento VARCHAR(255) NOT NULL,
    licitacao VARCHAR(255) NOT NULL
);
-- Adicionar o campo "nomeAutorizador" à tabela "autorizador"
ALTER TABLE autorizador
ADD COLUMN nomeAutorizador VARCHAR(255); -- Defina o tipo de dados e o comprimento conforme necessário

-- Adicionar o campo "nomeFantasia" à tabela "farmacia"
ALTER TABLE farmacia
ADD COLUMN nomeFantasia VARCHAR(255); -- Defina o tipo de dados e o comprimento conforme necessário
ALTER TABLE farmacia
ADD COLUMN documentoBeneficiado VARCHAR(255) NULL,
ADD COLUMN fotoDocumento VARCHAR(255) NULL;
ALTER TABLE Beneficiado
ADD COLUMN pendente BOOLEAN DEFAULT FALSE,
ADD COLUMN usuarioPendente VARCHAR(14) NOT NULL;
ALTER TABLE Beneficiado
ADD quantidadeTotal INT NOT NULL DEFAULT 0;
ALTER TABLE Farmacia
ADD quantidadeTotal INT NOT NULL DEFAULT 0;

ALTER TABLE beneficiado
MODIFY documento LONGBLOB NOT NULL,
MODIFY licitacao LONGBLOB NOT NULL;
-- Adicionar cnpj_pesquisado na tabela Farmacia
ALTER TABLE Farmacia
ADD COLUMN cnpj_pesquisado VARCHAR(14);

-- Adicionar cpf_pesquisado na tabela Autorizador
ALTER TABLE Autorizador
ADD COLUMN cpf_pesquisado VARCHAR(11);


ALTER TABLE Usuario
ADD COLUMN email_confirmed BOOLEAN DEFAULT FALSE;

CREATE TABLE IF NOT EXISTS UsuarioTemp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

ALTER TABLE UsuarioTemp
ADD COLUMN tipo_login VARCHAR(255);

ALTER TABLE Usuario
ADD COLUMN tipo_usuario VARCHAR(255);



ALTER TABLE UsuarioTemp
ADD COLUMN cpf VARCHAR(11);
ALTER TABLE UsuarioTemp
ADD COLUMN cnpj VARCHAR(14); 

ALTER TABLE UsuarioTemp
ADD COLUMN nome VARCHAR(255);

ALTER TABLE beneficiado
ADD COLUMN usuarioPendente VARCHAR(255);

ALTER TABLE prefeitura
ADD COLUMN cpf_prefeitura VARCHAR(11);

ALTER TABLE prefeitura
ADD COLUMN nomePrefeitura VARCHAR(255);

ALTER TABLE beneficiado
ADD COLUMN usuario_pendente VARCHAR(255);
ALTER TABLE beneficiado
ADD COLUMN marca_fralda VARCHAR(255);

-- Alterar o tipo da coluna documento para BLOB
ALTER TABLE beneficiado
MODIFY COLUMN documento BLOB NOT NULL;

-- Alterar o tipo da coluna licitacao para BLOB
ALTER TABLE beneficiado
MODIFY COLUMN licitacao BLOB NOT NULL;

ALTER TABLE Beneficiado
ADD COLUMN id_autorizador INTEGER;

ALTER TABLE Farmacia
ADD COLUMN data_retirada DATETIME DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE transacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmacia_id INT NOT NULL,
    quantidade INT NOT NULL,
    data_retirada DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmacia_id) REFERENCES farmacia(id)
);
ALTER TABLE farmacia ADD COLUMN data_criacao DATE DEFAULT '2024-01-01';

ALTER TABLE transacao ADD COLUMN media_tamanho_fralda VARCHAR(10) NOT NULL DEFAULT '';
ALTER TABLE transacao ADD COLUMN media_marca_fralda VARCHAR(10) NOT NULL DEFAULt '';

ALTER TABLE transacao ADD marca_fralda_entregue VARCHAR(20) NOT NULL;
ALTER TABLE transacao MODIFY marca_fralda_entregue VARCHAR(20) NOT NULL;
ALTER TABLE transacao ADD tamanho_fralda VARCHAR(20) NOT NULL;
CREATE TABLE transacaoA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    autorizador_id INT NOT NULL,
    quantidadeBeneficiado INT NOT NULL,
    data_retirada DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (autorizador_id) REFERENCES autorizador(id)
);
ALTER TABLE TransacaoA
ADD COLUMN total_por_mes FLOAT,
ADD COLUMN detalhes_beneficiados VARCHAR(255),
ADD COLUMN media FLOAT;
ALTER TABLE TransacaoA
ADD COLUMN cpf_beneficiadoA VARCHAR(40);


ALTER TABLE Usuario
ADD COLUMN first_login BOOLEAN DEFAULT TRUE;

ALTER TABLE Farmacia
ADD COLUMN localizacao VARCHAR(255) NOT NULL,
ADD COLUMN tipos_fralda VARCHAR(20) NOT NULL;

ALTER TABLE UsuarioTemp
ADD COLUMN localizacao VARCHAR(255) ,
ADD COLUMN tipos_fralda VARCHAR(20) ,
ADD COLUMN tamanho_fralda VARCHAR(20) ;


ALTER TABLE Beneficiado
ADD COLUMN id_prefeitura INTEGER;


ALTER TABLE Farmacia
ADD COLUMN documento_liberacao VARCHAR(255) DEFAULT '';

ALTER TABLE Autorizador
ADD COLUMN documento_liberacao VARCHAR(255) DEFAULT '';

ALTER TABLE Prefeitura
ADD COLUMN documento_liberacao VARCHAR(255) DEFAULT '';

ALTER TABLE UsuarioTemp
ADD COLUMN documento_liberacao VARCHAR(255) DEFAULT '' ;


ALTER TABLE farmacia
ADD COLUMN cep VARCHAR(9) NOT NULL,
ADD COLUMN logradouro VARCHAR(255) NOT NULL,
ADD COLUMN numero VARCHAR(10) NOT NULL,
ADD COLUMN complemento VARCHAR(255),
ADD COLUMN bairro VARCHAR(255),
ADD COLUMN cidade VARCHAR(255) NOT NULL,
ADD COLUMN estado VARCHAR(2) NOT NULL,
ADD COLUMN tamanho_fralda VARCHAR(20) ;

ALTER TABLE farmacia
DROP COLUMN localizacao;

ALTER TABLE usertemp
DROP COLUMN localizacao;

ALTER TABLE usuariotemp
ADD COLUMN cep VARCHAR(9) DEFAULT '',
ADD COLUMN logradouro VARCHAR(255) DEFAULT '',
ADD COLUMN numero VARCHAR(10) DEFAULT '',
ADD COLUMN complemento VARCHAR(255),
ADD COLUMN bairro VARCHAR(255),
ADD COLUMN cidade VARCHAR(255) DEFAULT '',
ADD COLUMN estado VARCHAR(2) DEFAULT '';

ALTER TABLE Usuario

ADD COLUMN ativo BOOLEAN DEFAULT FALSE;
ALTER TABLE transacao
ADD quantidadeTotal INT NOT NULL DEFAULT 0;
ALTER TABLE UsuarioTemp
MODIFY COLUMN documento_liberacao BLOB;
ALTER TABLE FARMACIA
MODIFY COLUMN documento_liberacao BLOB;
ALTER TABLE Autorizador
MODIFY COLUMN documento_liberacao BLOB;

ALTER TABLE farmacia CHANGE COLUMN quantidadeTotal quantidade INT;

ALTER TABLE beneficiado
ADD COLUMN data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE farmacia
ADD COLUMN data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE beneficiado
ADD COLUMN data_final DATETIME DEFAULT current_timestamp;
ALTER TABLE Beneficiado
ADD COLUMN confirmacao BOOLEAN DEFAULT FALSE;
ALTER TABLE dadosTemporarios
ADD COLUMN beneficiado_id INT,
ADD FOREIGN KEY (beneficiado_id) REFERENCES Beneficiado(id);

CREATE TABLE dadosTemporarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quantidade_liberada INT,
    tamanho_liberado VARCHAR(50),
    motivo_liberacao VARCHAR(200),
    data_inicio DATE,
    validade_meses INT
);
ALTER TABLE dadosTemporarios
ADD COLUMN beneficiado_id INT,
ADD FOREIGN KEY (beneficiado_id) REFERENCES Beneficiado(id);

ALTER TABLE Usuario
add column is_admin BOOLEAN DEFAULT FALSE;
ALTER TABLE Beneficiado
ADD COLUMN ativo BOOLEAN DEFAULT FALSE;

ALTER TABLE farmacia ADD COLUMN razaoSocial VARCHAR(255) AFTER nomeFantasia;
ALTER TABLE usuariotemp ADD COLUMN razaoSocial VARCHAR(255) AFTER nome;
ALTER TABLE transacao
RENAME COLUMN media_marca_fralda TO quantidade_total;
ALTER TABLE transacao
CHANGE COLUMN quantidade_total quantidade_total INT;
ALTER TABLE transacao
ADD COLUMN nome_beneficiado VARCHAR(100),  -- Assumindo que o nome seja uma string com até 100 caracteres
ADD COLUMN cpf_beneficiado VARCHAR(20);    -- Assumindo que CPF seja uma string com até 20 caracteres



CREATE TABLE PaginaInicial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    capa VARCHAR(100),
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    beneficiarios_adultos TEXT NOT NULL,
    beneficiarios_criancas TEXT NOT NULL,
    objetivo1 TEXT NOT NULL,
    objetivo2 TEXT NOT NULL,
    objetivo3 TEXT NOT NULL
);
use fraldario;
alter table usuario
add column is_root boolean default false


CREATE TABLE funcao (
    id INTEGER PRIMARY KEY,
    descricao TEXT
);

-- Tabela de Associação entre Usuários e Funções
CREATE TABLE usuario_funcao (
    usuario_id INTEGER,
    funcao_id INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuario (id),
    FOREIGN KEY (funcao_id) REFERENCES funcao (id)
);
ALTER TABLE usuario
ADD COLUMN funcoes VARCHAR(255); -- Adjust the data type and size as per your requirements
CREATE TABLE documento (
    id INT PRIMARY KEY AUTO_INCREMENT,
    beneficiado_id INT,
    licitacao BLOB,
    documento_licitacao BLOB,
    FOREIGN KEY (beneficiado_id) REFERENCES beneficiado(id)
);
ALTER TABLE documento MODIFY COLUMN licitacao LONGBLOB;
ALTER TABLE UsuarioTemp
ADD COLUMN funcoes VARCHAR(255)