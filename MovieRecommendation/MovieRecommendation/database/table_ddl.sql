create schema `6889proj` collate utf8_general_ci;

create table model_res
(
    date date not null
        primary key,
    pos  int  not null,
    neg  int  not null,
    constraint model_res_date_uindex
        unique (date)
);