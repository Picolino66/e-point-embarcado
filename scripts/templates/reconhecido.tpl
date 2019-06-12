{% args req %}
<html lang="pt">
	<head>
		<style rel="stylesheet" type="text/css">
			.button {
				background-color: #5e2075;
				border: none;
				color: white;
				padding: 0 10px;
				text-align: center;
				text-decoration: none;
				display: inline-block;
				font-size: 16px;
				margin: 4px 2px;
				cursor: pointer;
				border-radius: 5px;
			}
			.entrada {
				background-color: #5e2075;
				color: white;
				border:none;
				border-radius: 5px;
				padding: 0 3px;
				margin: 5px;
				font-size: 16px;
			}
			.bloco {
				padding: 50% 0;
				}
			::placeholder {
				color: white;
				opacity: 0.85;
			}	
		</style>
		<title>ESP</title>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<meta name="description" content="">
		<meta name="author" content="">
	</head>
	<body class="text-center" style="background-color: #eaeaea">
		<div>
			<form class="bloco" align="center">
				<h1 style="color: #5e2075" ><font face="arial">E-POINT</h1>	
				<div>
					<input class="entrada" type="number" id="ID" placeholder="ID:" required autofocus>
				</div>		
				<div>	
					<input class="entrada  type="number" id="matricula" placeholder="MATRÍCULA:" required>
				</div>
				<div>
					<p style="color: white; padding:5%"><font face="arial">RECONHECIDO</p>
				</div>
				<div>
					<button type="btn" class="button">Cadastrar</button>
					<button type="submit" class="button">Enviar</button>			
				</div>
			</form>
		</div>
	</body>
</html>