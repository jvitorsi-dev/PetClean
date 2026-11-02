-- =====================================================================
-- PetClean - carga inicial de dados de demonstracao
-- Executado automaticamente na subida da aplicacao (spring.sql.init)
-- Datas relativas (DATEADD) mantem o dashboard sempre com dados.
-- =====================================================================

-- ---------------------------------------------------------------------
-- EP-06 - Usuarios (RNF-04: senhas em hash bcrypt)
--   helen@petclean.com / gabriel@petclean.com / joao@petclean.com => petclean123
--   gestor@petclean.com => gestor123
-- ---------------------------------------------------------------------
insert into usuario (nome, email, senha_hash, perfil) values ('Helen Vitoria Silva Aclina', 'helen@petclean.com', '$2a$10$tMT7m8XFXufr/Jro6D.uWOr7p/3YxHhX0rKIvOlAvxFKaeQ80XzmW', 'ATENDENTE');
insert into usuario (nome, email, senha_hash, perfil) values ('Gabriel Wagner dos Santos Lira', 'gabriel@petclean.com', '$2a$10$tMT7m8XFXufr/Jro6D.uWOr7p/3YxHhX0rKIvOlAvxFKaeQ80XzmW', 'GESTOR');
insert into usuario (nome, email, senha_hash, perfil) values ('Joao Vitor', 'joao@petclean.com', '$2a$10$tMT7m8XFXufr/Jro6D.uWOr7p/3YxHhX0rKIvOlAvxFKaeQ80XzmW', 'ATENDENTE');
insert into usuario (nome, email, senha_hash, perfil) values ('Marina Gestora', 'gestor@petclean.com', '$2a$10$vXJEekQymeC.90UmMr0hCuGFBomJHn.EV2xyRkuNikRM7JutHmu1.', 'GESTOR');

-- ---------------------------------------------------------------------
-- EP-01 - Clientes (US-03 / US-15)
-- ---------------------------------------------------------------------
insert into cliente (nome, cpf, telefone, email, endereco) values ('Maria da Silva', '12345678909', '(11) 98765-4321', 'maria.silva@email.com', 'Rua das Flores, 100 - Santo Andre/SP');
insert into cliente (nome, cpf, telefone, email, endereco) values ('Carlos Pereira', '11144477735', '(11) 97654-3210', 'carlos.pereira@email.com', 'Av. Industrial, 245 - Santo Andre/SP');
insert into cliente (nome, cpf, telefone, email, endereco) values ('Ana Beatriz Souza', '52998224725', '(11) 96543-2109', 'ana.souza@email.com', 'Rua das Acacias, 47 - Sao Bernardo do Campo/SP');
insert into cliente (nome, cpf, telefone, email, endereco) values ('Rodrigo Almeida', '46801234510', '(11) 95432-1098', 'rodrigo.almeida@email.com', 'Rua Ipiranga, 890 - Sao Caetano do Sul/SP');
insert into cliente (nome, cpf, telefone, email, endereco) values ('Juliana Costa', '35178945670', '(11) 94321-0987', 'juliana.costa@email.com', 'Rua Vergueiro, 1200 - Sao Paulo/SP');
insert into cliente (nome, cpf, telefone, email, endereco) values ('Fernando Lima', '78912365428', '(11) 93210-9876', 'fernando.lima@email.com', 'Rua das Palmeiras, 33 - Maua/SP');
insert into cliente (nome, cpf, telefone, email, endereco) values ('Patricia Nogueira', '45678912364', '(11) 92109-8765', 'patricia.nogueira@email.com', 'Av. Kennedy, 550 - Diadema/SP');
insert into cliente (nome, cpf, telefone, email, endereco) values ('Bruno Martins', '23456789173', '(11) 91098-7654', 'bruno.martins@email.com', 'Rua Amazonas, 78 - Ribeirao Pires/SP');

-- ---------------------------------------------------------------------
-- EP-02 - Pets (US-07)
-- ---------------------------------------------------------------------
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (1, 'Thor', 'CACHORRO', 'Golden Retriever', 'GRANDE', 4);
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (1, 'Mel', 'CACHORRO', 'Poodle', 'PEQUENO', 2);
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (2, 'Nina', 'GATO', 'Siamês', 'PEQUENO', 3);
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (3, 'Bob', 'CACHORRO', 'Buldogue Francês', 'MEDIO', 5);
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (3, 'Luna', 'GATO', 'Persa', 'PEQUENO', 1);
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (4, 'Simba', 'GATO', 'SRD', 'MEDIO', 6);
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (5, 'Rex', 'CACHORRO', 'Pastor Alemão', 'GRANDE', 7);
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (6, 'Pipoca', 'AVE', 'Calopsita', 'PEQUENO', 1);
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (7, 'Bidu', 'CACHORRO', 'SRD', 'MEDIO', 8);
insert into pet (fk_cliente, nome, especie, raca, porte, idade) values (8, 'Amora', 'CACHORRO', 'Shih Tzu', 'PEQUENO', 3);

-- ---------------------------------------------------------------------
-- EP-03 - Agendamentos (US-11 a US-17)
-- Historico das ultimas 8 semanas (US-23) + dia atual + proximos dias
-- ---------------------------------------------------------------------
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (1, 1, 'BANHO_E_TOSA', DATEADD('DAY', -52, CURRENT_DATE), TIME '09:00', 85.00, 75, 'REALIZADO', null, DATEADD('DAY', -52, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (2, 3, 'BANHO', DATEADD('DAY', -50, CURRENT_DATE), TIME '10:00', 45.00, 45, 'REALIZADO', null, DATEADD('DAY', -50, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (3, 4, 'TOSA', DATEADD('DAY', -45, CURRENT_DATE), TIME '14:00', 50.00, 40, 'REALIZADO', null, DATEADD('DAY', -45, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (4, 6, 'CONSULTA_VETERINARIA', DATEADD('DAY', -44, CURRENT_DATE), TIME '11:30', 120.00, 30, 'REALIZADO', 'Vacina anual', DATEADD('DAY', -44, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (5, 7, 'BANHO_E_TOSA', DATEADD('DAY', -38, CURRENT_DATE), TIME '08:30', 85.00, 75, 'REALIZADO', null, DATEADD('DAY', -38, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (6, 8, 'HIDRATACAO', DATEADD('DAY', -37, CURRENT_DATE), TIME '16:00', 60.00, 50, 'CANCELADO', 'Cliente desmarcou', DATEADD('DAY', -38, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (7, 9, 'BANHO', DATEADD('DAY', -31, CURRENT_DATE), TIME '09:30', 45.00, 45, 'REALIZADO', null, DATEADD('DAY', -31, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (8, 10, 'TOSA', DATEADD('DAY', -30, CURRENT_DATE), TIME '13:00', 50.00, 40, 'REALIZADO', null, DATEADD('DAY', -30, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (1, 2, 'BANHO', DATEADD('DAY', -25, CURRENT_DATE), TIME '10:30', 45.00, 45, 'REALIZADO', null, DATEADD('DAY', -25, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (2, 3, 'BANHO_E_TOSA', DATEADD('DAY', -23, CURRENT_DATE), TIME '15:00', 85.00, 75, 'REALIZADO', null, DATEADD('DAY', -23, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (3, 5, 'CONSULTA_VETERINARIA', DATEADD('DAY', -17, CURRENT_DATE), TIME '11:00', 120.00, 30, 'REALIZADO', null, DATEADD('DAY', -17, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (5, 7, 'BANHO', DATEADD('DAY', -16, CURRENT_DATE), TIME '09:00', 45.00, 45, 'REALIZADO', null, DATEADD('DAY', -16, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (6, 8, 'BANHO', DATEADD('DAY', -10, CURRENT_DATE), TIME '14:30', 45.00, 45, 'REALIZADO', null, DATEADD('DAY', -10, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (7, 9, 'HIDRATACAO', DATEADD('DAY', -9, CURRENT_DATE), TIME '10:00', 60.00, 50, 'REALIZADO', null, DATEADD('DAY', -9, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (8, 10, 'BANHO_E_TOSA', DATEADD('DAY', -5, CURRENT_DATE), TIME '08:00', 85.00, 75, 'REALIZADO', null, DATEADD('DAY', -5, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (1, 1, 'BANHO', DATEADD('DAY', -2, CURRENT_DATE), TIME '09:00', 45.00, 45, 'REALIZADO', null, DATEADD('DAY', -2, CURRENT_TIMESTAMP));
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (4, 6, 'TOSA', DATEADD('DAY', -1, CURRENT_DATE), TIME '15:30', 50.00, 40, 'REALIZADO', null, DATEADD('DAY', -1, CURRENT_TIMESTAMP));
-- dia atual
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (1, 2, 'BANHO_E_TOSA', CURRENT_DATE, TIME '09:00', 85.00, 75, 'CONFIRMADO', null, CURRENT_TIMESTAMP);
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (3, 4, 'CONSULTA_VETERINARIA', CURRENT_DATE, TIME '11:00', 120.00, 30, 'AGENDADO', null, CURRENT_TIMESTAMP);
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (5, 7, 'BANHO', CURRENT_DATE, TIME '14:00', 45.00, 45, 'AGENDADO', 'Pet idoso, manejo cuidadoso', CURRENT_TIMESTAMP);
-- proximos dias
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (2, 3, 'BANHO', DATEADD('DAY', 1, CURRENT_DATE), TIME '10:00', 45.00, 45, 'AGENDADO', null, CURRENT_TIMESTAMP);
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (6, 8, 'TOSA', DATEADD('DAY', 2, CURRENT_DATE), TIME '13:30', 50.00, 40, 'AGENDADO', null, CURRENT_TIMESTAMP);
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (7, 9, 'BANHO_E_TOSA', DATEADD('DAY', 3, CURRENT_DATE), TIME '09:30', 85.00, 75, 'AGENDADO', null, CURRENT_TIMESTAMP);
insert into agendamento (fk_cliente, fk_pet, servico, data, hora, valor, duracao_minutos, status, observacao, atualizado_em) values (8, 10, 'HIDRATACAO', DATEADD('DAY', 5, CURRENT_DATE), TIME '16:00', 60.00, 50, 'AGENDADO', null, CURRENT_TIMESTAMP);

-- ---------------------------------------------------------------------
-- EP-04 - Produtos do estoque (US-18 / US-20)
-- Itens 2, 4, 7 e 8 estao com estoque critico (quantidade <= estoque_minimo)
-- ---------------------------------------------------------------------
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Ração Premium Adulto 10kg', 'RACAO', 12, 5, 189.90, true);
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Ração Filhote 5kg', 'RACAO', 3, 5, 129.90, true);
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Shampoo Antipulgas 500ml', 'HIGIENE', 8, 3, 34.90, true);
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Antipulgas Comprimido', 'MEDICAMENTO', 2, 6, 79.90, true);
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Brinquedo Morder Resistente', 'BRINQUEDO', 15, 4, 24.90, true);
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Coleira Peitoral Tam. M', 'ACESSORIO', 6, 2, 59.90, true);
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Condicionador Pet 500ml', 'HIGIENE', 1, 4, 29.90, true);
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Vermífugo Suspensão 10ml', 'MEDICAMENTO', 0, 3, 45.00, true);
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Areia Sanitária 4kg', 'OUTRO', 9, 5, 39.90, true);
insert into produto (nome, categoria, quantidade, estoque_minimo, preco, ativo) values ('Petisco Natural 300g', 'OUTRO', 4, 2, 19.90, true);

-- ---------------------------------------------------------------------
-- US-19 - Historico de movimentacoes
-- O produto 10 nao possui movimentacao, permitindo demonstrar a exclusao (US-21)
-- ---------------------------------------------------------------------
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (1, 'ENTRADA', 20, 'Nota fiscal 1123 - Distribuidora Pet', DATEADD('DAY', -40, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (1, 'SAIDA', 8, 'Vendas do mes', DATEADD('DAY', -20, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (2, 'ENTRADA', 10, 'Nota fiscal 1188', DATEADD('DAY', -35, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (2, 'SAIDA', 7, 'Vendas do mes', DATEADD('DAY', -12, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (3, 'ENTRADA', 12, 'Compra de reposicao', DATEADD('DAY', -30, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (3, 'SAIDA', 4, 'Uso nos banhos', DATEADD('DAY', -8, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (4, 'ENTRADA', 6, 'Compra de reposicao', DATEADD('DAY', -28, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (4, 'SAIDA', 4, 'Vendas no balcao', DATEADD('DAY', -6, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (5, 'ENTRADA', 15, 'Compra de reposicao', DATEADD('DAY', -25, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (6, 'ENTRADA', 6, 'Compra de reposicao', DATEADD('DAY', -22, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (7, 'ENTRADA', 5, 'Compra de reposicao', DATEADD('DAY', -18, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (7, 'SAIDA', 4, 'Uso nos banhos', DATEADD('DAY', -5, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (8, 'ENTRADA', 3, 'Compra de reposicao', DATEADD('DAY', -15, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (8, 'SAIDA', 3, 'Vendas no balcao', DATEADD('DAY', -3, CURRENT_TIMESTAMP));
insert into movimentacao_estoque (fk_produto, tipo, quantidade, observacao, registrado_em) values (9, 'ENTRADA', 9, 'Compra de reposicao', DATEADD('DAY', -14, CURRENT_TIMESTAMP));

-- ---------------------------------------------------------------------
-- Reinicia as sequences: os inserts acima nao informam id, mas os vinculos
-- (fk_cliente, fk_pet, fk_produto) usam a ordem 1..N da carga inicial.
-- ---------------------------------------------------------------------
alter table usuario alter column id restart with 5;
alter table cliente alter column id restart with 9;
alter table pet alter column id restart with 11;
alter table agendamento alter column id restart with 25;
alter table produto alter column id restart with 11;
alter table movimentacao_estoque alter column id restart with 16;
