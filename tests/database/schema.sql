create database if not exists encoder;

use encoder;

drop table if exists `todo_list`;
create table `todo_list` (
  `id` int(11) not null auto_increment,
  `title` varchar(255) not null,
  `is_done` tinyint(4) not null default 0,
  `created_at` timestamp not null default current_timestamp,
  primary key (`id`),
  key `is_done` (`is_done`),
  key `created_at` (`created_at`)
) engine=innodb default charset=utf8;