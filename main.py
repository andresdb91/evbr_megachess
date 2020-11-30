import asyncio
import argparse
import threading
import logging
import datetime

from config.default import config
import instance.config

from config_manager import ConfigManager
from game.client import GameClient
from ui import UI


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='Override token in configuration', type=str)

    cli = parser.add_mutually_exclusive_group()
    cli.add_argument('-i', '--interface', action='store_true', help='Enable command line interface')
    cli.add_argument('-n', '--no-interface', action='store_true', help='Disable command line interface')

    cmd_args = parser.parse_args()

    # Load and merge configuration files
    config.update(instance.config.config)

    # Configure and start logging
    logging.basicConfig(
        filename=f'logs/{datetime.datetime.now().timestamp()}.log',
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s (%(name)s): %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Override stored configuration with parameters
    if cmd_args.token:
        logger.info('Using token from command line')
        config['auth_token'] = cmd_args.token
    if cmd_args.interface:
        logger.info('Command line interface enabled')
        config['interface'] = True

    # Create configuration manager instance
    cfg_manager = ConfigManager(config)

    # Override log level with config
    if log_level := ConfigManager.get('log_level'):
        logger.level = log_level

    # Create game instance
    game = GameClient()

    # Start cli interface
    if config.get('interface'):
        ui = UI(game)
        logger.info('Starting UI thread')
        T = threading.Thread(target=ui.cli, daemon=True)
        T.start()

    # Call event loop
    logger.info('Starting game loop')
    try:
        asyncio.run(game.main())
    except RuntimeError:
        exit(1)
    except Exception:
        raise
