# Roteiro de fala — Apresentação da API PetClean

**Três blocos**, um por integrante: Helen Aclina, Gabriel Wagner e João Vitor Silva.
Este arquivo é gerado a partir das notas do apresentador embutidas no `.pptx`
(`gerador/deck.py`). Cada slide tem a fala sugerida.

| Bloco | Quem | Slides |
|---|---|---|
| Bloco 01 · Modelos e Entidades | Helen Aclina | slides 1 a 6 |
| Bloco 02 · Banco de Dados e Repositories | Gabriel Wagner | slides 7 a 10 |
| Bloco 03 · Swagger, CRUD e Endpoints Especializados | Joao Vitor Silva | slides 11 a 15 |

> As notas também estão no arquivo do PowerPoint: em **Exibir › Anotações do
> apresentador** (ou na tela do apresentador).

---

## Bloco 01 — Modelos e Entidades

**Helen Aclina** · slides 1 a 6

### Slide 01 — Capa

Boa noite! Somos o grupo do PetClean — eu sou a Helen, e junto comigo estão o Gabriel e o João Vitor. Vamos apresentar a API do PetClean, o back-end Java do nosso Projeto Interdisciplinar.

A ideia é simples: o painel que vocês já conhecem só funciona porque existe uma API por trás. É ela que guarda os clientes, os pets, os agendamentos e o estoque. Hoje mostramos como essa API foi construída — os modelos, o banco H2, os repositories, a documentação no Swagger e os endpoints com as regras de negócio.

Dividimos a apresentação em três blocos: eu começo pelos modelos e entidades, o Gabriel segue com banco de dados e repositories e o João Vitor fecha com Swagger, CRUD e endpoints especializados.


### Slide 02 — Roteiro

Antes de começar, só para vocês saberem onde estamos indo.

A apresentação tem três blocos, um para cada integrante. Eu começo pelo modelo de dados: como o PetClean representa clientes, pets, agendamentos e estoque no código Java. O Gabriel continua com a camada de persistência — o banco H2 e os repositories. E o João Vitor fecha com a parte que todo mundo vê: a documentação no Swagger, o CRUD e os endpoints que carregam as regras de negócio.

A ordem não é por acaso: ela é exatamente o caminho que uma requisição faz dentro do projeto.


### Slide 03 — Arquitetura

Antes de entrar nas entidades, vale entender onde elas vivem.

O projeto está dividido em camadas, igual ao padrão que a gente viu na disciplina. A requisição entra pelo control, que só cuida de HTTP: recebe o JSON, valida com Bean Validation e devolve o status certo. Ele chama o service, que é onde ficam as regras de negócio — por exemplo, checar conflito de horário. O service fala com o repository, e o repository com o banco H2.

Essa separação é o que permite testar as regras sem subir servidor: a maioria dos nossos testes ataca o service direto. E o GlobalExceptionHandler garante que qualquer erro saia no mesmo formato JSON, o que o painel consegue mostrar em qualquer tela.


### Slide 04 — Entidades

Este é o coração do projeto: seis entidades que cobrem todo o domínio de um pet shop.

Cliente é o tutor. Pet está sempre vinculado a um cliente — a chave estrangeira é obrigatória. Agendamento amarra cliente, pet, serviço, data e hora, e guarda o valor e a duração calculados a partir do serviço, não digitados pelo usuário.

Produto controla o estoque com quantidade e estoque mínimo, e MovimentacaoEstoque guarda o histórico de cada entrada e saída. Por último, Usuario, que cuida do acesso ao painel com senha em bcrypt.

Repare que os campos que só podem ter alguns valores viraram enums — espécie, porte, serviço, status, categoria, tipo de movimentação e perfil. Isso evita status escrito errado no banco e faz o Swagger listar as opções automaticamente.


### Slide 05 — Relacionamentos

Aqui estão as três ligações principais. Cliente para pet é um para muitos: um tutor pode ter vários pets, mas cada pet tem um tutor. Agendamento aponta para o cliente e para o pet ao mesmo tempo, porque na tela a gente precisa mostrar os dois.

Esses vínculos não são só desenho: eles viraram regra. O ClienteService consulta se o cliente tem pets antes de excluir; o PetService checa se existe agendamento futuro. Se existir, a API devolve 409 com uma mensagem explicando o motivo, em vez de quebrar o banco.

E os enums são gravados como texto — @Enumerated STRING. Isso deixa o banco legível quando abrimos o console do H2, e qualquer valor inválido nem compila.


### Slide 06 — Código da entidade

Para fechar meu bloco, um pedaço real do código, sem simplificação.

Em quatro linhas a gente tem o essencial: a classe vira tabela, o cliente vira chave estrangeira obrigatória, a espécie é um enum gravado como texto e cada campo tem uma descrição que aparece no Swagger.

Uma decisão importante: a validação de faixa, tipo idade entre 0 e 40, fica no DTO, não na entidade. A entidade representa o dado; o DTO representa o que o usuário pode enviar. Com isso eu passo a palavra para o Gabriel falar do banco.


## Bloco 02 — Banco de Dados e Repositories

**Gabriel Wagner** · slides 7 a 10

### Slide 07 — Bloco 02

Obrigado, Helen. Meu bloco é o que fica embaixo da API: onde os dados realmente moram. Vou mostrar o banco H2, como ele é configurado, a carga inicial de dados e depois os repositories — incluindo as consultas que escrevemos na mão.


### Slide 08 — Banco H2

O enunciado permitia usar o H2, e a gente escolheu justamente por ser em memória: o projeto sobe, cria as tabelas e carrega os dados de demonstração sozinho. Ninguém precisa instalar MySQL para rodar na sua máquina.

São quatro linhas de configuração que importam: a URL jdbc:h2:mem:petcleandb, o console habilitado em /h2-console, o ddl-auto create — que recria o schema a cada subida — e o defer-datasource-initialization com sql.init.mode always, que garante que o data.sql rode depois do Hibernate criar as tabelas.

O data.sql tem 71 inserts: 8 clientes, 10 pets, 24 agendamentos, 10 produtos, 15 movimentações e 4 usuários. As datas dos agendamentos são relativas, com DATEADD, para o dashboard nunca aparecer vazio, independentemente do dia da apresentação.

E como é em memória, ao parar a aplicação tudo é descartado — o que é ótimo para demonstração: cada ./mvnw spring-boot:run começa de um estado conhecido.


### Slide 09 — Repositories

O Spring Data JPA resolve a maior parte do trabalho pesado. As seis interfaces estendem JpaRepository e, só com isso, cada entidade já tem findAll, findById, save, deleteById e paginação. Não existe classe de implementação no projeto — o Spring gera o proxy em tempo de execução.

Quando o método padrão não serve, a gente desce um nível. Primeiro os query methods: o nome do método é a consulta. findByClienteIdOrderByNome quer dizer 'busque por id do cliente, ordenado por nome'. existsByCpf resolve a duplicidade de CPF, countByClienteId conta os pets do tutor.

E quando a consulta é mais complexa — filtro com like, contagem de conflito de horário, agregação por mês — a gente escreve com @Query, em HQL ou SQL nativo. Isso me leva ao próximo slide.


### Slide 10 — Consultas

Essa dupla de métodos mostra bem a evolução. A primeira consulta é HQL e devolve a entidade Pet inteira, com todos os relacionamentos. É o que a tela de edição precisa.

A segunda é SQL nativo com projection: um select que traz só nome, espécie e nome do tutor. A interface PetResumoProjection é uma interface com três getters, e o Spring preenche direto — não existe classe, não existe mapeamento manual.

Isso importa porque a listagem de pets aparece no dashboard e precisa ser leve. Volume de dados baixo aqui, mas o hábito é o que vale: busque só o que a tela mostra.

Tem ainda um detalhe de regra: o estoque crítico já vem ordenado pelo banco, do maior déficit para o menor. A ordenação é decisão de negócio, então mora na consulta, não no JavaScript.


## Bloco 03 — Swagger, CRUD e Endpoints Especializados

**Joao Vitor Silva** · slides 11 a 15

### Slide 11 — Bloco 03

Boa, Gabriel. Eu fecho mostrando a parte que dá para ver funcionando: a documentação no Swagger, o CRUD completo e os endpoints que carregam as regras de negócio do PetClean.


### Slide 12 — Swagger

Boa noite. Fecho o grupo mostrando o que o Swagger faz por nós.

A configuração é uma classe só. O springdoc lê os controllers e gera a especificação OpenAPI automaticamente — quem escreve a documentação é o próprio código. É por isso que os @Operation e @Schema que a Helen mostrou fazem diferença: eles viram o texto que aparece aqui.

A parte que a gente adicionou de propósito foi o esquema de segurança: a nossa autenticação é sessão por cookie, então o Swagger precisa saber que existe um cookie chamado PETCLEANSESSION. Sem isso, toda rota protegida responde 401 e não dá para testar nada.

Na prática: abre /swagger-ui.html, executa o POST /login, o navegador guarda o cookie e a partir daí os endpoints de clientes, pets, agendamentos e estoque funcionam direto na tela, sem Postman. As tags numeradas organizam os endpoints por épico do projeto.


### Slide 13 — CRUD

Sobre o CRUD: as quatro operações existem para todas as entidades principais, então são 48 endpoints no total. O que importa aqui é que cada uma devolve o status correto.

POST devolve 201 com o Location do recurso criado — não 200. DELETE devolve 204, sem corpo. E o DELETE do cliente é o exemplo perfeito de regra de negócio no CRUD: se o cliente tem pet ou agendamento, ele não apaga, devolve 409 e explica o motivo. Produto é parecido: com histórico de movimentação, o certo é inativar em vez de excluir, e existe um PATCH específico para isso.

Os erros também são padronizados pelo GlobalExceptionHandler: 400 para corpo inválido, 401 quando não tem sessão, 404 quando o id não existe, 409 para conflito e 422 para regra não atendida, como a foto acima de 2 MB.


### Slide 14 — Especializados

O último requisito era o que mais gostei de fazer: endpoints que não são CRUD, que existem por causa de uma regra do PetClean.

Alguns são consultas: busca por termo em clientes, filtro combinado de nome e categoria no estoque, agenda do dia. Outros são operações que só fazem sentido no nosso domínio: o conflito de horário, que impede dois banhos no mesmo horário e devolve 409 sem gravar nada; o estoque crítico já ordenado pelo déficit; e o dashboard, que devolve os KPIs e o gráfico de oito semanas ou seis meses.

Cada um desses endpoints corresponde a uma história de usuário do relatório. Dá para rastrear: a US-17 é o conflito, a US-20 é o alerta de estoque crítico, a US-23 é o gráfico por período.


### Slide 15 — Fechamento

Fechando: os seis requisitos do trabalho estão entregues. Modelos e entidades com as seis classes JPA, banco H2 em memória com carga inicial, repositories com Spring Data, Swagger configurado e documentado, CRUD completo e os endpoints especializados com as regras do PetClean.

Tudo isso roda com um comando, e os links para testar estão aqui. Obrigado — ficamos à disposição para perguntas.


---

## Dicas de condução

- **Passagem de bastão:** cada bloco termina com uma frase que entrega a palavra.
- **Se precisar encurtar:** os slides 3 (arquitetura) e 5 (relacionamentos) podem
  ser resumidos em uma frase; os slides de código (06, 09, 12) devem ser mantidos.
- **Demonstração ao vivo (opcional):** abrir `localhost:8080/swagger-ui.html`
  depois do slide 12 é o momento de maior impacto.
