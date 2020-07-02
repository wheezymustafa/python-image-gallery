create table if not exists users(username varchar(50) primary key, password varchar(50), fullname varchar(50));
create table if not exists userimages(username varchar(50) references users(username), imageid varchar(50), primary key(username, imageid));
create user image_gallery with password '1mage_ga113ry!';
grant all on all tables in schema public to image_gallery;
insert into users (username, password, fullname) values ('dam0045', '111', 'daniel mustafa'), ('dongji', 'cpsc4973', 'dongji the GTA');
