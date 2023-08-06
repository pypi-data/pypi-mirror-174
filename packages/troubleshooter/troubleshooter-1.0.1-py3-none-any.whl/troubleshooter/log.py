import logging


def _get_logger():
    """
    Get logger instance.

    Returns:
        Logger, a logger.
    """
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    return logger


def info(msg, *args, **kwargs):
    """
    Log a message with severity 'INFO' on the MindSpore logger.

    Examples:
        >>> from mindspore import log as logger
        >>> logger.info("The arg(%s) is: %r", name, arg)
    """
    _get_logger().info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """
    Log a message with severity 'DEBUG' on the MindSpore logger.

    Examples:
        >>> from mindspore import log as logger
        >>> logger.debug("The arg(%s) is: %r", name, arg)
    """
    _get_logger().debug(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """Log a message with severity 'ERROR' on the MindSpore logger."""
    _get_logger().error(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """Log a message with severity 'WARNING' on the MindSpore logger."""
    _get_logger().warning(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    """Log a message with severity 'CRITICAL' on the MindSpore logger."""
    _get_logger().critical(msg, *args, **kwargs)