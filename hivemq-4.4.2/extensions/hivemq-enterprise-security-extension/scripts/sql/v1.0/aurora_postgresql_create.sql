create table users
(
    id                  serial  not null
        constraint users_pkey
            primary key,
    username            text    not null
        constraint users_username_unique unique,
    password            text,
    password_iterations integer not null,
    password_salt       text    not null,
    algorithm           text    not null
)
;

create unique index users_id_uindex
    on users (id)
;

create unique index users_username_uindex
    on users (username)
;

comment on column users.password is 'Base64 encoded raw byte array'
;

comment on column users.password_salt is 'Base64 encoded raw byte array'
;

create table roles
(
    id          serial not null
        constraint roles_pkey
            primary key,
    name        text   not null
        constraint roles_name_unique unique,
    description text
)
;

create unique index roles_id_uindex
    on roles (id)
;

create unique index roles_name_uindex
    on roles (name)
;

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
)
;

create table permissions
(
    id                    serial                not null
        constraint permissions_pkey
            primary key,
    topic                 text                  not null,
    publish_allowed       boolean default false not null,
    subscribe_allowed     boolean default false not null,
    qos_0_allowed         boolean default false not null,
    qos_1_allowed         boolean default false not null,
    qos_2_allowed         boolean default false not null,
    retained_msgs_allowed boolean default false not null,
    shared_sub_allowed    boolean default false not null,
    shared_group          text
)
;

create index permissions_topic_index
    on permissions (topic)
;

comment on table permissions is 'All permissions are whitelist permissions'
;

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
)
;

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
)
;
