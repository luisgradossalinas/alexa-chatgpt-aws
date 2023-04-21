# Integración de Alexa Skill con ChatGPT usando servicios de AWS (Lambda, Secrets Manager y DynamoDB)

<img width="991" src="https://user-images.githubusercontent.com/2066453/233669157-99ea9943-90cd-4d2d-8793-0b725036904f.png">

Requisitos

- Tener una cuenta en AWS - https://gist.github.com/luisgradossalinas/c233c0333022c6617dd70609bfdf6441

## Creando Skill en Alexa.

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

Creamos un nuevo stack en CloudFormation, a partir del archivo chatgpt.yaml.

Actualizar el código de la lambda con el archivo zip code/alexa02mar.zip.

Lo subimos al bucket de S3, y le indicamos la url.

<img width="942" src="https://user-images.githubusercontent.com/2066453/222504942-753615b9-88d9-487f-992f-86b89561b609.png">

Le asociado un desencadenador que será Alexa Skills, le indicamos el Skill ID de nueva skill.

<img width="794" src="https://user-images.githubusercontent.com/2066453/222495499-7192c53b-b802-426c-a8af-10e9c356d835.png">

Regresamos a la consola de Alexa.

Clic en Endpoint.

Copiamos el valor de Your skill ID, y lo asociamos a nuestra función Lambda.
En default region indicamos el ARN de nuestra Lambda.

Clic en Save Endpoints.

![Captura de Pantalla 2023-02-24 a la(s) 18 03 31](https://user-images.githubusercontent.com/2066453/221317285-e0e2773d-3824-4b66-808d-74e97e213d27.png)

