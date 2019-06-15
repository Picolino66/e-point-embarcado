{% args req %}
<html lang="pt">
	<head>
		<style rel="stylesheet" type="text/css">
			body {
				background-color: #eaeaea;
			}
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
				font-family:Verdana;
				font-size: 23px;
				margin-top: 1%;
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
				margin: 8px 0px;
				font-size: 20px;
				font-family:Verdana;
				width:400px;
				height: auto;
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
	<body>
		<div class="container">
			<form action="/server_off" method="POST" align="center">
				<h1 style="color: #5e2075;font-size: 60px;font-weight:289; text-shadow: rgb(0,0,0,0.7) 1px 3px 6px; margin-bottom:7%" ><font face="Verdana">E-POINT</h1>				
				<div>
					<p style="color: white; font-size: 40px; text-shadow: rgb(0,0,0,0.3) 0px 3px 6px; white-space:pre;"><font face="Verdana">
CADASTRADO
COM
SUCESSO!
					</p>
				</div>
				<div>
					<button type="submit" class="button">SAIR</button>
				</div>
			</form>
		</div>
	</body>
</html>
