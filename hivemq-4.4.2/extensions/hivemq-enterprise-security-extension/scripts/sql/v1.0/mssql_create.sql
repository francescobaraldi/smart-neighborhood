create FULLTEXT CATALOG full_text_catalogue AS DEFAULT;

create table users
(
    id                  integer      not null identity
        constraint users_pkey
            primary key,
    username            varchar(max) not null,
    password            varchar(max),
    password_iterations integer      not null,
    password_salt       varchar(max) not null,
    algorithm           varchar(max) not null
);

create unique index users_id_uindex
    on users (id);

create FULLTEXT INDEX on users (username)
    KEY INDEX users_id_uindex
    with STOPLIST = SYSTEM;

create table roles
(
    id          integer      not null identity
        constraint roles_pkey
            primary key,
    name        varchar(max) not null,
    description varchar(max)
);

create unique index roles_id_uindex
    on roles (id);

create FULLTEXT INDEX on roles (name)
    KEY INDEX roles_id_uindex
    with STOPLIST = SYSTEM;


create table user_roles
(
    user_id integer not null
        constraint user_roles_users_id_fk
            references users,
    role_id integer not null
        constraint user_roles_roles_id_fk
            references roles,
    constraint user_roles_user_role_pk
        primary key (user_id, role_id)
);

create table permissions
(
    id                    integer       not null identity
        constraint permissions_pkey
            primary key,
    topic                 varchar(max)  not null,
    publish_allowed       bit default 0 not null,
    subscribe_allowed     bit default 0 not null,
    qos_0_allowed         bit default 0 not null,
    qos_1_allowed         bit default 0 not null,
    qos_2_allowed         bit default 0 not null,
    retained_msgs_allowed bit default 0 not null,
    shared_sub_allowed    bit default 0 not null,
    shared_group          varchar(max)
);

create table role_permissions
(
    role       integer not null
        constraint role_permissions_roles_id_fk
            references roles,
    permission integer not null
        constraint role_permissions_permissions_id_fk
            references permissions,
    constraint role_permissions_role_permission_pk
        primary key (role, permission)
);

create table user_permissions
(
    user_id    integer not null
        constraint user_permissions_users_id_fk
            references users,
    permission integer not null
        constraint user_permissions_permissions_id_fk
            references permissions,
    constraint user_permissions_user_permission_pk
        primary key (user_id, permission)
);
