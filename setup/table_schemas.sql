-- tables required

CREATE TABLE user (
    `user_id` VARCHAR(8) NOT NULL,
    `name` VARCHAR(256) DEFAULT NULL,
    `modified` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`user_id`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE product (
    `product_id` VARCHAR(16) NOT NULL,
    `title` VARCHAR(256) NOT NULL,
    `price` decimal(8,2) unsigned NOT NULL,
    `quantity` smallint unsigned NOT NULL,
    `modified` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`product_id`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE cart (
    `id` INT(20) NOT NULL AUTO_INCREMENT,
    `user_id` VARCHAR(8) NOT NULL,
    `product_id` VARCHAR(16) NOT NULL,
    `quantity` smallint unsigned NOT NULL DEFAULT '1',
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`),
    KEY user (`user_id`),
    CONSTRAINT fk_user_id
        FOREIGN KEY (`user_id`)
        REFERENCES user(`user_id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `order` (
    `order_id` VARCHAR(16) NOT NULL,
    `user_id` VARCHAR(8) NOT NULL,
    `total` decimal(8,2) unsigned NOT NULL,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE order_item(
    `id` INT NOT NULL AUTO_INCREMENT,
    `order_id` VARCHAR(16) NOT NULL,
    `product_id` VARCHAR(16) NOT NULL,
    `quantity` smallint unsigned NOT NULL DEFAULT '1',
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`),
    KEY user (`order_id`),
    CONSTRAINT fk_order_id
        FOREIGN KEY (`order_id`)
        REFERENCES `order`(`order_id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;