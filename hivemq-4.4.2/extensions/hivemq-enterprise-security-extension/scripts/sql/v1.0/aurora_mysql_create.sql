create table users
(
    id                  integer not null auto_increment unique,
    username            text    not null,
    password            text comment 'Base64 encoded raw byte array',
    password_iterations integer not null,
    password_salt       text    not null comment 'Base64 encoded raw byte array',
    algorithm           text    not null,
    constraint users_pkey primary key (id)
)
;

create unique index users_id_uindex
    on users (id)
;

create table roles
(
    id          integer not null auto_increment unique,
    name        text    not null,
    description text,
    constraint roles_pkey primary key (id)
)
;

create unique index roles_id_uindex
    on roles (id)
;

create table user_roles
(
    user_id integer not null,
    role_id integer not null,
    constraint user_roles_user_role_pk primary key (user_id, role_id),
    constraint user_roles_users_id_fk foreign key (user_id) references users (id),
    constraint user_roles_roles_id_fk foreign key (role_id) references roles (id)
)
;

create table permissions
(
    id                    integer               not null auto_increment unique,
    topic                 text                  not null,
    publish_allowed       boolean default false not null,
    subscribe_allowed     boolean default false not null,
    qos_0_allowed         boolean default false not null,
    qos_1_allowed         boolean default false not null,
    qos_2_allowed         boolean default false not null,
    retained_msgs_allowed boolean default false not null,
    shared_sub_allowed    boolean default false not null,
    shared_group          text,
    constraint permissions_pkey primary key (id)
)
    comment ='All permissions are whitelist permissions'
;

create index permissions_topic_index
    on permissions (topic(767)) # 3072 bytes / 4 = 768 chars, 767 is max for MySQL 5.6
;

create table role_permissions
(
    role       integer not null,
    permission integer not null,
    constraint role_permissions_role_permission_pk primary key (role, permission),
    constraint role_permissions_roles_id_fk foreign key (role) references roles (id),
    constraint role_permissions_permissions_id_fk foreign key (permission) references permissions (id)
)
;

create table user_permissions
(
    user_id    integer not null,
    permission integer not null,
    constraint user_permissions_user_permission_pk primary key (user_id, permission),
    constraint user_permissions_users_id_fk foreign key (user_id) references users (id),
    constraint user_permissions_permissions_id_fk foreign key (permission) references permissions (id)
)
;
