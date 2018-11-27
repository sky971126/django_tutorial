# MySQL 8.x Statement Syntax Examples

## Data definition statements

```mysql
CREATE DATABASE IF NOT EXISTS cgh_shipping;
```

```mysql
DROP DATABASE IF EXISTS cgh_shipping;
```

## Data manipulation statements



## Database administration statements


### User account management

```mysql
CREATE USER 'arwhyte'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MyPassword';
GRANT ALL PRIVILEGES ON *.* TO 'arwhyte'@'localhost' WITH GRANT OPTION;

CREATE USER 'arwhyte'@'%' IDENTIFIED WITH mysql_native_password BY 'MyPassword';
GRANT ALL PRIVILEGES ON *.* TO 'arwhyte'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;
```

TODO add ALTER statement.


```mysql
DROP USER IF EXISTS 'arwhyte'@'localhost', 'arwhyte'@'%';
```