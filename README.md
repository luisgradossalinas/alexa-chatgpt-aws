# Integración de Alexa Skill con ChatGPT usando servicios de AWS (Lambda, Secrets Manager y DynamoDB)

<img width="991" src="https://user-images.githubusercontent.com/2066453/233669157-99ea9943-90cd-4d2d-8793-0b725036904f.png">

## Requisitos

- [Tener una cuenta en AWS](https://gist.github.com/luisgradossalinas/c233c0333022c6617dd70609bfdf6441)
- [Tener una cuenta en OpenAI](https://gist.github.com/luisgradossalinas/45c1c5ed27b7f73e0d3cf3bc0fbe846d)

## Video con la explicación

Youtube - https://www.youtube.com/watch?v=fwTLeF1DOVk

[![aws](https://user-images.githubusercontent.com/2066453/233724168-3947aa77-a608-4951-a1d8-bcd377e4c505.png)](https://www.youtube.com/watch?v=fwTLeF1DOVk)

## Creando Skill en Alexa

Ir a https://developer.amazon.com/alexa/console/ask/create-new-skill/name, definimos un nombre para nuestro skill

<img width="991" src="https://user-images.githubusercontent.com/2066453/222503030-61148526-c1b7-4422-a5d8-4375ad2e43cd.png">

Elegimos:

- Choose a type of experience : Other
- Choose a model : Custome
- Hosting services : Provision your own.

Clic en NEXT

![Captura de Pantalla 2023-02-24 a la(s) 16 59 13](https://user-images.githubusercontent.com/2066453/221301265-3ff49fc3-1336-4de2-a394-b6392b636de5.png)

Clic en Start from Scratch y Next.

![Captura de Pantalla 2023-02-24 a la(s) 17 00 40](https://user-images.githubusercontent.com/2066453/221301472-b4b9a280-720d-4f77-a86e-2c128e13034d.png)

Clic en Create Skill.

![Captura de Pantalla 2023-02-24 a la(s) 17 05 17](https://user-images.githubusercontent.com/2066453/221302213-8f9d9466-c265-4622-9e37-dad0e087c42f.png)

Nos aparecerá la siguiente pantalla.

![Captura de Pantalla 2023-02-24 a la(s) 17 13 43](https://user-images.githubusercontent.com/2066453/221303471-48b6f99f-9d92-4b0c-aa16-09fb153da3a5.png)

Definimos una palabra para invocar a nuestro skill.

<img width="892" src="https://user-images.githubusercontent.com/2066453/222496118-33986a70-9d08-4837-8d7c-5af2177efc15.png">

Agregaremos las intenciones con los utterances al Skill, clic en JSON editor.
Copiamos el contenido del json que se encuentra en la ruta skill/alexa-skill.json y lo pegamos, clic en Save model.

<img width="991" src="https://user-images.githubusercontent.com/2066453/233673883-719fc575-0538-43ed-ba8a-2b4cdf0644c4.png">

Veremos las 2 intenciones que se han agregado : PreguntaIntent y DespedidaIntent.

<img width="991" src="https://user-images.githubusercontent.com/2066453/233674483-94331ef4-66df-4e55-b35d-398d4194381a.png">

Clic en Save model y Build Model.

![Captura de Pantalla 2023-02-24 a la(s) 17 36 12](https://user-images.githubusercontent.com/2066453/221308472-451daaf4-3606-49e4-82db-0549ce9fc10a.png)

## Accedemos a nuestra cuenta de AWS y creamos un entorno de Cloud9, donde clonaremos el repositorio.

<img width="991" src="https://user-images.githubusercontent.com/2066453/233682805-64683d49-1ff9-44f5-8335-d4f7fd7471ce.png">

Ejecutar en Cloud9.

	git clone https://github.com/luisgradossalinas/alexa-chatgpt-aws

Abrir el contenido del archivo chatgpt.yaml e ingresamos en la línea 40 nuestro API Key de OpenAI.

<img width="791" src="https://user-images.githubusercontent.com/2066453/233698021-ac835ab5-63aa-4c2d-8c87-4bec57423c7d.png">

Ejecutar en Cloud9

	cd alexa-chatgpt-aws/
	sh sh/01_Start_Deploy.sh

Esperamos que se cree el stack en CloudFormation.

<img width="691" src="https://user-images.githubusercontent.com/2066453/233698317-b171b5a9-d45c-4909-b745-6d94a677aed7.png">

Volvemos a Alexa y nos ubicamos en la opción Endpoint, copiamos el valor de nuestro Skill ID para asociarlo a la función Lambda creada en AWS.

<img width="691" src="https://user-images.githubusercontent.com/2066453/233698594-cb5d5e21-8106-4306-b79f-d35c06376ef2.png">

Regresamos a AWS, y entramos a la función Lambda llamada : fnc-alexa-skill-chatgpt-dynamodb, para agregar un desencadenador. Clic en Add trigger.

<img width="691" src="https://user-images.githubusercontent.com/2066453/233698933-28c9308f-e524-47ce-9857-8706b54253e7.png">

Seleccionamos Alexa e ingresamos nuestro Skill ID, clic en Add.

<img width="691" src="https://user-images.githubusercontent.com/2066453/233699263-e12b70e1-016d-4ea4-93b9-8a6c3b30090d.png">

Ahora copiamos el ARN de la función Lambda, para asociarlo al Skill de Alexa.

<img width="691" src="https://user-images.githubusercontent.com/2066453/233699532-26e0c588-849d-4897-b180-fd70232ebd8e.png">

Volvemos a Alexa Console y pegamos el valor del ARN de la función Lambda, clic en Save Endpoints.

<img width="691" src="https://user-images.githubusercontent.com/2066453/233699750-eea55320-18db-4e01-8cee-3f7f1bb530f8.png">

Clic en Test para probar desde la consola nuestra Skill.

![image](https://user-images.githubusercontent.com/2066453/233701986-f285221c-d4c8-49bf-967b-8d09c39edb38.png)

Ahora puedes preguntar lo que desees a ChatGPT usando una Skill de Alexa.

![image](https://user-images.githubusercontent.com/2066453/233707636-c2bf8596-465d-45d1-b44a-451908ab7623.png)

Si queremos ver esta interacción (pregunta y respuesta de ChatGPT), podemos ir a AWS, al servicio de DynamoDB y en la tabla chatgpt_interaction veremos un registro con la pregunta y respuesta de ChatGPT.

![image](https://user-images.githubusercontent.com/2066453/233708715-f7f7983e-a393-4838-89ba-1a9dcf666921.png)

Si tenemos un dispositivo Echo Dot, también podemos utilizar esta skill.

## Agradecimientos

Espero te haya servido esta solución, si pudiste replicarlo, puedes publicarlo en LinkedIn con tus aportes, cambios y etiquétame (https://www.linkedin.com/in/luisgrados).

## Eliminar recursos en AWS

Ejecutar en Cloud9.

	aws s3 ls | grep alexachatgpt-code | awk {'print "aws s3 rb s3://" $3 " --f"'} | sh
	aws cloudformation delete-stack --stack-name StackAlexaChatGPT	
	echo "Stack StackAlexaChatGPT eliminándose"

Eliminamos el entorno de Cloud9.
