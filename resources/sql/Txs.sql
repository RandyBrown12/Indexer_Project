---------------------------------------------------------------------------
---  Project Name: Txs.sql                                                -
---                                                                       -
---  Language: sql                                                        -
---                                                                       -
---                                                                       -
--- Version: 1.0                                                          -
---                                                                       -
---                                                                       -
--- Version: 1.1                                                          -
--- New indexes have been added, such as indexes for all tx_id in msg     -                                                                       
---                                                                       -
--- Version: 1.2                                                          -
--- For transaction table and all message table, new column 'comment'     -
--- has been added.
--- For each table of message, the UNIQUE column has been changed.        -
---                                                                       -
--- Version: 1.3                                                          -
--- There are two more message tables added, 'multisend' and 'vote'.      -
--- The 'address' table has been updated. The unique column has been      -
--- limited to 'addresses' itself.                                        -
---
--- Version: 1.4 
--- New type 'cosmos_vote_beta1_msg' has been added. The only difference  -
--- between this type and 'cosmos_vote_msg' is that this table does not   -
--- have 'metadata' column.
--- Also, new type 'cosmos_unjail_msg' has been added.                    -
--- 
--- Version 1.5 
--- New types 'ibc_core_channel_v1_msgchannelopenack' and
--- 'ibc_core_channel_v1_msgchannelopeninit' have been added.             -
--- Commission_rate is set to accept null values
---
--- Version 1.6
--- New table message_table_lookup has been created to perform a join
--- between the message tables and the transaction table. An index
--- has also been created using the tx_id and message_id columns.
--- 
--- Version 1.7
--- Table cosmos_multisend_outputs has removed UNIQUE constraint and also
--- removed inputs_denom and inputs_amount. Table cosmos_multisend_msg has
--- removed UNIQUE constraint for now.
--- 
--- Version 1.8
--- Table cosmos_setwithdrawaddress_msg has been added with delegation_address_id
--- and withdraw_address_id for the columns.
---
--- Version 1.9
--- Table blocks has been changed to have tx_num and height as NUMERIC
---------------------------------------------------------------------------
SET client_min_messages TO WARNING;

create extension if not exists "pgcrypto";

-- Block table 
-- TX_NUM should be NUMERIC
create table if not exists blocks
(
    block_id        uuid default gen_random_uuid() not null
        primary key,    
    block_hash      VARCHAR                   not null,   
    chain_id        VARCHAR                   not null,
    height          NUMERIC                   not null,
    tx_num          NUMERIC                  not null,
    created_at      timestamp with time zone                     not null,
    UNIQUE (chain_id, height)
);



create index if not exists blocks_block_hash
    on blocks (block_hash);

create index if not exists blocks_chain_id_height
    on blocks (chain_id,height);

create unique index if not exists blocks_chain_id_hash_height
    on blocks (chain_id, block_hash, height);



-- Transactions table

create table if not exists transactions
(
    tx_id         uuid default gen_random_uuid() not null
        primary key,
    block_id      uuid                          not null,
    tx_hash         VARCHAR                     not null,
    chain_id        VARCHAR                     not null,
    height          VARCHAR                     not null,    
    memo            VARCHAR                     not null,   
    fee_denom       VARCHAR                     not null,
    fee_amount      VARCHAR                     not null,
    gas_limit       VARCHAR                     not null,
    created_at timestamp with time zone         not null,
    tx_info    jsonb                            not null,
    comment         VARCHAR                     not null,
    FOREIGN KEY (block_id) REFERENCES blocks(block_id),
    UNIQUE(tx_hash, chain_id, height)
);


create index if not exists transactions_tx_hash
    on transactions (tx_hash);

create index if not exists transactions_chain_id_height
    on transactions (chain_id, height);

create unique index if not exists transactions_chain_id_hash_height
    on transactions (chain_id, tx_hash, height);



-- address table for all types of addresses

create table if not exists address 
(
    address_id         uuid default gen_random_uuid() not null
        primary key,   
    address_type    VARCHAR       not null,
    addresses       VARCHAR       not null,
    comment         VARCHAR       not null,
    created_at      timestamp with time zone     not null,
    updated_at      timestamp with time zone     not null,
    UNIQUE (addresses)
);


create index if not exists address_addresses
    on address (addresses);

create index if not exists address_address_type
    on address (address_type);

create unique index if not exists address_address_addresses_type
    on address (addresses, address_type);



-- type table 

create table if not exists type
(   
   id           uuid default gen_random_uuid() not null
        primary key,
   type         VARCHAR       not null,
   height       VARCHAR       not null,
   UNIQUE (type, height)
);



-- alliance_alliance_MsgClaimDelegationRewards table

create table if not exists alliance_claimdelegationrewards_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    delegator_address_id            uuid             not null,
    validator_address_id            uuid             not null,
    tx_type                         VARCHAR          not null,   
    tx_denom                        VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (delegator_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);

create index if not exists alli_delegationrewards_tx_id
    on alliance_claimdelegationrewards_msg (tx_id);

create index if not exists alli_delegationrewards_delegator_address_id
    on alliance_claimdelegationrewards_msg (delegator_address_id);

create index if not exists alli_delegationrewards_validator_address_id
    on alliance_claimdelegationrewards_msg (validator_address_id);



-- cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission

create table if not exists cosmos_withdrawvalidatorcommission_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    validator_address_id          uuid             not null,
    tx_type                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (validator_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_withdrawvalidatorcommission_validator_address_id
    on cosmos_withdrawvalidatorcommission_msg (validator_address_id);

create index if not exists cosmos_withdrawvalidatorcommission_tx_id
    on cosmos_withdrawvalidatorcommission_msg (tx_id);

-- alliance_alliance_MsgClaimDelegate table

create table if not exists alliance_delegate_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    delegator_address_id          uuid             not null,
    validator_address_id          uuid             not null, 
    tx_type             VARCHAR          not null,   
    tx_denom            VARCHAR          not null,
    amount              VARCHAR         not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (delegator_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists alli_delegate_delegator_address_id
    on alliance_delegate_msg (delegator_address_id);

create index if not exists alli_delegate_validator_address_id
    on alliance_delegate_msg (validator_address_id);

create index if not exists alli_delegate_tx_id
    on alliance_delegate_msg (tx_id);

-- alliance_alliance_MsgRedelegate table

create table if not exists alliance_redelegate_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    delegator_address_id              uuid             not null,
    validator_src_address_id          uuid             not null,
    validator_dst_address_id          uuid             not null,    
    tx_type             VARCHAR          not null,
    tx_denom            VARCHAR          not null,
    amount              VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (delegator_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_src_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_dst_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists alli_redelegate_delegator_address_id
    on alliance_redelegate_msg (delegator_address_id);

create index if not exists alli_redelegate_validator_src_address_id
    on alliance_redelegate_msg (validator_src_address_id);

create index if not exists alli_redelegate_validator_dst_address_id
    on alliance_redelegate_msg (validator_dst_address_id);

create index if not exists alli_redelegate_tx_id
    on alliance_redelegate_msg (tx_id);

-- alliance_alliance_MsgUndelegate table

create table if not exists alliance_undelegate_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    delegator_address_id          uuid             not null,
    validator_address_id          uuid             not null, 
    tx_type             VARCHAR          not null,   
    tx_denom            VARCHAR          not null,
    amount              VARCHAR         not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (delegator_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists alli_undelegate_delegator_address_id
    on alliance_undelegate_msg (delegator_address_id);

create index if not exists alli_undelegate_validator_address_id
    on alliance_undelegate_msg (validator_address_id);

create index if not exists alli_undelegate_tx_id
    on alliance_undelegate_msg (tx_id);

-- cosmos_authz_v1beta1_MsgExec table

create table if not exists cosmos_exec_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    receive_address_id          uuid             not null,
    tx_type             VARCHAR          not null,    
    msg_num             VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (receive_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)

);


create index if not exists cosmos_exec_receive_address_id
    on cosmos_exec_msg (receive_address_id);

create index if not exists cosmos_exec_tx_id
    on cosmos_exec_msg (tx_id);

-- cosmos_authz_v1beta1_MsgGrant table 

create table if not exists cosmos_grant_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    send_address_id          uuid             not null,
    receive_address_id          uuid             not null,
    tx_type             VARCHAR          not null,
    authorizationtype   VARCHAR          not null,
    max_tokens          VARCHAR          not null,
    authorization_type   VARCHAR         not null,
    msg                   VARCHAR        not null,
    expiration            VARCHAR        not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (send_address_id) REFERENCES address(address_id),
    FOREIGN KEY (receive_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_grant_receive_address_id
    on cosmos_grant_msg (receive_address_id);

create index if not exists cosmos_grant_send_address_id
    on cosmos_grant_msg (send_address_id);

create index if not exists cosmos_grant_tx_id
    on cosmos_grant_msg (tx_id);

create table if not exists cosmos_grant_allowlist
(
    address_id      uuid default gen_random_uuid() not null
        primary key,
    message_id      uuid                    not null   UNIQUE,
    addresses       VARCHAR                 not null,
    FOREIGN KEY (message_id) REFERENCES cosmos_grant_msg(message_id)
    
);

create index if not exists cosmos_grant_allowlist_addresses
    on cosmos_grant_allowlist (addresses);

create index if not exists cosmos_grant_allowlist_message_id
    on cosmos_grant_allowlist (message_id);

-- cosmos_authz_v1beta1_MsgRevoke table 

create table if not exists cosmos_revoke_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    send_address_id     uuid             not null,
    receive_address_id  uuid             not null,
    tx_type             VARCHAR          not null,
    msg_type_url        VARCHAR         not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (send_address_id) REFERENCES address(address_id),
    FOREIGN KEY (receive_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_revoke_send_address_id
    on cosmos_revoke_msg (send_address_id);

create index if not exists cosmos_revoke_receive_address_id
    on cosmos_revoke_msg (receive_address_id);

create index if not exists cosmos_revoke_tx_id
    on cosmos_revoke_msg (tx_id);

-- cosmos_bank_v1beta1_MsgSend table

create table if not exists cosmos_send_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    from_address_id          uuid             not null,
    to_address_id          uuid             not null,    
    tx_type             VARCHAR          not null,
    tx_denom            VARCHAR          not null,
    amount              VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (from_address_id) REFERENCES address(address_id),
    FOREIGN KEY (to_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_send_from_address_id
    on cosmos_send_msg (from_address_id);

create index if not exists cosmos_send_to_address_id
    on cosmos_send_msg (to_address_id);

create index if not exists cosmos_send_tx_id
    on cosmos_send_msg (tx_id);

-- cosmos_distribution_v1beta1_MsgWithdrawDelegatorReward table

create table if not exists cosmos_withdrawdelegatorreward_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    delegator_address_id          uuid             not null,
    validator_address_id          uuid             not null,    
    tx_type             VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (delegator_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_withdrawdelegatorreward_delegator_address_id
    on cosmos_withdrawdelegatorreward_msg (delegator_address_id);

create index if not exists cosmos_withdrawdelegatorreward_validator_address_id
    on cosmos_withdrawdelegatorreward_msg (validator_address_id);

create index if not exists cosmos_withdrawdelegatorreward_tx_id
    on cosmos_withdrawdelegatorreward_msg (tx_id);

-- cosmos_staking_v1beta1_MsgBeginRedelegate table

create table if not exists cosmos_beginredelegate_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    delegator_address_id              uuid             not null,
    validator_src_address_id          uuid             not null,
    validator_dst_address_id          uuid             not null,    
    tx_type             VARCHAR          not null,
    tx_denom            VARCHAR          not null,
    amount              VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (delegator_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_src_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_dst_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_beginredelegate_delegator_address_id
    on cosmos_beginredelegate_msg (delegator_address_id);

create index if not exists cosmos_beginredelegate_validator_src_address_id
    on cosmos_beginredelegate_msg (validator_src_address_id);

create index if not exists cosmos_beginredelegate_validator_dst_address_id
    on cosmos_beginredelegate_msg (validator_dst_address_id);

create index if not exists cosmos_beginredelegate_tx_id
    on cosmos_beginredelegate_msg (tx_id);

-- cosmos_staking_v1beta1_MsgDelegate table

create table if not exists cosmos_delegate_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    delegator_address_id          uuid             not null,
    validator_address_id          uuid             not null, 
    tx_type             VARCHAR          not null,   
    tx_denom            VARCHAR          not null,
    amount              VARCHAR         not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (delegator_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_delegate_delegator_address_id
    on cosmos_delegate_msg (delegator_address_id);

create index if not exists cosmos_delegate_validator_address_id
    on cosmos_delegate_msg (validator_address_id);

create index if not exists cosmos_delegate_tx_id
    on cosmos_delegate_msg (tx_id);

-- cosmos_staking_v1beta1_MsgUndelegate table

create table if not exists cosmos_undelegate_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    delegator_address_id          uuid             not null,
    validator_address_id          uuid             not null, 
    tx_type             VARCHAR          not null,   
    tx_denom            VARCHAR          not null,
    amount              VARCHAR         not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (delegator_address_id) REFERENCES address(address_id),
    FOREIGN KEY (validator_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_undelegate_delegator_address_id
    on cosmos_undelegate_msg (delegator_address_id);

create index if not exists cosmos_undelegate_validator_address_id
    on cosmos_undelegate_msg (validator_address_id);

create index if not exists cosmos_undelegate_tx_id
    on cosmos_undelegate_msg (tx_id);

-- cosmwasm_wasm_v1_MsgExecuteContract table   contracts to another table 

create table if not exists cosmwasm_executecontract_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    send_address_id          uuid             not null,    
    tx_type             VARCHAR          not null,
    contracts           VARCHAR         not null,
    msg                 VARCHAR          not null,
    tx_denom            VARCHAR        not null,
    amount              VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (send_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmwasm_executecontract_send_address_id
    on cosmwasm_executecontract_msg (send_address_id);

create index if not exists cosmwasm_executecontract_tx_id
    on cosmwasm_executecontract_msg (tx_id);

create index if not exists cosmwasm_executecontract_msg_contracts
    on cosmwasm_executecontract_msg (contracts);


-- cosmwasm_wasm_v1_MsgInstantiateContract table

create table if not exists cosmwasm_instantiatecontract_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    send_address_id          uuid             not null,
    admin_address_id    uuid             not null, 
    tx_type             VARCHAR          not null,
    code_id             VARCHAR          not null,
    label               VARCHAR          not null,
    msg                 VARCHAR[]           not null,
    funds               JSONB            not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (send_address_id) REFERENCES address(address_id),
    FOREIGN KEY (admin_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)

);


create index if not exists cosmwasm_instantiatecontract_send_address_id
    on cosmwasm_instantiatecontract_msg (send_address_id);

create index if not exists cosmwasm_instantiatecontract_admin_address_id
    on cosmwasm_instantiatecontract_msg (admin_address_id);

create index if not exists cosmwasm_instantiatecontract_tx_id
    on cosmwasm_instantiatecontract_msg (tx_id);

-- cosmwasm_wasm_v1_MsgStoreCode table

create table if not exists cosmwasm_storecode_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    sender_address_id          uuid             not null,    
    tx_type             VARCHAR          not null,
    wasm_byte_code          VARCHAR          not null,
    instantiate_permission  VARCHAR         not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (sender_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmwasm_storecode_sender_address_id
    on cosmwasm_storecode_msg (sender_address_id);

create index if not exists cosmwasm_storecode_tx_id
    on cosmwasm_storecode_msg (tx_id);

-- ibc_applications_transfer_v1_MsgTransfer table

create table if not exists ibc_transfer_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    sender_address_id                       uuid             not null,
    receiver_address_id                     uuid             not null,    
    tx_type                                 VARCHAR          not null,
    source_port                             VARCHAR          not null,
    source_channel                          VARCHAR          not null,
    token_denom                             VARCHAR          not null,
    token_amount                            VARCHAR          not null,
    timeout_height_revision_num             VARCHAR          not null,
    timeout_height_revision_height          VARCHAR          not null,
    timeout_timestamp                       VARCHAR          not null,
    memo                                    VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (sender_address_id) REFERENCES address(address_id),
    FOREIGN KEY (receiver_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists ibc_transfer_sender_address_id
    on ibc_transfer_msg (sender_address_id);

create index if not exists ibc_transfer_receiver_address_id
    on ibc_transfer_msg (receiver_address_id);

create index if not exists ibc_transfer_tx_id
    on ibc_transfer_msg (tx_id);

-- ibc_core_client_v1_MsgUpdateClient table

create table if not exists ibc_updateclient_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    client_id                       VARCHAR          not null,
    client_message                  jsonb              not null,
    signer_id                       VARCHAR          not null,
    signer                          VARCHAR          ,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);


create index if not exists ibc_updateclient_client_id
    on ibc_updateclient_msg (client_id);

create index if not exists ibc_updateclient_tx_id
    on ibc_updateclient_msg (tx_id);

-- ibc.core.channel.v1.MsgTimeout table 

create table if not exists ibc_timeout_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    sequence_num                    VARCHAR          not null,
    source_port                     VARCHAR          not null,
    source_channel                  VARCHAR          not null,
    destination_port                VARCHAR          not null,
    destination_channel             VARCHAR          not null,
    data_msg                        VARCHAR          not null,
    timeout_height_revision_number  VARCHAR          not null,
    timeout_height_revision_height  VARCHAR          not null,
    timeout_timestamp               VARCHAR          not null,
    proof_unreceived                VARCHAR          not null,
    proof_height_revision_number    VARCHAR          not null,
    proof_height_revision_height    VARCHAR          not null,
    next_seq_recv                   VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);

create index if not exists ibc_timeout_tx_id
    on ibc_timeout_msg (tx_id);

-- ibc_core_channel_v1_MsgRecvPacket table

create table if not exists ibc_recvpacket_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    sequence_num                    VARCHAR          not null,
    source_port                     VARCHAR          not null,
    source_channel                  VARCHAR          not null,
    destination_port                VARCHAR          not null,
    destination_channel             VARCHAR          not null,
    data_msg                        VARCHAR          not null,
    timeout_height_revision_number  VARCHAR          not null,
    timeout_height_revision_height  VARCHAR          not null,
    timeout_timestamp               VARCHAR          not null,
    proof_commitment                VARCHAR          not null,
    proof_height_revision_number    VARCHAR          not null,
    proof_height_revision_height    VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);

create index if not exists ibc_recvpacket_tx_id
    on ibc_recvpacket_msg (tx_id);

-- ibc_core_channel_v1_MsgAcknowledgement table

create table if not exists ibc_acknowledgement_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    sequence_num                    VARCHAR          not null,
    source_port                     VARCHAR          not null,
    source_channel                  VARCHAR          not null,
    destination_port                VARCHAR          not null,
    destination_channel             VARCHAR          not null,
    data_msg                        VARCHAR          not null,
    timeout_height_revision_number  VARCHAR          not null,
    timeout_height_revision_height  VARCHAR          not null,
    timeout_timestamp               VARCHAR          not null,
    acknowledgement                 VARCHAR          not null,
    proof_acked                     VARCHAR          not null,
    proof_height_revision_number    VARCHAR          not null,
    proof_height_revision_height    VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);

create index if not exists ibc_acknowledgement_tx_id
    on ibc_acknowledgement_msg (tx_id);

-- ibc.core.channel.v1.MsgChannelOpenConfirm table

create table if not exists ibc_channelopenconfirm_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    port_id                         VARCHAR          not null,
    channel_id                      VARCHAR          not null,
    proof_acked                     VARCHAR          not null,
    proof_height_revision_number    VARCHAR          not null,
    proof_height_revision_height    VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);

create index if not exists ibc_channelopenconfirm_tx_id
    on ibc_channelopenconfirm_msg (tx_id);

-- ibc.core.channel.v1.MsgChannelOpenTry table

create table if not exists ibc_channelopentry_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    port_id                         VARCHAR          not null,
    previous_channel_id             VARCHAR          not null,
    channel_state                   VARCHAR          not null,
    channel_ordering                VARCHAR          not null,
    counterparty_port_id            VARCHAR          not null,
    counterparty_channel_id         VARCHAR          not null,
    connection_hops                 VARCHAR          not null,
    version_num                     VARCHAR          not null,
    counterparty_version            VARCHAR          not null,
    proof_init                      VARCHAR          not null,
    proof_height_revision_number    VARCHAR          not null,
    proof_height_revision_height    VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);

create index if not exists ibc_channelopentry_tx_id
    on ibc_channelopentry_msg (tx_id);

-- cosmos.staking.v1beta1.MsgEditValidator Table

create table if not exists cosmos_editvalidator_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    validator_address_id            uuid             not null,    
    tx_type                         VARCHAR          not null,
    description_moniker             VARCHAR          not null,
    description_identity            VARCHAR          not null,
    description_website             VARCHAR          not null,
    description_security_contact    VARCHAR          not null,
    description_details             VARCHAR          not null,
    commission_rate                 VARCHAR          ,
    min_self_delegation             VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (validator_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_editvalidator_validator_address_id
    on cosmos_editvalidator_msg (validator_address_id);

create index if not exists cosmos_editvalidator_tx_id
    on cosmos_editvalidator_msg (tx_id);


-- cosmos.gov.v1.MsgVote Table

create table if not exists cosmos_vote_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    tx_type                         VARCHAR          not null,
    proposal_id                     VARCHAR          not null,
    voter_address_id                uuid             not null,
    options                         VARCHAR          not null,
    metadata                        VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (voter_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);

create index if not exists cosmos_vote_voter_address_id
    on cosmos_vote_msg (voter_address_id);

create index if not exists cosmos_vote_tx_id
    on cosmos_vote_msg (tx_id);


-- cosmos.gov.v1beta1.MsgVote Table

create table if not exists cosmos_vote_beta1_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    tx_type                         VARCHAR          not null,
    proposal_id                     VARCHAR          not null,
    voter_address_id                uuid             not null,
    options                         VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (voter_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);

create index if not exists cosmos_vote_beta1_voter_address_id
    on cosmos_vote_beta1_msg (voter_address_id);

create index if not exists cosmos_vote_beta1_tx_id
    on cosmos_vote_beta1_msg (tx_id);



-- cosmos.bank.v1beta1.MsgMultiSend Table

create table if not exists cosmos_multisend_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    tx_type                         VARCHAR          not null,
    inputs_address_id               uuid            not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (inputs_address_id) REFERENCES address(address_id)
);

create index if not exists cosmos_multisend_inputs_address_id
    on cosmos_multisend_msg (inputs_address_id);

create index if not exists cosmos_multisend_tx_id
    on cosmos_multisend_msg (tx_id);


create table if not exists cosmos_multisend_outputs
(
    outputs_message_id         uuid default gen_random_uuid() not null
        primary key,
    message_id                       uuid             not null,
    outputs_address_id               uuid          not null,
    outputs_denom                    VARCHAR          not null,
    outputs_amount                   VARCHAR          not null,
    FOREIGN KEY (message_id) REFERENCES cosmos_multisend_msg(message_id),
    FOREIGN KEY (outputs_address_id) REFERENCES address(address_id)
);

create index if not exists cosmos_multisend_outputs_address_id
    on cosmos_multisend_outputs (outputs_address_id);

create index if not exists cosmos_multisend_message_id
    on cosmos_multisend_outputs (message_id);


-- /cosmos.slashing.v1beta1.MsgUnjail Table

create table if not exists cosmos_unjail_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    tx_type                         VARCHAR          not null,
    validator_addr_id               uuid            not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (validator_addr_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);

create index if not exists cosmos_unjail_validator_address_id
    on cosmos_unjail_msg (validator_addr_id);

create index if not exists cosmos_unjail_tx_id
    on cosmos_unjail_msg (tx_id);

create table if not exists ibc_core_channel_v1_msgchannelopenack
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    port_id                         VARCHAR          not null,
    channel_id                      VARCHAR          not null,
    counterparty_channel_id         VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);
create index if not exists ibc_core_channel_v1_msgchannelopenack_tx_id
    on ibc_core_channel_v1_msgchannelopenack(tx_id);

create table if not exists ibc_core_channel_v1_msgchannelopeninit
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    port_id                         VARCHAR          not null,
    channel                         jsonb            not null,
    channel_state                   VARCHAR          not null,
    channel_ordering                VARCHAR          not null,
    counterparty_port_id            VARCHAR          not null,
    counterparty_channel_id         VARCHAR          not null,
    connection_hops                 VARCHAR          not null,
    version_num                     VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);
create index if not exists ibc_core_channel_v1_msgchannelopeninit_tx_id
    on ibc_core_channel_v1_msgchannelopeninit(tx_id);


create table if not exists cosmwasm_msg_instantiate_contract2
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    send_address_id          uuid             not null,
    admin_address_id    uuid             not null, 
    tx_type             VARCHAR          not null,
    code_id             VARCHAR          not null,
    label               VARCHAR          not null,
    msg_swap_venues                 VARCHAR          not null,
    funds               VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (send_address_id) REFERENCES address(address_id),
    FOREIGN KEY (admin_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)

);

create index if not exists cosmwasm_instantiatecontract2_send_address_id
    on cosmwasm_instantiatecontract_msg (send_address_id);

create index if not exists cosmwasm_instantiatecontract2_admin_address_id
    on cosmwasm_instantiatecontract_msg (admin_address_id);

create index if not exists cosmwasm_instantiatecontract2_tx_id
    on cosmwasm_instantiatecontract_msg (tx_id);

create table if not exists cosmwasm_migratecontract_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    send_address_id          uuid             not null,
    tx_type             VARCHAR          not null,
    contracts           VARCHAR          not null,
    code_id             VARCHAR          not null,
    msg                 VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (send_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)

);

create index if not exists cosmwasm_migratecontract_send_address_id
    on cosmwasm_executecontract_msg (send_address_id);

create index if not exists cosmwasm_migratecontract_tx_id
    on cosmwasm_executecontract_msg (tx_id);

create index if not exists cosmwasm_migratecontract_contracts
    on cosmwasm_migratecontract_msg(contracts);


create table if not exists ibc_openconnectiontry_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    client_id                    VARCHAR          not null,
    previous_connection_id                     VARCHAR          not null,
    counterparty_client_id                  VARCHAR          not null,
    counterparty_connection_id                VARCHAR          not null,
    counterparty_versions_identifier            VARCHAR          not null,
    counterparty_versions_features              VARCHAR         not null,
    proof_init                                  VARCHAR         not null,
    proof_height_revision_number    VARCHAR          not null,
    proof_height_revision_height    VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);

create index if not exists ibc_openconnectiontry_msg_tx_id
    on ibc_openconnectiontry_msg(tx_id);

create index if not exists ibc_openconnectiontry_msg_proof_height
    on ibc_openconnectiontry_msg(proof_height_revision_height);





create table if not exists ibc_openconnectionconfirm_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    connection_id                   VARCHAR          not null,
    proof_height_revision_number    VARCHAR          not null,
    proof_height_revision_height    VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);

create index if not exists ibc_openconnectionconfirm_msg_tx_id
    on ibc_openconnectionconfirm_msg(tx_id);

create index if not exists ibc_openconnectionconfirm_msg_proof_height
    on ibc_openconnectionconfirm_msg(proof_height_revision_height);

create table if not exists ibc_createclient_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,    
    tx_type                         VARCHAR          not null,
    client_type                     VARCHAR          not null,
    client_chain_id                 VARCHAR          not null,
    client_trust_level_num          VARCHAR          not null,
    client_trust_level_denom        VARCHAR          not null,
    latest_height_revision_num      VARCHAR          not null,
    latest_height_revision_height   VARCHAR          not null,
    frozen_height_revision_number   VARCHAR          not null,
    frozen_height_revision_height   VARCHAR          not null,
    signer                          VARCHAR          ,
    signer_id                       VARCHAR          not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    UNIQUE(tx_id, comment)
);


create index if not exists ibc_createclient_msg_tx_id
    on ibc_createclient_msg(tx_id);


create table if not exists cosmos_submitproposal_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    tx_type                         VARCHAR          not null,
    title                       VARCHAR             not null,
    descriptions                VARCHAR             not null, 
    proposer_id         uuid        not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (proposer_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);


create index if not exists cosmos_submitproposal_id
    on cosmos_submitproposal_msg (proposer_id);

create index if not exists cosmos_submitproposal_tx_id
    on cosmos_submitproposal_msg (tx_id);




create table if not exists cosmos_deposit_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    tx_type                     VARCHAR             not null,
    proposal_id                 VARCHAR             not null, 
    depositor_id        uuid          not null,   
    deposit_denom               VARCHAR          not null,
    deposit_amount              VARCHAR         not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (depositor_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);



create index if not exists cosmos_deposit_id
    on cosmos_deposit_msg (depositor_id);

create index if not exists cosmos_deposit_tx_id
    on cosmos_deposit_msg (tx_id);



create table if not exists ibc_connectionopeninit_msg
(
    message_id         uuid default gen_random_uuid() not null
        primary key,
    tx_id                           uuid             not null,
    tx_type                     VARCHAR             not null,
    signer_id                      uuid             not null,
    signer                          VARCHAR         ,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (signer_id) REFERENCES address(address_id),
    UNIQUE(tx_id, comment)
);
create index if not exists ibc_connectionopeninit_msg_signer_id
    on ibc_connectionopeninit_msg (signer_id);
create index if not exists ibc_connectionopeninit_msg_tx_id
    on ibc_connectionopeninit_msg (tx_id);

create table if not exists message_table_lookup(
    message_table_id UUID default gen_random_uuid() not null primary key,
    tx_id UUID not null,
    message_id UUID not null,
    message_table_name VARCHAR not null
);

create index if not exists message_table_lookup_txs_and_msg_id
    on message_table_lookup (tx_id, message_id);

create table if not exists cosmos_setwithdrawaddress_msg (
    message_id         uuid default gen_random_uuid() not null primary key,
    tx_id                           uuid             not null,
    tx_type                     VARCHAR             not null,
    delegator_address_id            uuid             not null,
    withdraw_address_id            uuid             not null,
    message_info                    jsonb            not null,
    comment                         VARCHAR          not null,
    FOREIGN KEY (tx_id) REFERENCES transactions(tx_id),
    FOREIGN KEY (delegator_address_id) REFERENCES address(address_id),
    UNIQUE(tx_id, delegator_address_id, withdraw_address_id)
);

create table if not exists error_logs (
    error_log_id uuid default gen_random_uuid() not null primary key,
    error_log_timestamp timestamp with time zone not null,
    error_log_message VARCHAR
);