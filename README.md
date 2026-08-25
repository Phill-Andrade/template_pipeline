# Template Pipeline

Template reutilizável para executar pipelines PySpark no cluster YARN da plataforma e permitir sua orquestração pelo Airflow.

> Status: arquitetura em definição. Ainda não existe uma implementação executável neste repositório.

## Índice

- [Arquitetura](#arquitetura)
- [Início rápido](#início-rápido)
- [Uso](#uso)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Contribuição](#contribuição)
- [Versionamento e releases](#versionamento-e-releases)
- [Responsabilidades](#responsabilidades)

## Arquitetura

Este repositório será o módulo de execução entre o Airflow e a plataforma de dados:

```text
Airflow
  → inicia o container do pipeline
  → pipeline executa spark-submit
  → YARN aloca driver e executores
  → Spark processa os dados
  → HDFS armazena as tabelas Hudi
  → Hive Metastore registra o catálogo
```

O pipeline usará:

- YARN como gerenciador do cluster;
- HDFS como armazenamento distribuído;
- Hudi como formato de tabela;
- Hive Metastore como catálogo;
- Spark History Server para consultar execuções finalizadas;
- uma imagem baseada no runtime fornecido pela plataforma.

## Início rápido

### Pré-requisitos

A implementação futura dependerá de:

- plataforma de dados em execução;
- rede Docker `data_platform_network`;
- imagem-base `hadoop_platform`;
- Airflow em um projeto independente.

### Instalação e execução

Ainda não existem comandos de instalação, execução ou testes. Eles serão documentados somente depois de implementados e validados.

## Uso

O caso de uso inicial será um job PySpark submetido ao YARN, gravando uma tabela Hudi no HDFS e sincronizando seus metadados com o Hive Metastore.

Entradas, saídas, recursos computacionais e parâmetros serão declarados em arquivos de configuração próprios do pipeline.

## Estrutura do projeto

Estrutura prevista para o final da primeira etapa:

```text
.
├── configs/
│   ├── jobs/
│   │   └── example.yaml
│   └── platform.yaml
├── .env.example
├── .gitignore
└── README.md
```

Os arquivos serão adicionados incrementalmente. Diretórios vazios não serão criados apenas para antecipar a estrutura.

## Contribuição

Cada parte da implementação deve:

1. partir da branch `dev`;
2. usar uma branch no padrão `feat/<change_name>`;
3. alterar somente o escopo acordado;
4. ser revisada antes do commit;
5. receber commit manual como aceite da parte concluída.

Os comandos de qualidade serão documentados quando as respectivas ferramentas forem adicionadas.

## Versionamento e releases

A estratégia de versionamento e o mecanismo de release ainda não foram definidos. Nenhuma release será publicada durante a fundação inicial do projeto.

## Responsabilidades

### Plataforma de dados

Responsável por Spark, YARN, HDFS, Hudi, Hive Metastore, PostgreSQL, configurações XML, imagem-base e rede Docker.

### Airflow

Responsável por agendamento, dependências, retries, timeout e parâmetros de execução.

### Pipeline

Responsável pela lógica de leitura, transformação, validação, escrita e pelo comando de submissão ao YARN. Este repositório não recriará os serviços pertencentes à plataforma ou ao Airflow.
