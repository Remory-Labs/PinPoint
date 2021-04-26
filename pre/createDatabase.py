import sys
import mysql.connector

# Setting up database
try:
  db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root",
      auth_plugin='mysql_native_password'
  )
except:
  print("Database is not responding, is it running?")
  input("Press Enter to exit setup...")
  sys.exit()
  

handler = db.cursor()

handler.execute("DROP DATABASE IF EXISTS `pinpoint`;")
handler.execute("CREATE DATABASE IF NOT EXISTS `pinpoint` DEFAULT CHARACTER SET utf8;")

handler.close()
db.disconnect()

# Using newly created database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pinpoint"
)

handler = db.cursor()

handler.execute("DROP TABLE IF EXISTS `position`;")
qr = """CREATE TABLE IF NOT EXISTS `position` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pos` VARCHAR(50) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
"""
handler.execute(qr)

handler.execute("DROP TABLE IF EXISTS `recognitions`;")
qr = """ CREATE TABLE IF NOT EXISTS `recognitions` (
  `recID` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`recID`))
ENGINE = InnoDB;
"""
handler.execute(qr)

handler.execute("DROP TABLE IF EXISTS `errors`;")
qr = """CREATE TABLE IF NOT EXISTS `errors` (
  `errorId` INT NOT NULL,
  `error_type` ENUM('OK', 'Minor', 'Major', 'Fatal', 'Crash') NOT NULL,
  PRIMARY KEY (`errorId`),
  INDEX `FK_recID` (`errorId` ASC),
  CONSTRAINT `FK_recID`
    FOREIGN KEY (`errorId`)
    REFERENCES `recognitions` (`recID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
"""
handler.execute(qr)

handler.close()
db.disconnect()

print("Database created successfully.")
input("Press Enter to exit setup...")
