import requests
import json
import time
import mysql.connector


url = 'https://carroya-pro-portal-api.avaldigitallabs.com/find-filters'
myobj = {
  "seoArray": [],
  "params": {
    "page": "1",
    "category": "Automóviles y Camionetas",
    "status": "usado"
  }
}
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="Scrap1"
)

class rueda:

	def getModels(self, marca):
		myobj["params"]["brand"] = marca
		if "model" in myobj["params"]:
			myobj["params"].pop("model")
		x = requests.post(url, json = myobj)
		y = json.loads(x.text)
		print("query")
		print(myobj["params"])
		#print(y['results']['filter-line'])

		for modelo in y['results']['filter-line']:
			if self.getModeloId(modelo['data']) == -1:

				sql = "INSERT INTO Modelo (Modelo, Marca_P) Values (%s, %s) "
				idMarca = self.getMarcaId(marca)
				val = (modelo['data'], idMarca[0])
				mycursor = mydb.cursor(buffered=True)
				mycursor.execute(sql, val)
				mydb.commit()
				print(mycursor.rowcount, "record inserted.")

			#Aca se gdebe guardar el modelo relacionado con la marca
			print("-------"+modelo['data']+"------------------------------------")
			self.getCars(modelo['data'], y['pages'])

			

	def getCars(self, modelo, tope):
		
			
			myobj["params"]["model"] = modelo
			#print(myobj["params"])
			print("tope: "+str(tope))
			pagina = 1
			while pagina < int(tope):
				print("Pagina: "+str(pagina))
				myobj["params"]["page"] = pagina
				x = requests.post(url, json = myobj)
				y = json.loads(x.text)
				print("tope: ", y['pages'])
				tope = y['pages']
				for carro1 in y['results']['megaHighlights']:
					"""
					print(carro1['brand'])
					print(carro1['model'])
					print(carro1['year'])
					print(carro1['city'])
					print(carro1['id'])
					"""
					print('/detalle/usado/'+carro1['brand']+'/'+carro1['model']+'/'+str(carro1['year'])+'/'+carro1['city']+'/'+str(carro1['id']))
					#print(carro1['detail'])
					self.insertCarro(carro1, modelo)
				for carro1 in y['results']['superHighlights']:
					#print(carro1['detail'])
					print('/detalle/usado/'+carro1['brand']+'/'+carro1['model']+'/'+str(carro1['year'])+'/'+carro1['city']+'/'+str(carro1['id']))
					self.insertCarro(carro1, modelo)
				#time.sleep(1);
				pagina += 1;

	def insertCarro(self, carroData, modelo):
		#print(carroData)
		lista = {"Ano": "year", "Version": "clinea2", "Kilometros": "kilometers", "Transmision": "ctipocaja", "Departamento":"cdivision", "Color":"color", "Combustible":"ccombustible", "Puertas":"", "Motor":"cylindrical", "Carroceria":"ctipo", "Precio":"cprecioint", "Dias_Publicado":"cfechapublicacion"}
		lista2 = {"Ano": "year", "Version": "clinea2", "Kilometros": "kilometers", "Transmision": "ctipocaja", "Departamento":"cdivision", "Color":"color", "Combustible":"ccombustible", "Puertas":"", "Motor":"cylindrical", "Carroceria":"ctipo", "Precio":"cprecioint", "Dias_Publicado":self.getDiasPorFecha(carroData['cfechapublicacion']), "URL":'/detalle/usado/'+carroData['brand']+'/'+carroData['model']+'/'+str(carroData['year'])+'/'+carroData['city']+'/'+str(carroData['id']), "Modelo_p":str(self.getModeloId(modelo))}
		
		#print("--------DATOS--------")
		indices = []
		valores = []
		for key in lista.keys():
			if lista[key] in carroData:
				#print(key+" -- "+lista[key])
				indices.append(key)
				if key == "Dias_Publicado":
					valores.append(str(self.getDiasPorFecha(carroData['cfechapublicacion'])))
				else:	
					valores.append('"'+str(carroData[lista[key]])+'"')
		indices.append("URL")
		valores.append('"/detalle/usado/'+carroData['brand']+'/'+carroData['model']+'/'+str(carroData['year'])+'/'+carroData['city']+'/'+str(carroData['id'])+'"')
		indices.append("Modelo_p")
		valores.append(str(self.getModeloId(modelo)))
		#print("----------------")
		indices2 = ", ".join(indices)
		valores2 = ", ".join(valores)
		sql = "INSERT INTO Carro ("+indices2+") Values ("+valores2+") "
		#val = (carroData[''], carroData[''], carroData[''], carroData[''], carroData[''], carroData[''], carroData[''], "", carroData[''], carroData[''], carroData[''], , , ,)
		#print(sql)
		existe = self.carroExiste('/detalle/usado/'+carroData['brand']+'/'+carroData['model']+'/'+str(carroData['year'])+'/'+carroData['city']+'/'+str(carroData['id']))
		if existe == False:
			mycursor = mydb.cursor(buffered=True)
			mycursor.execute(sql)
			mydb.commit()
			print(mycursor.rowcount, "carro inserted.")
		
	def getDiasPorFecha(self, fecha):
		return "'"+fecha+"'"		
			
	def getMarcaId(self, Marca):
		sql = "SELECT * FROM Marca WHERE Marca = %s"
		val = (Marca,)
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute(sql, val)
		myresult = mycursor.fetchall()
		for x in myresult:	
			print("Consulta: "+str(x))
		if len(myresult) > 0:
			return myresult[0]
		else:
			return -1

	def getModeloId(self, Modelo):
		sql = "SELECT * FROM Modelo WHERE Modelo = %s"
		val = (Modelo,)
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute(sql, val)
		myresult = mycursor.fetchall()
		for x in myresult:	
			pass
			#print("Consulta: "+str(x))
		if len(myresult) > 0:
			return myresult[0][0]
		else:
			return -1

	def carroExiste(self, URL):
		sql = "SELECT * FROM Carro WHERE URL = %s"
		val = (URL,)
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute(sql, val)
		myresult = mycursor.fetchall()
		print("carro: "+URL)
		for x in myresult:	
			print("Consulta Carro: "+str(x))
		if len(myresult) > 0:
			return True
		else:
			return False


	def __init__(self):
		x = requests.post(url, json = myobj)
		y = json.loads(x.text)
		
		for marca in y['results']['filter-brand']:
			#ACA debe haber un insert de marca
			if self.getMarcaId(marca['data']) == -1:
				sql = "INSERT INTO Marca (Marca) Values (%s) "
				val = (marca['data'],)
				mycursor = mydb.cursor(buffered=True)
				mycursor.execute(sql, val)
				mydb.commit()
				print(mycursor.rowcount, "record inserted.")
			
			print("---------------get "+marca['data']+"-----------------------------------")		
			self.getModels(marca['data'])
			print("-------------------------------------------------------")


	
#print(y['results']['filter-brand'])

rueda()