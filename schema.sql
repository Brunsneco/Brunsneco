CREATE TABLE "Cadastro" (
	"id"	INTEGER,
	"Criado"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"Nome"	TEXT NOT NULL,
	"Email"	TEXT NOT NULL,
	"Telefone"	TEXT,
	"Genero"	TEXT,
	"Nascimento"	TEXT NOT NULL,
	"Cidade"	TEXT NOT NULL,
	"Estado"	TEXT,
	"Endereco"	TEXT,
	"User"	TEXT NOT NULL,
	"Senha"	TEXT NOT NULL,
	"SenhaConfirm"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);