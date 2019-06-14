{% args req %}
<html lang="pt">
	<head>
		<title>ESP</title>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<meta name="description" content="">
		<meta name="author" content="">
		<style rel="stylesheet" type="text/css">
			body {
				background-color: #eaeaea;
			}
			.form-contact{
				width: 100%;

			}
			h1 {
				display: block;
				margin: 5%;
				font-size: 60px;
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
				margin-top: 10%;
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
				margin: 8px 0;
				font-size: 20px;
				font-family:Verdana;
				width: 400px;
				height: auto;
			}
			::placeholder {
				color: white;
				opacity: 0.80;
			}
		</style>
	</head>
	<body class="text-center">
		<div class="container">
			<form action="/aproxime_cartao" method="POST" tabindex="1" align="center">
				<div>	
					<h1 style="color: #5e2075;font-weight:289; text-shadow: rgb(0,0,0,0.7) 1px 3px 6px" ><font face="Verdana">E-POINT</h1>
					<div>
						<input name='matricula' class="entrada" type="number" id="matricula" placeholder="MATRÍCULA:" required >
					</div>
					<div>
						<p style="color: white; font-size: 40px; text-shadow: rgb(0,0,0,0.3) 0px 3px 6px;">
							<font face="Verdana">
								DIGITE
								SUA 
								MATRÍCULA!
							</font>
						</p>
					</div>
					<div>
						<button type="submit" class="button">ENVIAR</button>
					</div>
				</div>
			</form>
		</div>
	</body>
</html>