CREATE DATABASE IF NOT EXISTS `rhok_desahucios` ;
CREATE USER 'rhok'@'localhost' IDENTIFIED BY 'rhok';
GRANT ALL PRIVILEGES ON `rhok_desahucios`.* TO `rhok`@`localhost`;
