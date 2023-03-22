CREATE TABLE `Marca` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Marca` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=latin1;

CREATE TABLE `Modelo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Modelo` varchar(30) DEFAULT NULL,
  `Marca_P` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Marca_P` (`Marca_P`),
  CONSTRAINT `modelo_ibfk_1` FOREIGN KEY (`Marca_P`) REFERENCES `Marca` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1395 DEFAULT CHARSET=latin1;

CREATE TABLE `Carro` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `Ano` varchar(30) DEFAULT NULL,
  `Version` varchar(30) DEFAULT NULL,
  `Kilometros` varchar(30) DEFAULT NULL,
  `Transmision` varchar(30) DEFAULT NULL,
  `Departamento` varchar(30) DEFAULT NULL,
  `Color` varchar(30) DEFAULT NULL,
  `Combustible` varchar(30) DEFAULT NULL,
  `Puertas` varchar(30) DEFAULT NULL,
  `Motor` varchar(30) DEFAULT NULL,
  `Carroceria` varchar(30) DEFAULT NULL,
  `Precio` varchar(30) DEFAULT NULL,
  `Dias_Publicado` varchar(30) DEFAULT NULL,
  `URL` varchar(100) DEFAULT NULL,
  `Modelo_p` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Modelo_p` (`Modelo_p`),
  CONSTRAINT `carro_ibfk_1` FOREIGN KEY (`Modelo_p`) REFERENCES `Modelo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14593 DEFAULT CHARSET=latin1;