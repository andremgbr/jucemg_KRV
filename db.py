import sqlite3
conn = conn = sqlite3.connect('database.db')

def set_data_viabilidade(prot,nome,situa,data):
	cur = conn.cursor()
	cur.execute("""INSERT INTO Consulta_Viabilidade (Protocolo,Primeira_opcao_Nome,Situacao_da_Analise,Data_de_cadastro,Baixado)
	VALUES (?,?,?,?,?)""",(prot,nome,situa,data,"0"))
	conn.commit()
	cur.close()


def find_data_viabilidade(protocol):
	cur = conn.cursor()
	t = (protocol,)
	test = cur.execute("SELECT * FROM Consulta_Viabilidade WHERE Protocolo =?",t,).fetchone()
	cur.close()
	if test == None:
		return False
	else:
		return True



def consultar_data():
	cur = conn.cursor()
	temp = cur.execute("SELECT Protocolo FROM Consulta_Viabilidade WHERE Baixado = 0",).fetchall()
	data = []
	for i in temp:
		data.append(i[0])
	cur.close()
	return data



def update_data(protocolo,t):
	cur = conn.cursor()
	data = cur.execute("UPDATE Consulta_Viabilidade SET Baixado = 1, Situacao_da_Analise = ? WHERE Protocolo = ?",(str(t),protocolo,))
	conn.commit()
	cur.close()
