# -*- coding: utf-8 -*-

# This is a very basic configuration file for encoder.
# Uncomment or add what you need.

# ========== Huskar ==========
# from zeus_core.huskar import set_huskar_options
# set_huskar_options(local_mode=False)  # enable huskar in development

from zeus_core.huskar import get_config_manager

config_manager = get_config_manager()


# ========== DB Settings ==========
# Change the credentials in "master" and "slave" to your needs
DB_SETTINGS = {
    'encoder': {
        'urls': {
            'master': config_manager.get(
                'DB_MASTER',
                'mysql+pymysql://root@localhost:3306/encoder?charset=utf8'),
            'slave': config_manager.get(
                'DB_SLAVE',
                'mysql+pymysql://root@localhost:3306/encoder?charset=utf8')
        },
        'max_overflow': config_manager.get('DB_MAX_OVERFLOW', -1),
        'pool_size': config_manager.get('DB_POOL_SIZE', 10),
        'pool_recycle': config_manager.get('DB_POOL_RECYCLE', 1200)
    }
}


# ========= Cache Settings ==========
# cache settings
CACHE_NAMESPACE = 'cache.encoder'
CACHE_SETTINGS = {
    'encoder': config_manager.get('REDIS_CACHE_DSN', 'redis://localhost:6379')}


# ========== Async Settings ==========
# Enable async feature by uncomment following line, see
# also: `app.yaml`

ASYNC_ENABLED = False
