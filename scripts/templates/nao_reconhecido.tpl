{% args req %}
{% args req %}
<html lang="pt">
	<head>
		<style rel="stylesheet" type="text/css">
			.form-contact{
				width: 100%;
			}
			.button {
				background-color: #5e2075;
				border: none;
				color: white;
				padding:0 10px;
				text-align: center;
				text-decoration: none;
				display: inline-block;
				font-family:Century Gothic;
				font-size: 23px;
				margin: 10px 20px;
				cursor: pointer;
				border-radius: 5px;
				width:220px;
				height:41.83px;
			}
			.entrada {
				background-color: #5e2075;
				color: white;
				border:none;
				border-radius: 8px;
				padding:0 10px;
				margin: 8px 2px;
				font-size: 35px;
				font-family:Century Gothic;
				width:560.59px;
				height:43.82px;
			}
			.bloco {
				padding: 0 0;
			    margin-top: 3.6em;
				margin-bottom: 3.6em;
				margin-right: 3.6em;
				margin-left: 3.6em;
				}
			::placeholder {
				color: white;
				opacity: 0.85;
			}	
		</style>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<title>ESP</title>	
	</head>
	<body class="text-center" style="background-color: #eaeaea;">
		<div>
			<form class="bloco" align="center">
				<h1 style="color: #5e2075;font-size: 60px;font-weight:289; text-shadow: rgb(0,0,0,0.7) 1px 3px 6px" ><font face="Century Gothic">E-POINT</h1>	
				<div>
					<input class="entrada" type="text" id="ID" placeholder="ID:" required autofocus>
				</div>
				<div>
					<input class="entrada" type="number" id="matricula" placeholder="MATRÍCULA:" required autofocus>
				</div>
				<div>
					<p style="color: white; font-size: 40px; text-shadow: rgb(0,0,0,0.3) 0px 3px 6px; white-space:pre"><font face="Century Gothic">
CARTÃO
NÃO
RECONHECIDO
					</p>
				</div>
			</form>
			<form action="/" class="form_contact" method="post" tabindex="1" align=>
				<button type="submit" class="button">VOLTAR</button>
			</form>
		</div>
	</body>
</html>

