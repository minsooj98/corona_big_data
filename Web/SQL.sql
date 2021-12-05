drop table members;
create table members(userid varchar(20) primary key,
					passwd varchar(20), 
					username varchar(20),
					birth varchar(20) NULL,
					gender varchar(10) NULL
					);

create table graph(				 
				image varchar(50) primary key,
				userid VARCHAR(20) NOT NULL
				   );
